import requests

def call_api(endpoint, method='get', data=None):
    url = f"http://remove-duplicates-api-330089802.us-east-1.elb.amazonaws.com/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    if method.lower() == 'post' and data:
        response = requests.post(url, json=data, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    
    return response.json()

# Example usage:
if __name__ == "__main__":
    data = {
        "property_number": "4518",
        "property_street": "35th st north",
        "property_city": "arlington",
        "property_state": "va",
        "property_zipcode": "22207"
    }
    result = call_api('check-duplicate', method='post', data=data)
    print(result['is_duplicate'])