# Resume Screening System

A Python-based resume screening application that evaluates and ranks candidates against a job description using skills, experience, and job-specific keywords.

**Live Demo:** [Resume Screening System](https://resume-screening-system-ayech14.streamlit.app/)

## Overview

The Resume Screening System is a Streamlit application designed to streamline the initial stage of candidate screening.

Recruiters can provide a job description and upload multiple resumes in PDF or DOCX format. The system extracts relevant candidate information, identifies skills and experience, calculates a configurable match score, and ranks candidates based on their overall fit.

The application provides a structured way to compare candidates while keeping the final hiring decision with the recruiter.

## Features

* Upload multiple PDF and DOCX resumes
* Parse job descriptions for required and preferred qualifications
* Extract candidate skills, experience, and contact information
* Compare candidates against job-specific requirements
* Configure scoring weights for different evaluation categories
* Rank candidates by overall match score
* Identify matched and missing skills
* Generate candidate recommendations
* Export screening results to CSV
* Interactive web interface built with Streamlit

## How It Works

The screening pipeline consists of four main stages:

### 1. Resume and Job Description Parsing

Resume files are parsed to extract their text content. The job description is analyzed to identify required skills, preferred skills, experience requirements, and relevant keywords.

### 2. Information Extraction

The system extracts skills, years of experience, keywords, and candidate contact information from the available text.

### 3. Candidate Scoring

Each candidate receives a weighted score based on four categories:

* Required Skills
* Preferred Skills
* Experience
* Keywords

The scoring weights can be adjusted directly from the application.

### 4. Ranking and Review

Candidates are ranked from highest to lowest score. Recruiters can review each candidate's matched skills, missing skills, experience, contact information, and recommendation before exporting the results.

## Scoring

The default scoring configuration is:

| Category         |   Weight |
| ---------------- | -------: |
| Required Skills  |      50% |
| Preferred Skills |      25% |
| Experience       |      15% |
| Keywords         |      10% |
| **Total**        | **100%** |

The scoring configuration can be adjusted by the recruiter as long as the total weight equals 100%.

Candidate recommendations are generated from the final match score:

| Score         | Recommendation |
| ------------- | -------------- |
| 80% and above | Strong Match   |
| 60%–79%       | Good Match     |
| 40%–59%       | Partial Match  |
| Below 40%     | Weak Match     |

## Technology Stack

* **Python** — Application logic and data processing
* **Streamlit** — Web interface
* **PyPDF2** — PDF text extraction
* **python-docx** — DOCX text extraction
* **Pandas** — Data processing and CSV export
* **Regular Expressions** — Text and information extraction
* **Git / GitHub** — Version control and project hosting

## Project Structure

```text
resume-screening-system/
│
├── app.py
├── requirements.txt
├── skills_taxonomy.json
│
├── parsers/
│   ├── resume_parser.py
│   └── jd_parser.py
│
├── extractors/
│   └── keyword_extractor.py
│
├── matcher/
│   └── scorer.py
│
├── data/
├── input/
├── output/
│
└── README.md
```

## Getting Started

### Prerequisites

* Python 3.10 or later
* pip

### Installation

Clone the repository:

```bash
git clone https://github.com/Ayech14/resume-screening-system.git
cd resume-screening-system
```

Create and activate a virtual environment.

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

## Usage

1. Enter or paste a job description.
2. Upload one or more candidate resumes.
3. Configure the scoring weights if necessary.
4. Select **Screen Resumes**.
5. Review the ranked candidates.
6. Examine matched and missing skills, experience, and recommendations.
7. Export the results as a CSV file.

## Future Improvements

Possible extensions to the system include:

* Candidate filtering and search
* More detailed score breakdowns
* Improved resume parsing and information extraction
* Expanded skills taxonomy
* Additional document format support
* Semantic or NLP-based can
