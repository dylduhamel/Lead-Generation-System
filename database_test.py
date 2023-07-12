from database import Lead, Session
from owner_info import Owner

session = Session()

def store_data():
    owner = Owner(name="ddd", address="123")
    with Session() as session:
        new_home = Lead(owner_name=owner.name, address=owner.address, document_type=owner.doc_type, phone_number=owner.phone_number)
        session.add(new_home)
        session.commit()

store_data()
