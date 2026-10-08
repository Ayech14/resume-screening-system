# Resume Screening System

A Python-based resume screening and candidate ranking system that helps recruiters evaluate multiple resumes against a job description using skills, experience, and job-specific keywords.

## 🚀 Live Demo

Try the live application here:

👉 https://resume-screening-system-ayech14.streamlit.app/

## 📌 Overview

The Resume Screening System automates the initial stage of candidate screening by analyzing uploaded resumes against a provided job description.

The application extracts relevant candidate information, identifies skills and experience, calculates a weighted match score, and ranks candidates from strongest to weakest match.

The system is designed as a lightweight recruiter-focused tool that demonstrates practical applications of Python, natural language processing concepts, data processing, and Streamlit.

## ✨ Features

* 📄 Upload multiple PDF or DOCX resumes
* 📝 Paste a job description directly into the application
* 🔍 Extract candidate skills and experience
* 📊 Calculate candidate match scores
* ⚖️ Configure scoring weights
* 🏆 Automatically rank candidates
* 👤 Extract candidate contact information
* 💡 Provide candidate recommendations
* 🏷️ Display matched and missing skills
* 📥 Export screening results as CSV
* 🖥️ Interactive Streamlit interface

## 🧠 How It Works

The screening process follows several stages:

1. **Resume Parsing**

   * Extracts text from PDF and DOCX resumes.

2. **Job Description Parsing**

   * Identifies required skills, preferred skills, experience requirements, and target keywords.

3. **Keyword & Skill Extraction**

   * Compares resume content against the application's skills taxonomy.

4. **Candidate Scoring**

   * Calculates a weighted match score based on:

     * Required Skills
     * Preferred Skills
     * Experience
     * Keywords

5. **Candidate Ranking**

   * Candidates are sorted from highest to lowest match score.

6. **Recruiter Review**

   * Recruiters can review candidate details, matched skills, missing skills, experience, recommendations, and export the results.

## ⚖️ Scoring System

The default scoring configuration is:

| Category         | Default Weight |
| ---------------- | -------------: |
| Required Skills  |            50% |
| Preferred Skills |            25% |
| Experience       |            15% |
| Keywords         |            10% |

The application allows recruiters to adjust these weights depending on the requirements of a particular screening process.

Candidate recommendations are based on the final score:

| Score     | Recommendation |
| --------- | -------------- |
| 80%+      | Strong Match   |
| 60–79%    | Good Match     |
| 40–59%    | Partial Match  |
| Below 40% | Weak Match     |

## 🛠️ Technologies

* **Python**
* **Streamlit**
* **PyPDF2**
* **python-docx**
* **Pandas**
* **Regular Expressions**
* **Git & GitHub**

## 📂 Project Structure

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

## 💻 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ayech14/resume-screening-system.git
cd resume-screening-system
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📖 Usage

1. Enter a job description.
2. Upload one or more candidate resumes.
3. Adjust the scoring configuration if needed.
4. Click **Screen Resumes**.
5. Review the candidate rankings.
6. Examine matched and missing skills.
7. Review candidate recommendations.
8. Export the results as a CSV file if needed.

## 🔮 Future Improvements

Potential future improvements include:

* Candidate filtering and search
* More detailed score transparency
* Improved resume parsing
* Expanded skills taxonomy
* Support for additional document formats
* Advanced NLP-based semantic matching
* Recruiter dashboards and analytics
* Database integration

## ⚠️ Disclaimer

This project is intended as an educational and portfolio project. Screening results should be treated as decision-support information rather than an automated replacement for human hiring decisions.


