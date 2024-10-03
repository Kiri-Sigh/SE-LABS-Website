from fastapi.testclient import TestClient
from ..publication import router

client = TestClient(router)