import pytest
import os
from fastapi import status

class UploadTests:
    def __init__(self, client):
        self.client = client
        self.BASE_URL = "/customers"

    def print_result(self, test_name: str, status: str, response: dict = None, error: str = None):
        print(f"\n=== Test: {test_name} ===")
        print(f"Status: {status}")
        if response:
            print(f"Response: {response}")
        if error:
            print(f"Error: {str(error)}")

    @pytest.fixture(autouse=True)
    def cleanup_uploads(self):
        yield
        upload_dir = "tests/uploads"
        if os.path.exists(upload_dir):
            for file in os.listdir(upload_dir):
                os.remove(os.path.join(upload_dir, file))
            if not os.listdir(upload_dir):
                os.rmdir(upload_dir)

    def test_post_upload_document(self):
        try:
            payload = {"name": "Test User", "city": "Chennai", "country": "India", "fraud_code": 1}
            post_response = self.client.post(f"{self.BASE_URL}/", json=payload)
            assert post_response.status_code == status.HTTP_200_OK
            customer_id = post_response.json()["id"]

            sample_file_path = "tests/sample.txt"
            os.makedirs("tests", exist_ok=True)
            with open(sample_file_path, "w") as f:
                f.write("fraud document")
            with open(sample_file_path, "rb") as f:
                response = self.client.post(
                    f"{self.BASE_URL}/upload",
                    data={"customer_id": str(customer_id)},
                    files={"file": ("sample.txt", f, "text/plain")}
                )
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["is_fraud"] is True
            self.print_result("test_post_upload_document", "PASSED", response.json())
        except AssertionError as e:
            self.print_result("test_post_upload_document", "FAILED", error=str(e))
            raise