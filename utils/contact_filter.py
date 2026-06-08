DECISION_MAKER_KEYWORDS = [
    "chief executive officer",
    "ceo",

    "chief technology officer",
    "cto",

    "chief financial officer",
    "cfo",

    "chief operating officer",
    "coo",

    "chief marketing officer",
    "cmo",

    "chief product officer",
    "cpo",

    "founder",
    "co-founder",

    "vice president",
    "vp",

    "director",

    "head",

    "manager"
]


def filter_decision_makers(contacts):
    filtered_contacts = []

    for contact in contacts:
        position = (contact.get("position") or "").lower()

        if (
            contact.get("confidence", 0) >= 80
            and any(
                keyword in position
                for keyword in DECISION_MAKER_KEYWORDS
            )
        ):
            filtered_contacts.append(contact)

    return filtered_contacts