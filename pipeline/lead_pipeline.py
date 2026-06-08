from datetime import datetime, timezone

from services.apollo import ApolloService
from services.hunter import HunterService

from utils.contact_filter import filter_decision_makers
from utils.logger import setup_logger

from pipeline.similar_company_finder import SimilarCompanyFinder

logger = setup_logger()


class LeadPipeline:

    def __init__(self):
        self.apollo = ApolloService()
        self.hunter = HunterService()

        self.similar_company_finder = (
            SimilarCompanyFinder(
                self.apollo
            )
        )

    def run(self, domain):

        try:

            logger.info(
                f"Fetching company data for {domain}"
            )

            company = self.apollo.get_company(
                domain
            )

            if not company:

                raise ValueError(
                    f"No company found for {domain}"
                )

        except Exception as e:

            logger.error(
                f"Apollo failed: {e}"
            )

            raise

        similar_companies = (
            self.similar_company_finder.find(
                company
            )
        )

        similar_company_leads = []

        for similar_company in similar_companies[:5]:

            try:

                logger.info(
                    f"Fetching contacts for "
                    f"{similar_company['name']}"
                )

                contacts = (
                    self.hunter.get_contacts(
                        similar_company["domain"]
                    )
                )

                decision_makers = (
                    filter_decision_makers(
                        contacts
                    )
                )

                if not decision_makers:

                    logger.warning(
                        f"No decision makers found for "
                        f"{similar_company['name']}"
                    )

                    continue

                logger.info(
                    f"Found "
                    f"{len(decision_makers)} "
                    f"decision makers for "
                    f"{similar_company['name']}"
                )

                similar_company_leads.append(
                    {
                        "company": similar_company,
                        "contacts": decision_makers
                    }
                )

            except Exception as e:

                logger.error(
                    f"Failed to fetch contacts for "
                    f"{similar_company['name']}: "
                    f"{e}"
                )

        total_contacts_found = sum(
            len(company["contacts"])
            for company in similar_company_leads
        )

        similar_companies_found = len(
            similar_company_leads
        )

        return {
            "source_company": company,
            "similar_companies_found":
                similar_companies_found,
            "total_contacts_found":
                total_contacts_found,
            "generated_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
            "similar_company_leads":
                similar_company_leads
        }