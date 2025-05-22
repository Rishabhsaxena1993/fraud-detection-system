from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from app.models.customer import CustomerCreate, CustomerOut
from app.db.connection import get_connection
from mysql.connector import Error
from app.services.fraud_check import check_fraud
from app.utils.document_ai import verify_document
import os
import shutil

router = APIRouter(prefix="/customers", tags=["customers"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[CustomerOut])
def get_all_customers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers")
        results = cursor.fetchall()
        return results
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/", response_model=dict)
def create_customer(customer: CustomerCreate):
    try:
        if customer.fraud_code not in [1, 2]:
            raise HTTPException(status_code=400, detail="fraud_code must be 1 or 2")
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO customers (name, city, country, fraud_code)
            VALUES (%s, %s, %s, %s)
        """
        data = (customer.name, customer.city, customer.country, customer.fraud_code)
        cursor.execute(query, data)
        conn.commit()
        customer_id = cursor.lastrowid
        return {"message": "Customer added successfully!", "customer_id": customer_id}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/upload")
async def upload_doc(customer_id: int = Form(...), file: UploadFile = File(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        allowed_extensions = [".pdf", ".txt"]
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Only PDF or TXT files allowed")

        file_path = os.path.join(UPLOAD_DIR, f"{customer_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        is_genuine = verify_document(file_path)
        new_fraud_code = 1 if is_genuine else 2
        cursor.execute(
            "UPDATE customers SET fraud_code = %s WHERE id = %s",
            (new_fraud_code, customer_id)
        )
        conn.commit()

        # Fetch updated customer
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        is_fraud = check_fraud(customer)
        return {
            "message": f"File {file.filename} uploaded and saved to {file_path}",
            "fraud_code_updated_to": new_fraud_code,
            "is_fraud": is_fraud
        }
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()