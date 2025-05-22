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


def test_get_customers():
    response = client.get(BASE_URL + "/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_post_customer():
    payload = {
        "name": "Test User",
        "city": "Chennai",
        "country": "India",
        "fraud_code": 2
    }
    response = client.post(BASE_URL + "/", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Customer added successfully!"
    assert "customer_id" in response.json()
    # Store customer_id for later use
    pytest.customer_id = response.json()["customer_id"]


@pytest.mark.asyncio
async def test_post_upload(cleanup):
    # Create a customer
    test_post_customer()
    customer_id = pytest.customer_id

    # Create a sample file
    sample_file_path = "tests/sample.txt"
    os.makedirs("tests", exist_ok=True)
    with open(sample_file_path, "w") as f:
        f.write("Test document")

    # Upload file with customer_id
    with open(sample_file_path, "rb") as f:
        response = client.post(
            f"{BASE_URL}/upload",
            data={"customer_id": str(customer_id)},  # Form data expects string
            files={"file": ("sample.txt", f, "text/plain")}
        )

    if response.status_code != 200:
        print(f"Upload Response: {response.json()}")

    assert response.status_code == 200, f"Failed with status {response.status_code}"
    assert "File sample.txt uploaded" in response.json()["message"]
    assert response.json()["fraud_code_updated_to"] in [1, 2]

    if os.path.exists(sample_file_path):
        os.remove(sample_file_path)