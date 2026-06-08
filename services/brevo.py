import os
import requests
from dotenv import load_dotenv

load_dotenv()


class BrevoService:
    BASE_URL = "https://api.brevo.com/v3/smtp/email"

    def __init__(self):
        self.api_key = os.getenv("BREVO_API_KEY")

        if not self.api_key:
            raise ValueError("BREVO_API_KEY not found")

    def send_email(
        self,
        recipient_email: str,
        recipient_name: str,
        subject: str,
        html_content: str,
    ):
        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }

        payload = {
            "sender": {
                "name": "Jeshik",
                "email": os.getenv("BREVO_SENDER_EMAIL"),
            },
            "to": [
                {
                    "email": recipient_email,
                    "name": recipient_name,
                }
            ],
            "subject": subject,
            "htmlContent": html_content,
        }

        response = requests.post(
            self.BASE_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()