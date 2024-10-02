import requests

def initiate_payment(phone_number, amount, transaction_id):
    url = "https://api.pawapay.com/v1/transactions"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    data = {
        "amount": amount,
        "currency": "ZMW",
        "reference": transaction_id,
        "phone": phone_number,
        "provider": "AIRTEL_MONEY"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
