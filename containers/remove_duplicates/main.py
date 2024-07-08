from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import IntegrityError
from postal.parser import parse_address
from contextlib import closing
from util.mappings import state_abbreviation_mapping, street_type_mapping
from util.get_env import get_secret

app = FastAPI()
env = get_secret("prod/lead_scraper/db")


# Pydantic models for data validation
class AddressData(BaseModel):
    full_address: str


class PropertyData(BaseModel):
    property_number: str
    property_street: str
    property_city: str
    property_state: str
    property_zipcode: str

@app.get("/health")
def health_check():
    return {"status": "ok"}
    
# Endpoint to parse addresses
@app.post("/parse", response_model=dict)
def parse_address_endpoint(data: AddressData):
    """
    Parses a full address into its constituent components using the libpostal library.

    This endpoint accepts a full address string, and utilizes the libpostal library to break
    the address down into components such as street name, city, state, and zip code.

    Args:
        data (AddressData): A Pydantic model that includes a single field 'full_address'.

    Returns:
        dict: A dictionary with keys representing address components (e.g., 'road', 'city', 'state')
        and values being the corresponding parsed elements from the input address.

    Example:
        POST /parse
        {
          "full_address": "1234 30th Street, Richmond, VA, 10000"
        }

        Returns:
        {
            'house_number': '1234',
            'road': '30th st',
            'city': 'richmond',
            'state': 'virginia',
            'postcode': '10000'
        }

    """
    parsed = parse_address(data.full_address)
    address_dict = {label: value for value, label in parsed}

    # Canonicalization of street and state token
    if "road" in address_dict:
        address_dict["road"] = " ".join(
            street_type_mapping.get(part, part) for part in address_dict["road"].split()
        )

    if "state" in address_dict:
        address_dict["state"] = state_abbreviation_mapping.get(
            address_dict["state"], address_dict["state"]
        )

    return address_dict


@app.post("/check-duplicate")
def check_duplicate(data: PropertyData):
    """
    Checks if a given property is already listed in the database based on its address components.

    If a duplicate is found, it returns a JSON indicating so, along with the lead_id of the existing entry.
    If no duplicate is found, it indicates this as well, returning a lead_id of None.

    Args:
        data (PropertyData): A Pydantic model that defines the required fields for the property
        being checked (property_number, property_street, property_city, property_state, property_zipcode).

    Returns:
        dict: A dictionary indicating whether the property is a duplicate, and if so, the ID of the
        existing lead. If not a duplicate, 'lead_id' will be None.

    Example:
        POST /check-duplicate
        {
          "property_number": "123",
          "property_street": "Main St",
          "property_city": "Anytown",
          "property_state": "CA",
          "property_zipcode": "12345"
        }

        Returns:
        {
          "is_duplicate": true,
          "lead_id": "abc123"
        }
    """
    connection = pymysql.connect(
        host=env["host"],
        user=env["username"],
        password=env["password"],
        database="LEAD_DB",
        cursorclass=DictCursor,
    )
    try:
        with closing(connection):
            with connection.cursor() as cursor:
                sql = """
                SELECT LEAD_ID FROM `LEAD` WHERE
                PROPERTY_NUMBER = %s AND
                PROPERTY_STREET = %s AND
                PROPERTY_CITY = %s AND
                PROPERTY_STATE = %s AND
                PROPERTY_ZIPCODE = %s
                FOR UPDATE
                """
                cursor.execute(
                    sql,
                    (
                        data.property_number,
                        data.property_street,
                        data.property_city,
                        data.property_state,
                        data.property_zipcode,
                    ),
                )
                result = cursor.fetchone()
                connection.commit() 
                if result:
                    return {"is_duplicate": True, "lead_id": result["LEAD_ID"]}
                else:
                    return {"is_duplicate": False, "lead_id": None}
    except IntegrityError as e:
        connection.rollback()
        raise HTTPException(
            status_code=409, detail="Duplicate entry for property detected."
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=501, detail=str(e))
