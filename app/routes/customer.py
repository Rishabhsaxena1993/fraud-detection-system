from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.customer import CustomerCreate
from app.db.connection import get_connection
from app.services.fraud_check import check_fraud
import os

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/{customer_id}")
def get_customer(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    finally:
        cursor.close()
        conn.close()

@router.get("/")
def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        return customers
    finally:
        cursor.close()
        conn.close()

@router.post("/")
def create_customer(customer: CustomerCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO customers (name, city, country, fraud_code) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (customer.name, customer.city, customer.country, customer.fraud_code))
        conn.commit()
        customer_id = cursor.lastrowid
        return {"message": "Customer created successfully", "id": customer_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/upload")
async def upload_document(customer_id: str = Form(...), file: UploadFile = File(...)):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        customer_id = int(customer_id)  # Convert to int
        upload_dir = "tests/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        is_fraud = check_fraud(file_path)
        fraud_code = 2 if is_fraud else 1
        cursor.execute("UPDATE customers SET fraud_code = %s WHERE id = %s", (fraud_code, customer_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
        conn.commit()
        return {"is_fraud": is_fraud, "fraud_code_updated_to": fraud_code}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid customer_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()