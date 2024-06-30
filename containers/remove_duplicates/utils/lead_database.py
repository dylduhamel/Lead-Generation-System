import os

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

## Load environment variables from .env file
load_dotenv()

Base = declarative_base()

## Database structure
class Lead(Base):
    # The name of the database
    __tablename__ = "LEAD"

    lead_id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=func.current_timestamp()) 
    first_name_owner = Column(String(45))
    last_name_owner = Column(String(45))
    property_address = Column(String(45))
    property_city = Column(String(45))
    property_state = Column(String(45))
    property_zipcode = Column(String(20))
    document_type = Column(String(250))
    document_subtype = Column(String(45))
    phone_number_1 = Column(String(20))
    phone_number_1_type = Column(String(20))
    phone_number_2 = Column(String(20))
    phone_number_2_type = Column(String(20))
    email = Column(String(20))
    county_website = Column(String(255))

    # Printing representation for testing
    def __repr__(self):
        return (
            f"Lead(date_added={self.date_added}, "
            f"first_name_owner={self.first_name_owner}, "
            f"last_name_owner={self.last_name_owner}, "
            f"document_type={self.document_type}, "
            f"document_subtype={self.document_subtype}, "
            f"property_address={self.property_address}, "
            f"property_city={self.property_city}, "
            f"property_state={self.property_state}, "
            f"property_zipcode={self.property_zipcode}, "
            f"phone_number_1={self.phone_number_1}, "
            f"phone_number_1_type={self.phone_number_1_type}, "
            f"phone_number_2={self.phone_number_2}, "
            f"phone_number_2_type={self.phone_number_2_type}, "
            f"email={self.email}, "
            f"county_website={self.county_website})"
        )


## Database credentials
db_endpoint = os.getenv("DB_ENDPOINT")
db_name = os.getenv("DB_NAME")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

engine = create_engine(f"mysql+pymysql://{username}:{password}@{db_endpoint}/{db_name}")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
