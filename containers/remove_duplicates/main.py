from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from pymysql.cursors import DictCursor
from postal.parser import parse_address
from contextlib import closing

app = FastAPI()


# Pydantic models for data validation
class AddressData(BaseModel):
    full_address: str


class PropertyData(BaseModel):
    property_number: str
    property_street: str
    property_city: str
    property_state: str
    property_zipcode: str


# Endpoint to parse addresses
@app.post("/parse", response_model=dict)
def parse_address_endpoint(data: AddressData):
    parsed = parse_address(data.full_address)
    address_dict = {label: value for value, label in parsed}
    # Convert state to lowercase abbreviation if needed, here simplified
    if "state" in address_dict:
        address_dict["state"] = address_dict["state"][:2].lower()
    return address_dict


# Endpoint to check for duplicates
@app.post("/check-duplicate")
def check_duplicate(data: PropertyData):
    connection = pymysql.connect(
        host="your-rds-host",
        user="username",
        password="password",
        database="dbname",
        cursorclass=DictCursor,
    )
    try:
        with closing(connection):
            with connection.cursor() as cursor:
                sql = """
                SELECT lead_id FROM lead WHERE
                property_number = %s AND
                property_street = %s AND
                property_city = %s AND
                property_state = %s AND
                property_zipcode = %s
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
                connection.commit()  # Important to release the lock
                if result:
                    return {"is_duplicate": True, "lead_id": result["lead_id"]}
                else:
                    return {"is_duplicate": False, "lead_id": None}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
