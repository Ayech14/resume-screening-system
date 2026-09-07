class Scorer:

    def calculate_score(
        self,
        required_skills_score: float,
        preferred_skills_score: float,
        experience_score: float,
        keyword_score: float
    ) -> float:

        total_score = (
            required_skills_score * 0.50
            + preferred_skills_score * 0.25
            + experience_score * 0.15
            + keyword_score * 0.10
        )

        return round(total_score * 100, 2)

    def calculate_skill_match(
        self,
        resume_skills: set[str],
        target_skills: set[str]
    ) -> float:

        if not target_skills:
            return 0.0

        matched_skills = resume_skills & target_skills

        return len(matched_skills) / len(target_skills)


    
    def calculate_skills_score(
        self,
        resume_skills: set[str],
        required_skills: set[str],
        preferred_skills: set[str]
    ) -> float:

        required_score = self.calculate_skill_match(
            resume_skills,
            required_skills
        )

        preferred_score = self.calculate_skill_match(
            resume_skills,
            preferred_skills
        )

        return (
            required_score * 0.50
            + preferred_score * 0.25
        )


    def calculate_experience_score(
        self,
        candidate_years: float,
        required_years: float
    ) -> float:

        if required_years <= 0:
            return 1.0

        return min(candidate_years / required_years, 1.0)

    def calculate_keyword_score(
        self,
        resume_keywords: set[str],
        target_keywords: set[str]
    ) -> float:

        if not target_keywords:
            return 0.0

        matched_keywords = resume_keywords & target_keywords

        return len(matched_keywords) / len(target_keywords)


    def score_candidate(
        self,
        resume_skills: set[str],
        required_skills: set[str],
        preferred_skills: set[str],
        candidate_years: float,
        required_years: float,
        resume_keywords: set[str],
        target_keywords: set[str]
    ) -> float:

        required_score = self.calculate_skill_match(
            resume_skills,
            required_skills
        )

        preferred_score = self.calculate_skill_match(
            resume_skills,
            preferred_skills
        )

        experience_score = self.calculate_experience_score(
            candidate_years,
            required_years
        )

        keyword_score = self.calculate_keyword_score(
            resume_keywords,
            target_keywords
        )

        return self.calculate_score(
            required_score,
            preferred_score,
            experience_score,
            keyword_score
        )