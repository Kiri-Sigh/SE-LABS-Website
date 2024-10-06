from ..database.database import SessionLocal

def get_db():
    # Create a new database session
    db = SessionLocal()
    try:
        # Yield the database session
        yield db
    finally:
        # Ensure the database session is closed after the request is finished
        db.close()