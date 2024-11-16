import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .api.router import router as api_router
from .auth import router as auth_router
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Use allow_origin_regex to match origins starting with "http://localhost:3000"
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://localhost:3000.*$",  # Matches all origins starting with "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)