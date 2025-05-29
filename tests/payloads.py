from dataclasses import dataclass
from typing import List

@dataclass
class CustomerPayload:
    name: str
    city: str
    country: str
    fraud_code: int

    def to_dict(self):
        return {
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "fraud_code": self.fraud_code
        }

def get_customer_payloads() -> List[CustomerPayload]:
    return [
        CustomerPayload("Amit Tripathi", "Mumbai", "India", 1),
        CustomerPayload("Priya Singh", "Delhi", "India", 2),
        CustomerPayload("Rahul Verma", "Bangalore", "India", 1),
        CustomerPayload("Sneha Patel", "Ahmedabad", "India", 2),
        CustomerPayload("Vikram Rao", "Chennai", "India", 1),
        CustomerPayload("Anjali Gupta", "Kolkata", "India", 2),
        CustomerPayload("Rohit Kumar", "Hyderabad", "India", 1),
        CustomerPayload("Neha Desai", "Pune", "India", 2),
        CustomerPayload("Hardik Pandya", "Jaipur", "India", 1),
        CustomerPayload("Kavita Joshi", "Lucknow", "India", 2)
    ]

def get_invalid_customer_payloads() -> List[CustomerPayload]:
    return [
        CustomerPayload("", "Mumbai", "India", 1),  # Empty name (invalid)
        CustomerPayload("Amit Tripathi", "Mumbai", "India", 999),  # Invalid fraud_code
        CustomerPayload("Sneha Patel", "", "India", 2),  # Empty city
    ]