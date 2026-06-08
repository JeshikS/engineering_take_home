from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_retry_session():

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[
            429,
            500,
            502,
            503,
            504
        ],
        allowed_methods=[
            "GET",
            "POST"
        ]
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy
    )

    session = Session()

    session.mount(
        "https://",
        adapter
    )

    session.mount(
        "http://",
        adapter
    )

    return session