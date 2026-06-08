import sys
import os
from dotenv import load_dotenv
from pipeline.lead_pipeline import LeadPipeline
from services.brevo import BrevoService

from utils.file_utils import save_json
from utils.email_template import generate_email
from utils.logger import setup_logger
from pipeline.similar_company_finder import SimilarCompanyFinder

logger = setup_logger()
load_dotenv()
TEST_EMAIL = os.getenv("TEST_EMAIL")

def main():

    if len(sys.argv) < 2:

        print(
            "Usage: python main.py <domain>"
        )

        sys.exit(1)

    domain = sys.argv[1]
    TEST_MODE = "--test" in sys.argv
    pipeline = LeadPipeline()

    result = pipeline.run(domain)

    company = result["company"]

    candidate_companies = [
        {
            "name": "Checkout.com",
            "industries": [
                "financial services",
                "internet"
            ],
            "keywords": [
                "payments",
                "payment gateway"
            ],
            "employees": 1800
        },
        {
            "name": "Adyen",
            "industries": [
                "financial services",
                "internet"
            ],
            "keywords": [
                "payments",
                "payment processing"
            ],
            "employees": 4000
        }
    ]

    finder = SimilarCompanyFinder()

    similar_companies = finder.rank_companies(
        source_company=company,
        candidate_companies=candidate_companies
    )

    save_json(
        similar_companies,
        "similar_companies.json"
    )

    save_json(
        result,
        f"leads_{domain}.json"
    )

    print(
        f"\nCompany: {result['company']['name']}"
    )

    print(
        f"Decision makers found: {len(result['contacts'])}"
    )
    if TEST_MODE:
        print(f"Mode: TEST ({TEST_EMAIL})")
    else:
        print("Mode: LIVE")

    confirm = input(
        "\nSend emails? (y/n): "
    )

    if confirm.lower() != "y":

        print(
            "Email sending cancelled."
        )

        return

    brevo = BrevoService()

    company = result["company"]

    for contact in result["contacts"]:

        try:

            html_content = generate_email(
                company,
                contact
            )

            recipient_email = (
                TEST_EMAIL
                if TEST_MODE
                else contact["email"]
            )

            brevo.send_email(
                recipient_email=recipient_email,
                recipient_name=f"{contact['first_name']} {contact['last_name']}",
                subject=f"Regarding {company['name']}",
                html_content=html_content
            )

            logger.info(
                f"Email sent to {contact['email']}"
            )

        except Exception as e:

            logger.error(
                f"Failed to send email to "
                f"{contact['email']}: {e}"
            )


if __name__ == "__main__":
    main()