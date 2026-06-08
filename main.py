import sys
from pipeline.lead_pipeline import LeadPipeline
from utils.file_utils import save_json
from services.brevo import BrevoService
from utils.email_template import generate_email

SEND_EMAILS = False
def main():

    domain = sys.argv[1]

    pipeline = LeadPipeline()

    result = pipeline.run(domain)

    save_json(result, f"leads_{domain}.json")
    print(f"\nCompany: {result['company']['name']}")
    print(f"Decision makers found: {len(result['contacts'])}")

    confirm = input("\nSend emails? (y/n): ")

    if confirm.lower() != "y":
        print("Email sending cancelled.")
        return

    if SEND_EMAILS:

        brevo = BrevoService()

        company = result["company"]

        for contact in result["contacts"]:

            html_content = generate_email(
                company,
                contact
            )

            brevo.send_email(
                recipient_email=contact["email"],
                recipient_name=f"{contact['first_name']} {contact['last_name']}",
                subject=f"Regarding {company['name']}",
                html_content=html_content
            )

            print(
                f"Email sent to {contact['email']}"
            )


if __name__ == "__main__":
    main()