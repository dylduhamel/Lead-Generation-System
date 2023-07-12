import pandas as pd
import numpy as np
import logging

class LeeCountyEnf():
    def __init__(self):
        # Set up logging
        logging.basicConfig(filename='processing.log', level=logging.INFO)
        
        self.read_file = input("Enter file to be used (include.csv)")
        self.read_file = r'C:\Users\Jake\Documents\LISTS\\' + self.read_file 

        # List of keywords to search for
        self.keywords = ["Nuisance Accumulation", "junk", "trash", "lot mow", "plywood", "Inoperable", 
                    "tents", "tires", "Abandoned", "boat", "Overgrown grass", "debris", 
                    "vacant", "damaged roof", "damage", "parts"]

        # List of keywords to exclude
        self.exclusions = ["Permit", "construction", "GVWR", "Builder", "commercial"]
    
    def start(self):
        try:
            # Load the csv file into a DataFrame
            df = pd.read_csv(self.read_file)
        except Exception as e:
            logging.error(f"Failed to load CSV file: {e}")
            exit()

        # Convert the Description to lowercase for case-insensitive matching 
        df['Description'] = df['Description'].str.lower()

        # Handle empty or missing values
        df = df.dropna(subset=['Address', 'Description'])

        # Create a new DataFrame to hold rows where a keyword is found
        selected_rows = pd.DataFrame(columns=df.columns)

        for keyword in self.keywords:
            keyword_rows = df[df['Description'].str.contains(keyword.lower())]
            selected_rows = pd.concat([selected_rows, keyword_rows])
            
        # Remove rows where an exclusion keyword is found
        for exclusion in self.exclusions:
            selected_rows = selected_rows[~selected_rows['Description'].str.contains(exclusion.lower())]

        # Split the 'Address' field into separate 'Address', 'City_State_Zip' fields
        selected_rows[['Address', 'City_State_Zip']] = selected_rows['Address'].str.split(',', n=1, expand=True)

        # Split the 'City_State_Zip' field into separate 'City', 'State_Zip' fields
        selected_rows[['City', 'State_Zip']] = selected_rows['City_State_Zip'].str.split(' FL', n=1, expand=True)

        # Split the 'State_Zip' field into separate 'State', 'Zip' fields
        selected_rows[['State', 'Zip']] = selected_rows['State_Zip'].str.split(' ', n=1, expand=True)

        # Remove unnecessary columns
        selected_rows = selected_rows.drop(columns=['Record Number', 'Status', 'Related Records', 'City_State_Zip', 'State_Zip'])

        # Populate 'State' column with 'FL'
        selected_rows['State'] = 'FL'

        # Reorder the columns
        selected_rows = selected_rows[['Address', 'City', 'State', 'Zip', 'Description']]

        # Save the selected rows to a new CSV file
        file_name = input("ENTER file name (include .csv): ")
        file_path = r'C:\Users\Jake\Documents\LISTS\\' + file_name

        # Remove duplicates based on 'Address'
        selected_rows = selected_rows.drop_duplicates(subset='Address')

        selected_rows.to_csv(file_path , index=False)

        
