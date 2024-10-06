import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables
load_dotenv()

# Load the database URL from the environment variable
URL_DATABASE = os.getenv("URL_DATABASE")

if URL_DATABASE is None:
    raise ValueError("No database URL found. Please set the URL_DATABASE environment variable.")

try:
    # Create the SQLAlchemy engine
    engine = create_engine(URL_DATABASE, pool_pre_ping=True)

    # Create a session local class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a declarative base class
    class Base(DeclarativeBase):
        pass

except SQLAlchemyError as e:
    raise RuntimeError(f"Failed to initialize database: {str(e)}")

def get_db():
    """
    Generator function to get a database session.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()