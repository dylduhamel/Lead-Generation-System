from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OwnerLead(Base):
     __tablename__ = 'owner_leads'

     id = Column(Integer, primary_key=True)
     owner_name = Column(String(100), unique=True)
     home_style = Column(String(50))
     address = Column(String(200))

# Replace the following with your own details
db_endpoint = "test.cynbkamcrdki.eu-north-1.rds.amazonaws.com"
db_name = "acuritas_test"
username = "admin"
password = "Acuritas1"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{db_endpoint}/{db_name}")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
