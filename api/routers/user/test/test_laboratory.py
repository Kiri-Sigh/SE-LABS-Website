from fastapi.testclient import TestClient
from ..laboratory import router

client = TestClient(router)