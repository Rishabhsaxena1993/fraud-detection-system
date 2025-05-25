import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import app
import os
import pytest_asyncio

client = TestClient(app)
BASE_URL = "/customers"

@pytest_asyncio.fixture
async def cleanup():
    yield
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        for file in os.listdir(upload_dir):
            os.remove(os.path.join(upload_dir, file))
        if not os.listdir(upload_dir):
            os.rmdir(upload_dir)

@pytest.fixture
def customer_id():
    payload = {
        "name": "Test User",
        "city": "Chennai",
        "country": "India",
        "fraud_code": 2
    }
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 200
    return response.json()["customer_id"]

def test_get_customers():
    response = client.get(BASE_URL + "/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_customer():
    payload = {
        "name": "Rahul Sharma",
        "city": "Delhi",
        "country": "India",
        "fraud_code": 1
    }
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Customer added successfully!"

@pytest.mark.asyncio
async def test_post_upload_document(cleanup, customer_id):
    sample_file_path = "tests/sample.txt"
    os.makedirs("tests", exist_ok=True)
    with open(sample_file_path, "w") as f:
        f.write("Test document")
    with open(sample_file_path, "rb") as f:
        response = client.post(
            f"{BASE_URL}/upload",
            data={"customer_id": str(customer_id)},
            files={"file": ("sample.txt", f, "text/plain")}
        )
    assert response.status_code == 200

def test_delete_customer(customer_id):
    response = client.delete(f"{BASE_URL}/{customer_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted successfully"

def test_delete_invalid_customer():
    response = client.delete(f"{BASE_URL}/9999")
    assert response.status_code == 404