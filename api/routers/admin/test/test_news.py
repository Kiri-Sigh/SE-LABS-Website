from fastapi.testclient import TestClient
from ..news import router

client = TestClient(router)