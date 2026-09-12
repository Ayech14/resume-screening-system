import json
from typing import Set
import re
from datetime import datetime

class KeywordExtractor:

    def __init__(self, taxonomy_path: str):
        with open(taxonomy_path, "r") as file:
            self.skills_taxonomy = json.load(file)

    def extract_skills(self, text: str) -> Set[str]:
        found_skills = set()
        text_lower = text.lower()

        for category, skills in self.skills_taxonomy.items():
            for skill_name, variations in skills.items():
                for variation in variations:
                    pattern = r"(?<!\w)" + re.escape(variation.lower()) + r"(?!\w)"

                    if re.search(pattern, text_lower):
                        found_skills.add(skill_name)
                        break

        return found_skills

    def extract_experience_years(self, text: str) -> float:
        text_lower = text.lower()

        patterns = [
            r"(\d+)\+?\s*(?:years?|yrs?).*?(?:experience|exp)",
            r"(?:experience|exp).*?(\d+)\+?\s*(?:years?|yrs?)",
            r"over\s+(\d+)\s+(?:years?|yrs?)",
            r"more\s+than\s+(\d+)\s+(?:years?|yrs?)"
        ]

        years = []

        for pattern in patterns:
            for match in re.finditer(pattern, text_lower):
                year = float(match.group(1))

                if 0 < year < 50:
                    years.append(year)

        date_pattern = (
            r"(january|february|march|april|may|june|july|august|"
            r"september|october|november|december)\s+(\d{4})"
            r"\s*[-–]\s*"
            r"(present|(january|february|march|april|may|june|july|"
            r"august|september|october|november|december)\s+\d{4})"
        )

        for match in re.finditer(date_pattern, text_lower):
            start_month = match.group(1)
            start_year = int(match.group(2))
            end_text = match.group(3)

            start_date = datetime.strptime(
                f"{start_month} {start_year}", "%B %Y"
            )

            if end_text == "present":
                end_date = datetime.now()
            else:
                end_date = datetime.strptime(end_text, "%B %Y")

            months = (
                (end_date.year - start_date.year) * 12
                + (end_date.month - start_date.month)
            )

            if months > 0:
                years.append(months / 12)

        return round(max(years), 1) if years else 0.0

    def extract_keywords(self, text: str) -> Set[str]:
        found_keywords = set()
        text_lower = text.lower()

        for category, skills in self.skills_taxonomy.items():
            for skill_name, variations in skills.items():
                for variation in variations:
                    pattern = r"(?<!\w)" + re.escape(variation.lower()) + r"(?!\w)"

                    if re.search(pattern, text_lower):
                        found_keywords.add(skill_name)
                        break

        return found_keywords

    def extract_email(self, text: str) -> str:
        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        match = re.search(pattern, text)

        return match.group(0) if match else ""


    def extract_phone(self, text: str) -> str:
        pattern = (
            r"(?:\+?1[-.\s]?)?"
            r"(?:\(?\d{3}\)?[-.\s]?)"
            r"\d{3}[-.\s]?\d{4}"
        )

        match = re.search(pattern, text)

        return match.group(0) if match else ""

    ### this method doesn't work correctly for all resumes currently
    def extract_name(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if lines:
            return lines[0]

        return ""

    