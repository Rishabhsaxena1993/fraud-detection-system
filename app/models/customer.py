from pydantic import BaseModel
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    city: Optional[str] = None
    country: Optional[str] = None
    fraud_code: int

class CustomerOut(CustomerCreate):
    id: int

    class Config:
        from_attributes = True  # Changed from orm_mode