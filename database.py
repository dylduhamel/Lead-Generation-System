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
     __tablename__ = 'leads'

     id = Column(Integer, primary_key=True)
     owner_name = Column(String(100), unique=True)
     address = Column(String(200))
     document_type = Column(String(50))
     phone_number = Column(String(100))

## Database credentials
db_endpoint = os.getenv('DB_ENDPOINT')
db_name = os.getenv('DB_NAME')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

engine = create_engine(f"mysql+pymysql://{username}:{password}@{db_endpoint}/{db_name}")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)