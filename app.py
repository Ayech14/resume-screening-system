import streamlit as st
import tempfile
from pathlib import Path

from parsers.resume_parser import ResumeParser
from extractors.keyword_extractor import KeywordExtractor
from matcher.scorer import Scorer
from parsers.jd_parser import JDParser

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
