import os
import requests
from dotenv import load_dotenv

load_dotenv()


class HunterService:
    BASE_URL = "https://api.hunter.io/v2/domain-search"

    def __init__(self):
        self.api_key = os.getenv("HUNTER_API_KEY")

        if not self.api_key:
            raise ValueError("HUNTER_API_KEY not found")

    def get_contacts(self, domain: str) -> list:
        response = requests.get(
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

        for person in data.get("data", {}).get("emails", []):
            contacts.append({
                "first_name": person.get("first_name"),
                "last_name": person.get("last_name"),
                "position": person.get("position"),
                "email": person.get("value"),
                "confidence": person.get("confidence")
            })

        return contacts