import logging

logger = logging.getLogger(__name__)


class SimilarCompanyFinder:

    def __init__(self, apollo_service):
        self.apollo = apollo_service

    def calculate_similarity(
        self,
        source_company,
        candidate_company
    ):

        score = 0

        source_industries = set(
            source_company.get("industries", [])
        )

        candidate_industries = set(
            candidate_company.get("industries", [])
        )

        industry_overlap = len(
            source_industries &
            candidate_industries
        )

        if industry_overlap < 2:
            return 0

        score += industry_overlap * 10

        source_keywords = set(
            source_company.get("keywords", [])
        )

        candidate_keywords = set(
            candidate_company.get("keywords", [])
        )

        keyword_overlap = len(
            source_keywords &
            candidate_keywords
        )

        score += keyword_overlap * 2

        source_employees = (
            source_company.get("employees")
            or 0
        )

        candidate_employees = (
            candidate_company.get("employees")
            or 0
        )

        if (
            source_employees > 0
            and candidate_employees > 0
        ):

            employee_ratio = (
                min(
                    source_employees,
                    candidate_employees
                )
                /
                max(
                    source_employees,
                    candidate_employees
                )
            )

            score += int(
                employee_ratio * 20
            )

        return score

    def find(
        self,
        source_company
    ):

        candidates = {}

        for industry in source_company.get(
            "industries",
            []
        ):

            logger.info(
                f"Searching industry: {industry}"
            )

            try:

                companies = (
                    self.apollo
                    .search_companies_by_industry(
                        industry
                    )
                )

                for company in companies:

                    if (
                        company["domain"]
                        ==
                        source_company["domain"]
                    ):
                        continue

                    candidates[
                        company["id"]
                    ] = company

            except Exception as e:

                logger.error(
                    f"Industry search failed: {e}"
                )

        ranked = []

        for company in candidates.values():

            score = (
                self.calculate_similarity(
                    source_company,
                    company
                )
            )

            if score > 0:

                company[
                    "similarity_score"
                ] = score

                ranked.append(company)

        ranked.sort(
            key=lambda x:
            x["similarity_score"],
            reverse=True
        )

        logger.info(
            f"Found {len(ranked)} similar companies"
        )

        return ranked[:10]