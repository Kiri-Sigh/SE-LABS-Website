from fastapi.testclient import TestClient
from ..research import router

client = TestClient(router)