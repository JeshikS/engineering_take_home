import os
import sys

from dotenv import load_dotenv

from pipeline.lead_pipeline import LeadPipeline
from services.brevo import BrevoService

from utils.file_utils import save_json
from utils.email_template import generate_email
from utils.logger import setup_logger


logger = setup_logger()

load_dotenv()

TEST_EMAIL = os.getenv(
    "TEST_EMAIL"
)


def main():

    if len(sys.argv) not in [2, 3]:

        print(
            "Usage: "
            "python main.py <domain> [--test]"
        )

        sys.exit(1)

    domain = sys.argv[1]

    TEST_MODE = (
        "--test" in sys.argv
    )

    if TEST_MODE and not TEST_EMAIL:

        raise ValueError(
            "TEST_EMAIL is required "
            "when using --test"
        )

    pipeline = LeadPipeline()

    result = pipeline.run(
        domain
    )

    save_json(
        result,
        f"leads_{domain}.json"
    )

    source_company = (
        result["source_company"]
    )

    similar_company_leads = (
        result["similar_company_leads"]
    )

    print(
        f"\nSource Company: "
        f"{source_company['name']}"
    )

    print(
        f"Similar Companies Found: "
        f"{result['similar_companies_found']}"
    )

    print(
        f"Decision Makers Found: "
        f"{result['total_contacts_found']}"
    )

    if TEST_MODE:

        print(
            f"Mode: TEST "
            f"({TEST_EMAIL})"
        )

    else:

        print(
            "Mode: LIVE"
        )

    confirm = input(
        "\nSend emails? (y/n): "
    )

    if confirm.lower() != "y":

        print(
            "Email sending cancelled."
        )

        return

    brevo = BrevoService()

    emails_sent = 0

    for lead in similar_company_leads:

        company = lead["company"]

        contacts = lead["contacts"]

        for contact in contacts:

            try:

                html_content = (
                    generate_email(
                        company,
                        contact
                    )
                )

                recipient_email = (
                    TEST_EMAIL
                    if TEST_MODE
                    else contact["email"]
                )

                brevo.send_email(
                    recipient_email=
                        recipient_email,

                    recipient_name=
                        (
                            f"{contact['first_name']} "
                            f"{contact['last_name']}"
                        ),

                    subject=
                        (
                            f"Regarding "
                            f"{company['name']}"
                        ),

                    html_content=
                        html_content
                )

                emails_sent += 1

                logger.info(
                    f"Email sent to "
                    f"{recipient_email}"
                )

            except Exception as e:

                logger.error(
                    f"Failed to send email "
                    f"to "
                    f"{contact.get('email')}: "
                    f"{e}"
                )

    print(
        f"\nFinished. "
        f"{emails_sent} emails sent."
    )


if __name__ == "__main__":
    main()