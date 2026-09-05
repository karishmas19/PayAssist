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

    # Get parameters directly
    parameters = query_result.get("parameters", {})

    # Get parameters from Dialogflow context
    output_contexts = query_result.get("outputContexts", [])

    for context in output_contexts:
        context_parameters = context.get("parameters", {})

        if context_parameters:
            if context_parameters.get("payment_type"):
                parameters = context_parameters
                break

    payment_type = parameters.get("payment_type")
    payment_method = parameters.get("payment_method")
    amount = parameters.get("amount")

    # Generate mock transaction ID
    transaction_id = "TXN" + str(random.randint(10000, 99999))

    # Send response back to Dialogflow
    return {
        "fulfillmentText": (
            f"Payment successful. "
            f"Your transaction ID is {transaction_id}. "
            f"You paid {amount} for {payment_type} "
            f"using {payment_method}."
        )
    }
