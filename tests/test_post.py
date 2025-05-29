import pytest
from fastapi import status
from tests.payloads import get_customer_payloads

class PostTests:
    def __init__(self, client):
        self.client = client
        self.BASE_URL = "/customers"

    def print_result(self, test_name: str, status: str, response: dict = None, error: str = None):
        print(f"\n=== Test: {test_name} ===")
        print(f"Status: {status}")
        if response:
            print(f"Response: {response}")
        if error:
            print(f"Error: {error}")

    def test_post_single_fraud_code_1(self):
        try:
            payload = {"name": "Test User", "city": "Chennai", "country": "India", "fraud_code": 1}
            response = self.client.post(f"{self.BASE_URL}/", json=payload)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["message"] == "Customer created successfully"
            self.print_result("test_post_single_fraud_code_1", "PASSED", response.json())
        except AssertionError as e:
            self.print_result("test_post_single_fraud_code_1", "FAILED", error=str(e))
            raise

    def test_post_single_fraud_code_2(self):
        try:
            payload = {"name": "Test User", "city": "Chennai", "country": "India", "fraud_code": 2}
            response = self.client.post(f"{self.BASE_URL}/", json=payload)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["message"] == "Customer created successfully"
            self.print_result("test_post_single_fraud_code_2", "PASSED", response.json())
        except AssertionError as e:
            self.print_result("test_post_single_fraud_code_2", "FAILED", error=str(e))
            raise

    def test_post_invalid_fraud_code(self):
        try:
            payload = {"name": "Test User", "city": "Chennai", "country": "India", "fraud_code": 3}
            response = self.client.post(f"{self.BASE_URL}/", json=payload)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            assert "detail" in response.json()
            self.print_result("test_post_invalid_fraud_code", "PASSED", response.json())
        except AssertionError as e:
            self.print_result("test_post_invalid_fraud_code", "FAILED", error=str(e))
            raise

    def test_post_multiple_customers(self):
        try:
            payloads = get_customer_payloads()
            for payload in payloads:
                response = self.client.post(f"{self.BASE_URL}/", json=payload.to_dict())
                assert response.status_code == status.HTTP_200_OK
            response = self.client.get(f"{self.BASE_URL}/")
            assert len(response.json()) == 10
            self.print_result("test_post_multiple_customers", "PASSED", {"count": len(response.json())})
        except AssertionError as e:
            self.print_result("test_post_multiple_customers", "FAILED", error=str(e))
            raise