from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests


def get_photo(city, state):
    # Use the Pexels API
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": f"{city} {state}", "per_page": 1}

    # Create a dictionary of data to use containing
    response_json = requests.get(url, params=params, headers=headers).json()

    # Extract src URL of picture
    picture_url = {
        "picture_url": response_json["photos"][0]["src"]["original"]
    }

    # Return the dictionary
    try:
        return picture_url
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(city, state):
    # Use the Open Weather API
    geo_response = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},US&limit=1&appid={OPEN_WEATHER_API_KEY}"
    ).json()

    try:
        lat = geo_response[0]["lat"]
        lon = geo_response[0]["lon"]
    except (KeyError, IndexError):
        return None

    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}"
    ).json()

    weather = {
        "temp": weather_response["main"]["temp"],
        "description": weather_response["weather"][0]["description"],
    }
    try:
        return weather
    except (KeyError, IndexError):
        return None
