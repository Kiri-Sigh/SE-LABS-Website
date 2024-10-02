# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
# from sqlalchemy.ext.declarative import declarative_base

# # Load environment variables
# load_dotenv()

# # Get database URL
# DATABASE_URL = os.getenv("URL_DATABASE")

# # Create engine
# engine = create_engine(DATABASE_URL)

# # Create declarative base
# Base = declarative_base()

# # Define a simple model
# class TestModel(Base):
#     __tablename__ = 'test_table'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))

# def create_tables():
#     Base.metadata.create_all(engine)
#     print("Tables created successfully.")

# def check_table_exists():
#     metadata = MetaData()
#     metadata.reflect(bind=engine)
#     if 'test_table' in metadata.tables:
#         print("Test table exists in the database.")
#     else:
#         print("Test table does not exist in the database.")

# if __name__ == "__main__":
#     try:
#         create_tables()
#         check_table_exists()
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")