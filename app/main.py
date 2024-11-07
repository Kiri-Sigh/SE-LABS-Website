import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .api.router import router as api_router
from .auth import router as auth_router
from .database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()


origins = [
    "http://localhost:3000",  # Replace with your frontend origin
    "http://127.0.0.1:8000",  # Replace with your backend origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)