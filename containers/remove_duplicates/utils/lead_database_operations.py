import csv
import json
import logging
import pandas as pd
from sqlalchemy import update, text, or_
from utils import *
from utils.util import status_print

logging.basicConfig(filename="processing.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

def remove_duplicates():
    # Initialize the session
    session = Session()

    # Query to find duplicate rows
    query = f"""
    DELETE t1 FROM LEAD_DB.LEAD t1
    INNER JOIN LEAD_DB.LEAD t2 
    WHERE t1.LEAD_ID > t2.LEAD_ID AND t1.PROPERTY_ADDRESS = t2.PROPERTY_ADDRESS
    """

    # Execute the DELETE query
    session.execute(text(query))

    # Commit the changes
    session.commit()

    status_print("Duplicates removed successfully.")