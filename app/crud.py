from fastapi import HTTPException

from app.db.connection import get_connection
from app.schemas import CustomerCreate


def create_customer(customer: CustomerCreate):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO customers (name, city, country, fraud_code) VALUES (%s, %s, %s, %s)"
        values = (customer.name, customer.city, customer.country, customer.fraud_code)
        cursor.execute(query, values)
        conn.commit()
        customer_id = cursor.lastrowid
        return customer_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
