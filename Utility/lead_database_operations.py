from Utility.lead_database import Lead, Session

def add_lead_to_database(lead):
    session = Session()

    try:
        session.add(lead)
        session.commit()
    except Exception as e:
        print(f"Not able to add lead to database. An error has occoured: {e}")
        session.rollback()
    finally:
        session.close()
