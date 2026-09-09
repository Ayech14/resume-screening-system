from extractors.keyword_extractor import KeywordExtractor


class JDParser:

    def __init__(self, taxonomy_path: str):
        self.keyword_extractor = KeywordExtractor(taxonomy_path)

    def _extract_section(
        self,
        job_description: str,
        section_name: str
    ) -> str:
        lines = job_description.splitlines()

        collecting = False
        section_lines = []

        for line in lines:
            line = line.strip()

            if line.lower().startswith(section_name.lower()):
                collecting = True
                continue

            if collecting and line.endswith(":"):
                break

            if collecting:
                section_lines.append(line)

        return "\n".join(section_lines)

    def _extract_years(self, experience_text: str) -> float:
        import re

        match = re.search(r"(\d+(?:\.\d+)?)\+?\s+years?", experience_text.lower())

        if match:
            return float(match.group(1))

        return 0.0

    def parse(self, job_description: str) -> dict:
        required_section = self._extract_section(
            job_description,
            "Required Skills"
        )

        preferred_section = self._extract_section(
            job_description,
            "Preferred Skills"
        )

        experience_section = self._extract_section(
            job_description,
            "Experience"
        )

        required_skills = self.keyword_extractor.extract_skills(
            required_section
        )

        preferred_skills = self.keyword_extractor.extract_skills(
            preferred_section
        )

        required_years = self._extract_years(experience_section)
        
        target_keywords = self.keyword_extractor.extract_keywords(job_description)

        return {
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "required_years": required_years,
            "target_keywords": target_keywords
        }