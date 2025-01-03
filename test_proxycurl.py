import requests

from utils.prompt_utils import json_to_nested_string

API_KEY = "g_xYUCQdFISo30DkFqzZDA"
API_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"

headers = {"Authorization": "Bearer " + API_KEY}
params = {
    "linkedin_profile_url": "https://www.linkedin.com/in/danielkimdk/",
    "extra": "include",
}
response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=12)
response = response.json()

print(json_to_nested_string(response))
