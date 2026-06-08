from services.apollo import ApolloService
from services.hunter import HunterService
from utils.contact_filter import filter_decision_makers


class LeadPipeline:

    def __init__(self):
        self.apollo = ApolloService()
        self.hunter = HunterService()

    def run(self, domain):
        company = self.apollo.get_company(domain)

        contacts = self.hunter.get_contacts(domain)

        decision_makers = filter_decision_makers(contacts)

        return {
            "company": company,
            "contacts": decision_makers
        }