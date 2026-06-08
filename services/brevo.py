import os

from dotenv import load_dotenv

from utils.retry_session import (
    create_retry_session
)

load_dotenv()


class BrevoService:

    BASE_URL = (
        "https://api.brevo.com/"
        "v3/smtp/email"
    )

    def __init__(self):

        self.api_key = os.getenv(
            "BREVO_API_KEY"
        )

        if not self.api_key:

            raise ValueError(
                "BREVO_API_KEY not found"
            )

        self.sender_name = os.getenv(
            "BREVO_SENDER_NAME"
        )

        self.sender_email = os.getenv(
            "BREVO_SENDER_EMAIL"
        )

        if not self.sender_name:

            raise ValueError(
                "BREVO_SENDER_NAME not found"
            )

        if not self.sender_email:

            raise ValueError(
                "BREVO_SENDER_EMAIL not found"
            )

        self.session = (
            create_retry_session()
        )

        self.headers = {
            "accept":
                "application/json",
            "api-key":
                self.api_key,
            "content-type":
                "application/json",
        }

    def send_email(
        self,
        recipient_email: str,
        recipient_name: str,
        subject: str,
        html_content: str,
    ):

        payload = {
            "sender": {
                "name":
                    self.sender_name,
                "email":
                    self.sender_email,
            },
            "to": [
                {
                    "email":
                        recipient_email,
                    "name":
                        recipient_name,
                }
            ],
            "subject":
                subject,
            "htmlContent":
                html_content,
        }

        response = self.session.post(
            self.BASE_URL,
            json=payload,
            headers=self.headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()