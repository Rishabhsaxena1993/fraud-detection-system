import pytest
from fastapi import status
from tests.payloads import get_customer_payloads

class GetTests:
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

    def test_get_customer(self):
        try:
            payload = {"name": "Ajay", "city": "Saxena", "country": "USA", "fraud_code": 1}
            post_response = self.client.post(f"{self.BASE_URL}/", json=payload)
            assert post_response.status_code == status.HTTP_200_OK
            customer_id = post_response.json()["id"]
            response = self.client.get(f"{self.BASE_URL}/{customer_id}")
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["name"] == "Ajay"
            self.print_result("test_get_customer", "PASSED", response.json())
        except AssertionError as e:
            self.print_result("test_get_customer", "FAILED", error=str(e))
            raise

    def test_get_customer_invalid_id(self):
        try:
            response = self.client.get(f"{self.BASE_URL}/9999")
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert response.json()["detail"] == "Customer not found"
            self.print_result("test_get_customer_invalid_id", "PASSED", response.json())
        except AssertionError as e:
            self.print_result("test_get_customer_invalid_id", "FAILED", error=str(e))
            raise

    def test_get_invalid_endpoint(self):
        try:
            response = self.client.get(f"{self.BASE_URL}/invalid")
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            assert "detail" in response.json()
            self.print_result("test_get_invalid_endpoint", "PASSED", response.json())
        except AssertionError as e:
            self.print_result("test_get_invalid_endpoint", "FAILED", error=str(e))
            raise

    def test_get_customers_valid_endpoint(self):
        try:
            payloads = get_customer_payloads()
            for payload in payloads:
                self.client.post(f"{self.BASE_URL}/", json=payload.to_dict())
            response = self.client.get(f"{self.BASE_URL}/")
            assert response.status_code == status.HTTP_200_OK
            assert len(response.json()) == 10  # 10 payloads
            self.print_result("test_get_customers_valid_endpoint", "PASSED", {"count": len(response.json())})
        except AssertionError as e:
            self.print_result("test_get_customers_valid_endpoint", "FAILED", error=str(e))
            raise

    def test_get_list_of_records_and_print(self):
        try:
            payloads = get_customer_payloads()[:2]
            for payload in payloads:
                self.client.post(f"{self.BASE_URL}/", json=payload.to_dict())
            response = self.client.get(f"{self.BASE_URL}/")
            assert response.status_code == status.HTTP_200_OK
            assert len(response.json()) >= 2
            self.print_result("test_get_list_of_records_and_print", "PASSED", response.json())
        except AssertionError as e:
            self.print_result("test_get_list_of_records_and_print", "FAILED", error=str(e))
            raise

    def test_get_list_of_duplicate_records(self):
        try:
            payloads = get_customer_payloads()[:2]
            for payload in payloads * 2:  # Insert duplicates
                self.client.post(f"{self.BASE_URL}/", json=payload.to_dict())
            from app.db.connection import get_connection
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT name, city, country, fraud_code, COUNT(*) as count
                FROM customers
                GROUP BY name, city, country, fraud_code
                HAVING count > 1
            """
            cursor.execute(query)
            duplicates = cursor.fetchall()
            assert len(duplicates) == 2  # 2 duplicate groups
            self.print_result("test_get_list_of_duplicate_records", "PASSED", {"duplicates": len(duplicates)})
            cursor.close()
            conn.close()
        except AssertionError as e:
            self.print_result("test_get_list_of_duplicate_records", "FAILED", error=str(e))
            raise

    def test_get_users_fraud_code_1(self):
        try:
            payload = {"name": "Test User", "city": "Chennai", "country": "India", "fraud_code": 1}
            self.client.post(f"{self.BASE_URL}/", json=payload)
            from app.db.connection import get_connection
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers WHERE fraud_code = 1")
            users = cursor.fetchall()
            assert len(users) >= 1
            self.print_result("test_get_users_fraud_code_1", "PASSED", {"count": len(users)})
            cursor.close()
            conn.close()
        except AssertionError as e:
            self.print_result("test_get_users_fraud_code_1", "FAILED", error=str(e))
            raise

    def test_get_users_fraud_code_2(self):
        try:
            payload = {"name": "Test User", "city": "Chennai", "country": "India", "fraud_code": 2}
            self.client.post(f"{self.BASE_URL}/", json=payload)
            from app.db.connection import get_connection
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM customers WHERE fraud_code = 2")
            users = cursor.fetchall()
            assert len(users) >= 1
            self.print_result("test_get_users_fraud_code_2", "PASSED", {"count": len(users)})
            cursor.close()
            conn.close()
        except AssertionError as e:
            self.print_result("test_get_users_fraud_code_2", "FAILED", error=str(e))
            raise