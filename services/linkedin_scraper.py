import os

import requests

PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")


def scrape_linkedin_profile(linkedin_url):
    """
    Scrape the LinkedIn profile at the given URL and return extracted data.

    Args:
        linkedin_url (str): The URL of the LinkedIn profile to scrape.

    Returns:
        dict: A dictionary containing the scraped data.
    """

    response = requests.get(
        "https://nubela.co/proxycurl/api/v2/linkedin",
        params={"linkedin_profile_url": linkedin_url, "extra": "include"},
        headers={"Authorization": "Bearer " + PROXYCURL_API_KEY},
        timeout=20,
    )
    response.raise_for_status()

    data: dict = response.json()

    # Remove unnecessary fields
    data.pop("profile_pic_url", None)
    data.pop("background_cover_image_url", None)
    data.pop("people_also_viewed", None)
    data.pop("similarly_named_profiles", None)

    return data
