import requests

def initiate_payment(phone_number, amount, transaction_id):
    url = "https://api.pawapay.com/v1/transactions"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    data = {
        "amount": amount,
        "currency": "ZMW",  # Zambian Kwacha
        "reference": transaction_id,
        "phone": phone_number,
        "provider": "AIRTEL_MONEY"  # or other relevant providers in Zambia
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
