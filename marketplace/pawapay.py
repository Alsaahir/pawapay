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
        "payoutId": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "ZMW",
        "country": "ZMB",
        "correspondent": "MTN_MOMO_ZMB",
        "recipient": {
            "type": "MSISDN",
            "address": {
                "value": phone_number
            }
        },
        "customerTimestamp": timezone.now().isoformat() + "Z",
        "statementDescription": "Payment for agricultural goods"
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}



def initiate_deposit(phone_number, total_price, order_id, customer_email):
    url = "https://api.sandbox.pawapay.cloud/deposits"
    headers = {
        "Authorization": "Bearer eyJraWQiOiIxIiwiYWxnIjoiRVMyNTYifQ.eyJ0dCI6IkFBVCIsInN1YiI6IjI4MjMiLCJleHAiOjIwNDI5MjIzNzMsImlhdCI6MTcyNzM4OTU3MywicG0iOiJEQUYsUEFGIiwianRpIjoiODg4NjliOTktOTA4ZC00YTI4LTlhNGItMmFmMDI0YzU1YTg3In0.DrNUz5xCNjP4NMZmS8686Uh7S8hwZ-repmb3QNFv0w4vn0ysHcuRWdX2PXdhnm7kRrYrIonTiikLDL6Rz-_CPA",
        "Content-Type": "application/json"
    }

    deposit_id = str(uuid.uuid4())
    
    data = {
        "depositId": deposit_id,
        "amount": str(total_price),
        "currency": "ZMW",
        "country": "ZMB",
        "correspondent": "MTN_MOMO_ZMB",
        "payer": {
            "type": "MSISDN",
            "address": {
                "value": int(phone_number)
            }
        },
        "customerTimestamp": datetime.utcnow().isoformat() + "Z",
        "statementDescription": "Payment for goods",
        "preAuthorisationCode": "string",
        "metadata": [
            {
                "fieldName": "orderId",
                "fieldValue": str(order_id)
            },
            {
                "fieldName": "customerId",
                "fieldValue": customer_email,
                "isPII": True
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Deposit successful:", response)
        return response.json()
    else:
        print("Deposit failed:", response)
        return {"error": response.status_code, "message": response.text}
