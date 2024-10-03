import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

# Load the database URL from the environment variable
URL_DATABASE = os.getenv("URL_DATABASE")

# Check if the URL_DATABASE is loaded correctly
if URL_DATABASE is None:
    raise ValueError(
        "No database URL found. Please set the URL_DATABASE environment variable.")

# Create the SQLAlchemy engine
engine = create_engine(URL_DATABASE)

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class


class Base(DeclarativeBase):
    pass
