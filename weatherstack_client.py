import requests
from config import WEATHERSTACK_API_KEY  # Ensure this is defined in your config.py file

# Define the base URL for Weatherstack
WEATHERSTACK_BASE_URL = "http://api.weatherstack.com/current"

# Function to get weather data for an airport by IATA code
def get_weather_data(airport_code):
    """
    Fetch weather data for a given airport IATA code from the Weatherstack API.

    :param airport_code: IATA code of the airport (e.g., 'LAX', 'JFK')
    :return: JSON response containing weather data
    """
    weather_url = f"{WEATHERSTACK_BASE_URL}?access_key={WEATHERSTACK_API_KEY}&query={airport_code}"
    response = requests.get(weather_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch weather data"}
