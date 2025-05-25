from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.customer import CustomerCreate
from app.db.connection import get_connection
from app.services.fraud_check import check_fraud
import os
import shutil

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/")
def get_customers():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.post("/")
def add_customer(customer: CustomerCreate):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO customers (name, city, country, fraud_code) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (customer.name, customer.city, customer.country, customer.fraud_code))
        conn.commit()
        customer_id = cursor.lastrowid
        return {"message": "Customer added successfully!", "customer_id": customer_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.post("/upload")
def upload_file(customer_id: str = Form(...), file: UploadFile = File(...)):
    conn = None
    cursor = None
    try:
        if not file.filename.endswith((".txt", ".pdf")):
            raise HTTPException(status_code=400, detail="Only PDF or TXT files allowed")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = %s", (int(customer_id),))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Customer not found")
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        try:
            is_fraud = check_fraud(file_path)
        except Exception as fraud_error:
            raise HTTPException(status_code=500, detail=f"Fraud check failed: {str(fraud_error)}")
        fraud_code = 2 if is_fraud else 1
        cursor.execute("UPDATE customers SET fraud_code = %s WHERE id = %s", (fraud_code, int(customer_id)))
        conn.commit()
        return {"message": f"File {file.filename} uploaded", "is_fraud": is_fraud, "fraud_code_updated_to": fraud_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Customer not found")
        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        conn.commit()
        return {"message": "Customer deleted successfully"}
    except HTTPException as e:
        raise e  # Re-raise 404
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete error: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()