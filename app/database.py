import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

URL_DATABASE = os.getenv("URL_DATABASE")

if URL_DATABASE is None:
    raise ValueError(
        "No database URL found. Please set the URL_DATABASE environment variable.")

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

