import os
import pandas as pd
from sodapy import Socrata
from datetime import datetime, timedelta
from dotenv import load_dotenv

## Load environment variables from .env file
load_dotenv()

# App token for authenticated requests
MyAppToken = os.getenv("CINCI_API_TOKEN")

# Create a client instance
client = Socrata("data.cincinnati-oh.gov",
                 MyAppToken,
                 username=os.getenv("CINCI_API_USERNAME"),
                 password=os.getenv("CINCI_API_PASSWORD"))

# Calculate yesterday's date
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%dT00:00:00.000')

# Make a request to the API and get the results
# Filter results for records with an 'entered_date' from yesterday and limit to 2000 results
results = client.get("cncm-znd6", where="entered_date=2023-05-18T00:00:00.000", limit=2000)

# Convert results into a pandas DataFrame
df = pd.DataFrame.from_records(results)

print(df)

# Select only the desired columns
# df = df[['work_type', 'work_subtype', 'city_id', 'full_address']]

# Convert the DataFrame to a list of dictionaries (for each row)
# records = df.to_dict('records')

# # Print the records
# for record in records:
#     print(record)