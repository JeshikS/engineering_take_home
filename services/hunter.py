import os

from dotenv import load_dotenv

from utils.retry_session import (
    create_retry_session
)

load_dotenv()


class HunterService:

    BASE_URL = (
        "https://api.hunter.io/"
        "v2/domain-search"
    )

    def __init__(self):

        self.api_key = os.getenv(
            "HUNTER_API_KEY"
        )

        if not self.api_key:

            raise ValueError(
                "HUNTER_API_KEY not found"
            )

        self.session = (
            create_retry_session()
        )

    def get_contacts(
        self,
        domain: str
    ) -> list:

        response = self.session.get(
            self.BASE_URL,
            params={
                "domain": domain,
                "api_key": self.api_key
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        contacts = []

        for person in (
            data.get(
                "data",
                {}
            ).get(
                "emails",
                []
            )
        ):

            email = person.get(
                "value"
            )

            if not email:
                continue

            contacts.append(
                {
                    "first_name":
                        person.get(
                            "first_name"
                        ) or "",
                    "last_name":
                        person.get(
                            "last_name"
                        ) or "",
                    "position":
                        person.get(
                            "position"
                        ),
                    "email":
                        email,
                    "confidence":
                        person.get(
                            "confidence"
                        )
                }
            )

        return contacts