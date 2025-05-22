import requests
import os

BASE_URL = "http://127.0.0.1:8000"


def test_post_customer():
    url = f"{BASE_URL}/customers/"
    payload = {
        "name": "Vishal Saxena",
        "city": "Gr Noida",
        "country": "India",
        "fraud_code": 2
    }
    try:
        response = requests.post(url, json=payload)
        print("POST /customers Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
        return response.json().get("customer_id")
    except Exception as e:
        print(f"Error in POST /customers: {e}")
        return None


def test_post_upload(customer_id):
    url = f"{BASE_URL}/customers/upload"
    # Sample file path (apne system pe koi file daal, ya yeh bana le)
    file_path = "test.txt"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("This is a test file.")

    files = {"file": open(file_path, "rb")}
    data = {"customer_id": customer_id}
    try:
        response = requests.post(url, files=files, data=data)
        print("\nPOST /customers/upload Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
    except Exception as e:
        print(f"Error in POST /customers/upload: {e}")


def main():
    # First, add a customer
    customer_id = test_post_customer()
    if customer_id:
        # Then, upload a file for that customer
        test_post_upload(customer_id)

    # Finally, check updated data
    print("\nGET /customers to verify:")
    response = requests.get(f"{BASE_URL}/customers/")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")


if __name__ == "__main__":
    main()