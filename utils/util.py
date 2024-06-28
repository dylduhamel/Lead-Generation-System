import datetime
import pytz
import textwrap
import os
import re
import requests
from dotenv import load_dotenv

## Load environment variables from .env file
load_dotenv()

def get_address_from_lat_lng(lat, lng):
    # API Key
    api_key = os.getenv("GOOGLECLOUD_API_TOKEN")
    # Define the endpoint URL.
    endpoint_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}"

    # Send a GET request to the Google Maps API.
    response = requests.get(endpoint_url)

    # Check that the request was successful.
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            # Extract the formatted address from the response.
            formatted_address = data['results'][0]['formatted_address']
            return formatted_address
        else:
            return "Error: The API returned status: {}".format(data['status'])
    else:
        return "Error: The request was unsuccessful. Status code: {}".format(response.status_code)


# Get current date - * Used for DB, do not modify
def curr_date():
    current_date = datetime.datetime.now(pytz.timezone('America/New_York'))
    formatted_date = current_date.strftime("%m/%d/%Y")
    return formatted_date

# Get past month date
def past_month_date(months_back, current_date):
    date_obj = datetime.datetime.strptime(current_date, "%m/%d/%Y")
    past_date = date_obj - datetime.timedelta(days=months_back*30)
    formatted_date = past_date.strftime("%m/%d/%Y")
    return formatted_date

# Print status message
def status_print(message):
    """
    Prints out a message in a formatted way.
    """
    print("*" * 50)  # Print a line of *s
    # Print each line of the message in a formatted way
    for line in textwrap.wrap(message, width=45):
        print("* {: <45}*".format(line))
    print("*" * 50)  # Print a line of *s

# Get zipcode with API
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

# Format string in all caps with no spaces
def clean_string(input_string):
    # Convert the name to all uppercase and remove leading/trailing spaces
    formatted_name = input_string.strip().upper()
    
    # Remove extra spaces within the name
    formatted_name = re.sub(r'\s+', ' ', formatted_name)
    
    return formatted_name