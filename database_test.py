from database import Lead, Session
from owner_info import Owner

session = Session()

def store_data():
    try:
        # Create a new Lead
        new_lead = Lead(
            owner_name='John Doe',
            property_address='123 Main St',
            property_city='Anytown',
            property_state='Anystate',
            property_zipcode='12345',
            document_type='Type1',
            phone_number_1='123-456-7890',
            phone_number_1_type='mobile',
            phone_number_2='098-765-4321',
            phone_number_2_type='home',
            email='johndoe@example.com',
        )

        # Add the new Lead to the session
        session.add(new_lead)

        # Commit the session to write the data to the database
        session.commit()

    except Exception as e:
        # An error occurred, handle it in whatever way is appropriate for your situation
        print(f"An error occurred: {e}")
        session.rollback()  # Roll back the transaction in case of error

    finally:
        # Ensure the session is closed when we're done with it
        session.close()

store_data()
