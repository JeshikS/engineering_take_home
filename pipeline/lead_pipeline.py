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

            company = self.apollo.get_company(domain)

        except Exception as e:

            logger.error(
                f"Apollo failed: {e}"
            )

            raise

        try:

            logger.info(
                f"Fetching contacts for {domain}"
            )

            contacts = self.hunter.get_contacts(domain)

        except Exception as e:

            logger.error(
                f"Hunter failed: {e}"
            )

            contacts = []

        decision_makers = filter_decision_makers(
            contacts
        )

        logger.info(
            f"Found {len(decision_makers)} decision makers"
        )
        similar_companies = (
            self.similar_company_finder.find(
                company
            )
        )

        return {
            "company": company,
            "contacts": decision_makers,
            "similar_companies": similar_companies
        }