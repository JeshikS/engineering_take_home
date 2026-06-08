import os
import requests
from dotenv import load_dotenv

load_dotenv()


class ApolloService:
    BASE_URL = "https://api.apollo.io/api/v1/organizations/search"

    def __init__(self):
        self.api_key = os.getenv("APOLLO_API_KEY")

        if not self.api_key:
            raise ValueError("APOLLO_API_KEY not found in environment variables")

    def get_company(self, domain: str) -> dict:
        payload = {
            "q_organization_domains_list": [domain]
        }

        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }

        response = requests.post(
            self.BASE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("organizations"):
            return {}

        company = data["organizations"][0]

        return {
            "id": company.get("id"),
            "name": company.get("name"),
            "domain": company.get("primary_domain"),
            "industry": company.get("industry"),
            "industries": company.get("industries", []),
            "employees": company.get("estimated_num_employees"),
            "revenue": company.get("organization_revenue"),
            "linkedin": company.get("linkedin_url"),
            "website": company.get("website_url"),
            "keywords": company.get("keywords", [])
        }
    def search_companies_by_industry(
        self,
        industry: str,
        page: int = 1,
        per_page: int = 50
    ):
        payload = {
            "organization_industries": [industry],
            "page": page,
            "per_page": per_page
        }

        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }

        response = requests.post(
            self.BASE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        companies = []

        for company in data.get("organizations", []):

            companies.append({
                "id": company.get("id"),
                "name": company.get("name"),
                "domain": company.get("primary_domain"),
                "industries": company.get("industries", []),
                "keywords": company.get("keywords", []),
                "employees": company.get(
                    "estimated_num_employees"
                )
            })

        return companies