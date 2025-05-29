from fastapi import FastAPI
from app.routes import customer

app = FastAPI()

app.include_router(customer.router)

@app.get("/")
def home():
    return {"msg": "Fraud Detection API is Live!"}