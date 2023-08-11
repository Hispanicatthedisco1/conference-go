import requests
from .keys import PEXELS_API_KEY


def get_picture_url(query):
    """
    Get the URL of a picture from the Pexels API
    """
    url = f"https://api.pexels.com/v1/search?query={query}"

    headers = {"Authorization": PEXELS_API_KEY}

    response = requests.get(url, headers=headers)
    api_dict = response.json()
    return api_dict["photos"][0]["src"]["original"]
