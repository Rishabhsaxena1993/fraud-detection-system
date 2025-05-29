from pydantic import BaseModel, field_validator

class CustomerCreate(BaseModel):
    name: str
    city: str
    country: str
    fraud_code: int

    @field_validator('fraud_code')
    @classmethod
    def validate_fraud_code(cls, v):
        if v not in [1, 2]:
            raise ValueError('fraud_code must be 1 or 2')
        return v