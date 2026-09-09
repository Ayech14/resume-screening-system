import streamlit as st
import tempfile
from pathlib import Path

from parsers.resume_parser import ResumeParser
from extractors.keyword_extractor import KeywordExtractor
from matcher.scorer import Scorer

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

            st.write(resume_text)
            st.write("Detected skills:", resume_skills)
            st.write("Detected keywords:", resume_keywords)
            st.write("Candidate experience:", candidate_years)
