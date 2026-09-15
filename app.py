import streamlit as st
import tempfile
import csv
from pathlib import Path

from parsers.resume_parser import ResumeParser
from extractors.keyword_extractor import KeywordExtractor
from matcher.scorer import Scorer
from parsers.jd_parser import JDParser
from io import StringIO

st.title("Resume Screening System")

job_description = st.text_area(
    "Job Description",
    placeholder="Paste the job description here..."
    
)

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if st.button("Screen Resumes"):
    if not job_description:
        st.error("Please enter a job description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        parser = ResumeParser()
        extractor = KeywordExtractor("data/skills_taxonomy.json")
        jd_parser = JDParser("data/skills_taxonomy.json")
        scorer = Scorer()

        jd_data = jd_parser.parse(job_description)

        results = []

        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=Path(uploaded_file.name).suffix
            ) as temp_file:

                temp_file.write(uploaded_file.getbuffer())

            file_path = Path(temp_file.name)

            resume_text = parser.parse(file_path)

            resume_skills = extractor.extract_skills(resume_text)

            resume_keywords = extractor.extract_keywords(resume_text)

            candidate_years = extractor.extract_experience_years(resume_text)

            candidate_name = extractor.extract_name(resume_text)
            candidate_email = extractor.extract_email(resume_text)
            candidate_phone = extractor.extract_phone(resume_text)

            required_skills = jd_data["required_skills"]
            preferred_skills = jd_data["preferred_skills"]
            required_years = jd_data["required_years"]
            target_keywords = jd_data["target_keywords"]

            score = scorer.score_candidate(
                resume_skills,
                required_skills,
                preferred_skills,
                candidate_years,
                required_years,
                resume_keywords,
                target_keywords
        )
            

            matched_required = resume_skills & required_skills
            missing_required = required_skills - resume_skills
            matched_preferred = resume_skills & preferred_skills
            missing_preferred = preferred_skills - resume_skills
            experience_gap = max(required_years - candidate_years, 0)
            if score >= 80:
                recommendation = "Strong Match"
            elif score >= 60:
                recommendation = "Good Match"
            elif score >= 40:
                recommendation = "Partial Match"
            else:
                recommendation = "Weak Match"

            results.append({
                "filename": uploaded_file.name,
                "name": candidate_name,
                "email": candidate_email,
                "phone": candidate_phone,
                "score": score,
                "recommendation": recommendation,
                "experience": candidate_years,
                "matched_required": matched_required,
                "missing_required": missing_required,
                "matched_preferred": matched_preferred,
                "missing_preferred": missing_preferred,
                "experience_gap": experience_gap,
            })
            st.write(resume_text)
            st.write("Detected skills:", resume_skills)
            st.write("Detected keywords:", resume_keywords)
            st.write("Candidate experience:", candidate_years)
            st.subheader(f"Match Score: {score}%")
            st.write("Matched required skills:", matched_required)
            st.write("Missing required skills:", missing_required)
            st.write("Matched preferred skills:", matched_preferred)
            st.write("Missing preferred skills:", missing_preferred)
            st.write("Required experience:", required_years, "years")
            st.write("Experience gap:", round(experience_gap, 1), "years")
            
        results.sort(key=lambda candidate: candidate["score"], reverse=True)

        st.subheader("Screening Summary")

        total_candidates = len(results)
        average_score = sum(
            candidate["score"] for candidate in results
        ) / total_candidates

        top_candidate = results[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Candidates Screened",
                total_candidates
            )

        with col2:
            st.metric(
                "Average Match Score",
                f"{average_score:.2f}%"
            )

        with col3:
            st.metric(
                "Top Candidate",
                f"{top_candidate['score']}%"
            )

        st.write(
            f"**Top Candidate:** {top_candidate['name']}"
        )

        st.divider()

        st.subheader("Candidate Rankings")

        for rank, candidate in enumerate(results, start=1):

            required_matched = len(candidate["matched_required"])
            required_total = (
                required_matched + len(candidate["missing_required"])
            )

            with st.expander(
                f"{rank}. {candidate['filename']} — {candidate['score']}%"
            ):
                st.write(f"**Candidate:** {candidate['name']}")
                st.write(f"**Email:** {candidate['email']}")
                st.write(f"**Phone:** {candidate['phone']}")
                st.write(
                    f"**Recommendation:** {candidate['recommendation']}"
                )
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Match Score",
                        f"{candidate['score']}%"
                    )

                with col2:
                    st.metric(
                        "Experience",
                        f"{candidate['experience']} years"
                    )

                with col3:
                    st.metric(
                        "Required Skills",
                        f"{required_matched}/{required_total}"
                    )

                st.write(
                    "**Matched Required Skills:**",
                    candidate["matched_required"]
                )

                st.write(
                    "**Missing Required Skills:**",
                    candidate["missing_required"]
                )

                st.write(
                    "**Matched Preferred Skills:**",
                    candidate["matched_preferred"]
                )

                st.write(
                    "**Missing Preferred Skills:**",
                    candidate["missing_preferred"]
                )

                st.write(
                    "**Experience Gap:**",
                    round(candidate["experience_gap"], 1),
                    "years"
                )
                csv_buffer = StringIO()

        writer = csv.writer(csv_buffer)

        writer.writerow([
            "Rank",
            "Candidate",
            "Email",
            "Phone",
            "Score",
            "Recommendation",
            "Experience",
            "Required Skills Matched",
            "Missing Required Skills",
            "Matched Preferred Skills",
            "Missing Preferred Skills",
            "Experience Gap"
        ])

        for rank, candidate in enumerate(results, start=1):
            required_matched = len(candidate["matched_required"])
            required_total = (
                required_matched + len(candidate["missing_required"])
            )

            writer.writerow([
                rank,
                candidate["name"],
                candidate["email"],
                candidate["phone"],
                candidate["score"],
                candidate["recommendation"],
                candidate["experience"],
                f"{required_matched}/{required_total}",
                ", ".join(sorted(candidate["missing_required"])),
                ", ".join(sorted(candidate["matched_preferred"])),
                ", ".join(sorted(candidate["missing_preferred"])),
                round(candidate["experience_gap"], 1)
            ])

        st.download_button(
            label="Download Results as CSV",
            data=csv_buffer.getvalue(),
            file_name="resume_screening_results.csv",
            mime="text/csv"
        )
            
