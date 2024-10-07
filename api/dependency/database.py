import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Load environment variables
load_dotenv()

# Load the database URL from the environment variable
URL_DATABASE = os.getenv("URL_DATABASE")

if URL_DATABASE is None:
    raise ValueError("No database URL found. Please set the URL_DATABASE environment variable.")

try:
    # Create the SQLAlchemy engine
    engine = create_async_engine(URL_DATABASE, pool_pre_ping=True, echo=True)

    # Create a session local class
    AsyncSessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

    # Create a declarative base class
    class Base(DeclarativeBase):
        pass

except SQLAlchemyError as e:
    raise RuntimeError(f"Failed to initialize database: {str(e)}")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session