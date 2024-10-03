from fastapi.testclient import TestClient
from ..event import router

client = TestClient(router)
