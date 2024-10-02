import requests
import uuid
from datetime import datetime
from django.utils import timezone


def initiate_payout(amount, phone_number):
    url = "https://api.sandbox.pawapay.cloud/payouts"
    headers = {
        "Authorization": "Bearer eyJraWQiOiIxIiwiYWxnIjoiRVMyNTYifQ.eyJ0dCI6IkFBVCIsInN1YiI6IjI4MjMiLCJleHAiOjIwNDI5MjIzNzMsImlhdCI6MTcyNzM4OTU3MywicG0iOiJEQUYsUEFGIiwianRpIjoiODg4NjliOTktOTA4ZC00YTI4LTlhNGItMmFmMDI0YzU1YTg3In0.DrNUz5xCNjP4NMZmS8686Uh7S8hwZ-repmb3QNFv0w4vn0ysHcuRWdX2PXdhnm7kRrYrIonTiikLDL6Rz-_CPA",  # Use your PawaPay token
        "Content-Type": "application/json"
    }
    
    data = {
        "payoutId": str(uuid.uuid4()),  # Generate a unique UUID for the payout
        "amount": str(amount),  # Payout amount
        "currency": "ZMW",  # Zambian Kwacha
        "country": "ZMB",  # Zambia
        "correspondent": "MTN_MOMO_ZMB",  # Correspondent provider
        "recipient": {
            "type": "MSISDN",  # Mobile number type
            "address": {
                "value": phone_number  # Farmer's phone number
            }
        },
        "customerTimestamp": timezone.now().isoformat() + "Z",  # Current timestamp in ISO format
        "statementDescription": "Payment for agricultural goods"  # Description of the transaction
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # Return JSON response if successful
    else:
        return {"error": response.status_code, "message": response.text}



def initiate_deposit(phone_number, total_price, order_id, customer_email):
    url = "https://api.sandbox.pawapay.cloud/deposits"
    headers = {
        "Authorization": "Bearer eyJraWQiOiIxIiwiYWxnIjoiRVMyNTYifQ.eyJ0dCI6IkFBVCIsInN1YiI6IjI4MjMiLCJleHAiOjIwNDI5MjIzNzMsImlhdCI6MTcyNzM4OTU3MywicG0iOiJEQUYsUEFGIiwianRpIjoiODg4NjliOTktOTA4ZC00YTI4LTlhNGItMmFmMDI0YzU1YTg3In0.DrNUz5xCNjP4NMZmS8686Uh7S8hwZ-repmb3QNFv0w4vn0ysHcuRWdX2PXdhnm7kRrYrIonTiikLDL6Rz-_CPA",
        "Content-Type": "application/json"
    }

    # Generate a unique UUID for the deposit transaction
    deposit_id = str(uuid.uuid4())
    
    data = {
        "depositId": deposit_id,  # Insert generated UUID for deposit
        "amount": str(total_price),  # Amount in ZMW (make sure it's a string)
        "currency": "ZMW",  # Zambian Kwacha
        "country": "ZMB",  # Zambia
        "correspondent": "MTN_MOMO_ZMB",  # Correspondent provider
        "payer": {
            "type": "MSISDN",  # Mobile subscriber number type
            "address": {
                "value": int(phone_number)  # Payer's phone number from the form
            }
        },
        "customerTimestamp": datetime.utcnow().isoformat() + "Z",  # Current timestamp
        "statementDescription": "Payment for goods",  # Transaction statement description
        "preAuthorisationCode": "string",  # Pre-authorization code, if available
        "metadata": [
            {
                "fieldName": "orderId",
                "fieldValue": str(order_id)  # Use the actual order ID
            },
            {
                "fieldName": "customerId",
                "fieldValue": customer_email,  # Use the customer's email from the user
                "isPII": True  # Mark as Personally Identifiable Information (PII)
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Deposit successful:", response)
        return response.json()  # Return JSON response if the request was successful
    else:
        print("Deposit failed:", response)
        return {"error": response.status_code, "message": response.text}
