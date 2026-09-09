import json
from typing import Set
import re


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

    def extract_experience_years(self, text: str) -> int:
        text_lower = text.lower()

        patterns = [
            r"(\d+)\+?\s*(?:years?|yrs?).*?(?:experience|exp)",
            r"(?:experience|exp).*?(\d+)\+?\s*(?:years?|yrs?)",
            r"over\s+(\d+)\s+(?:years?|yrs?)",
            r"more\s+than\s+(\d+)\s+(?:years?|yrs?)"
        ]

        years = []

        for pattern in patterns:
            matches = re.finditer(pattern, text_lower)

            for match in matches:
                year = int(match.group(1))

                if 0 < year < 50:
                    years.append(year)

        return max(years) if years else 0

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

    