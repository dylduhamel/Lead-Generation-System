import datetime
import pytz
import textwrap
import os
import re
import requests
from dotenv import load_dotenv

## Load environment variables from .env file
load_dotenv()

# Get current date
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