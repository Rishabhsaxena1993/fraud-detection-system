from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Fraud Detection API")

app.include_router(router)

@app.get("/")
def home():
    return {"msg": "Fraud Detection API is Live!"}