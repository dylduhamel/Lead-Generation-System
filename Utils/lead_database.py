import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

## Load environment variables from .env file
load_dotenv()

Base = declarative_base()

## Database structure
class Lead(Base):
     # The name of the database
     __tablename__ = 'leads'

     id = Column(Integer, primary_key=True)
     date_added = Column(String(199))
     owner_name = Column(String(100), unique=True)
     property_address = Column(String(200))
     property_city = Column(String(200))
     property_state = Column(String(200))
     property_zipcode = Column(String(200))
     document_type = Column(String(50))
     document_subtype = Column(String(50))
     phone_number_1 = Column(String(100))
     phone_number_1_type = Column(String(100))
     phone_number_2 = Column(String(100))
     phone_number_2_type = Column(String(100))
     email = Column(String(200))

     # Printing representation for testing
     def __repr__(self):
        return (f"Lead(document_type={self.document_type}, "
                f"document_subtype={self.document_subtype}, "
                f"property_address={self.property_address}, "
                f"property_city={self.property_city}, "
                f"property_state={self.property_state}, "
                f"property_zipcode={self.property_zipcode}, "
                f"phone_number_1={self.phone_number_1}, "
                f"phone_number_1_type={self.phone_number_1_type}, "
                f"phone_number_2={self.phone_number_2}, "
                f"phone_number_2_type={self.phone_number_2_type}, "
                f"email={self.email})")

## Database credentials
db_endpoint = os.getenv('DB_ENDPOINT')
db_name = os.getenv('DB_NAME')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

engine = create_engine(f"mysql+pymysql://{username}:{password}@{db_endpoint}/{db_name}")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)