from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "PayAssist Payment Backend is running"
    }
from pydantic import BaseModel
import random

class PaymentRequest(BaseModel):
    payment_type: str
    payment_method: str
    amount: float


@app.post("/payment/create")
def create_payment(payment: PaymentRequest):
    transaction_id = "TXN" + str(random.randint(10000, 99999))

    return {
        "transaction_id": transaction_id,
        "status": "SUCCESS",
        "payment_type": payment.payment_type,
        "payment_method": payment.payment_method,
        "amount": payment.amount
    }