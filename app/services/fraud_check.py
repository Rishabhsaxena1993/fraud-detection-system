def check_fraud(customer_data: dict) -> bool:
    fraud_code = customer_data.get("fraud_code", 2)
    return fraud_code == 2