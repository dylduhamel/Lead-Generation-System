import os
import requests
from dotenv import load_dotenv

## Load environment variables from .env file
load_dotenv()

def get_zipcode(lat, lon):
    key = os.getenv("OPENCAGE_GEO_API_TOKEN")
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={key}"
    
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and len(data['results']) > 0:
        components = data['results'][0]['components']
        return components.get('postcode')
    else:
        return None
