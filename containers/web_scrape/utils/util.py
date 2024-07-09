import datetime
import re
import textwrap
import requests
from dotenv import load_dotenv

def call_api(endpoint, method='get', data=None):
    url = f"http://remove-duplicates-api-330089802.us-east-1.elb.amazonaws.com/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    if method.lower() == 'post' and data:
        response = requests.post(url, json=data, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    
    return response.json()

def past_month_date(months_back, current_date):
    date_obj = datetime.datetime.strptime(current_date, "%m/%d/%Y")
    past_date = date_obj - datetime.timedelta(days=months_back*30)
    formatted_date = past_date.strftime("%m/%d/%Y")
    
    return formatted_date

def status_print(message):
    print("*" * 50) 
    for line in textwrap.wrap(message, width=45):
        print("* {: <45}*".format(line))
    print("*" * 50)

def clean_string(input_string):
    formatted_name = input_string.strip().upper()
    formatted_name = re.sub(r'\s+', ' ', formatted_name)
    
    return formatted_name