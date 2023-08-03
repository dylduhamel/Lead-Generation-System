import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_property_sales_from_url(url):
    # make a GET request to the website
    response = requests.get(url)
    # parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # find the table on the webpage
    table = soup.find('table')

    # create a list to store our table rows
    rows = []

    # iterate over the table rows
    for row in table.find_all('tr'):
        # get the HTML for each row
        row_html = row.prettify()

        # create a BeautifulSoup object for each row
        row_soup = BeautifulSoup(row_html, 'html.parser')

        # find all 'td' tags (table data) in the row
        td_tags = row_soup.find_all('td')

        # if the length of td_tags is not 0
        if len(td_tags) > 0:
            # iterate over the 'td' tags
            for tag in td_tags:
                # append the text of each tag to our row list
                rows.append(tag.text)

    # transform the list into a dataframe
    df = pd.DataFrame(rows)

    # convert the dataframe to json
    json_data = df.to_json(orient="records")

    # return the json data
    return json_data

# test the function
url = "https://www.hcso.org/community-services/search-property-sales/property-sales/"
json_data = get_property_sales_from_url(url)
print(json_data)
