from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()


# Home / Test API
@app.get("/")
def home():
    return {
        "message": "PayAssist Payment Backend is running"
    }


# Payment Request Model
class PaymentRequest(BaseModel):
    payment_type: str
    payment_method: str
    amount: float


# Create Payment API
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


# Dialogflow Webhook
@app.post("/webhook")
def webhook(request: dict):
    query_result = request.get("queryResult", {})
    parameters = query_result.get("parameters", {})

    payment_type = parameters.get("payment_type")
    payment_method = parameters.get("payment_method")
    amount = parameters.get("amount")

    transaction_id = "TXN" + str(random.randint(10000, 99999))

    return {
        "fulfillmentText": (
            f"Payment successful. Your transaction ID is {transaction_id}. "
            f"You paid {amount} for {payment_type} using {payment_method}."
        )
    }
