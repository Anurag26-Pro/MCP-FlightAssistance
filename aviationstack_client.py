import requests
from config import AVIATIONSTACK_API_KEY

BASE_URL = "http://api.aviationstack.com/v1"

def get_flight_status(flight_iata):
    url = f"{BASE_URL}/flights?access_key={AVIATIONSTACK_API_KEY}&flight_iata={flight_iata}"
    response = requests.get(url)
    return response.json()
