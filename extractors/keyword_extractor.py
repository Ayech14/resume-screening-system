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