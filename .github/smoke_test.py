# Checks that the backend starts and its APIs answer, without signing in.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

response = client.get("/api/get-account")
assert response.status_code == 401, response.text

response = client.get("/toLogin")
assert "/login/oauth/authorize?client_id=" in response.text, response.text

response = client.post("/api/signin?code=invalid&state=state")
assert response.json()["status"] == "error", response.text

response = client.post("/api/signout")
assert response.json()["status"] == "ok", response.text

print("ok")
