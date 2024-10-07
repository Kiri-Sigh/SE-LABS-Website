import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("URL_DATABASE")
if not DATABASE_URL:
    raise ValueError("No database URL found. Please set the DATABASE_URL environment variable.")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Function to initialize the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)