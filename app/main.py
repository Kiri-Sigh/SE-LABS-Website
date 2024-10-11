from fastapi import FastAPI
from .api.router import router as api_router
from .auth import router as auth_router
from .database import Base, engine

app = FastAPI()

app.include_router(api_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)