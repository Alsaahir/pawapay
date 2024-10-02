from datetime import datetime
import uuid
from django.shortcuts import render, get_object_or_404, redirect
import requests
from .models import Product, Order, Transaction, Farmer, Customer
from .pawapay import initiate_payout, initiate_deposit
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import FarmerSignupForm, CustomerSignupForm, ProductForm, OrderForm, LoginForm
import logging
from django.http import JsonResponse


logger = logging.getLogger(__name__)


def home_view(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def purchase_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        quantity = int(request.POST['quantity'])
        phone_number = request.POST['phone_number']
        total_price = product.price * quantity
        
        customer = request.user.customer

        order = Order.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price,
            customer=customer
        )

        transaction = Transaction.objects.create(
            order=order,
            amount=total_price,
            transaction_id=f"TX-{order.id}",
            status="Pending"
        )

 
        response = initiate_deposit(phone_number, total_price, transaction.transaction_id, customer.email)
        logger.debug(f"Payment response: {response}")

        if response.get('error'):
            return render(request, 'error.html', {'error': response["message"]})

        if response.get('status') == 'ACCEPTED':
            transaction.status = "Completed"
            order.is_done = False
            order.save() 
            return redirect('order_list')
        else:
            transaction.status = "Failed"
        
        transaction.save()

        return render(request, 'transaction_status.html', {'transaction': transaction, 'response': response})

    return render(request, 'purchase.html', {'product': product})


def process_payment(request):
    if request.method == "POST":
       
        recipient_phone = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        order_id = request.POST.get('order_id')
        customer_email = request.POST.get('customer_email')
      
        url = "https://api.sandbox.pawapay.cloud/payouts"
        payout_id = str(uuid.uuid4()) 
        
        payload = {
            "payoutId": payout_id,
            "amount": amount,
            "currency": "ZMW",
            "country": "ZMB",
            "correspondent": "MTN_MOMO_ZMB",
            "recipient": {
                "type": "MSISDN",
                "address": {
                    "value": int(recipient_phone)
                }
            },
            "customerTimestamp": datetime.utcnow().isoformat() + "Z",
            "statementDescription": "Payment for goods",
            "metadata": [
                {
                    "fieldName": "orderId",
                    "fieldValue": order_id
                },
                {
                    "fieldName": "customerId",
                    "fieldValue": customer_email,
                    "isPII": True
                }
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer eyJraWQiOiIxIiwiYWxnIjoiRVMyNTYifQ.eyJ0dCI6IkFBVCIsInN1YiI6IjI4MjMiLCJleHAiOjIwNDI5MjIzNzMsImlhdCI6MTcyNzM4OTU3MywicG0iOiJEQUYsUEFGIiwianRpIjoiODg4NjliOTktOTA4ZC00YTI4LTlhNGItMmFmMDI0YzU1YTg3In0.DrNUz5xCNjP4NMZmS8686Uh7S8hwZ-repmb3QNFv0w4vn0ysHcuRWdX2PXdhnm7kRrYrIonTiikLDL6Rz-_CPA",
            "Content-Digest": "string",  
            "Signature": "string",  
            "Signature-Input": "string",  
            "Accept-Signature": "string",  
            "Accept-Digest": "string"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()

            if response.get('status') == 'ACCEPTED':
                print(response_data)
                return JsonResponse({"message": "Payment successful", "data": response_data})
            else:
                print(response_data)
                return JsonResponse({"error": "Payment failed", "details": response_data}, status=response.status_code)
        
        except Exception as e:

            return JsonResponse({"error": "An error occurred", "details": str(e)}, status=500)
    
    return render(request, 'payment_form.html')


def farmer_signup(request):
    if request.method == 'POST':
        form = FarmerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('process_payment')
    else:
        form = FarmerSignupForm()
        print("Unssuccessful!")
    return render(request, 'registration/farmer_signup.html', {'form': form})

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('process_payment')
    else:
        form = CustomerSignupForm()
    return render(request, 'registration/customer_signup.html', {'form': form})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = Farmer.objects.get(user=request.user)
            product.save()
            return redirect('products')
    else:
        form = ProductForm()
    
    return render(request, 'product/add_product.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            quantity = order_form.cleaned_data['quantity']
            total_price = product.price * quantity
            
            customer, created = Customer.objects.get_or_create(email=request.user.email, defaults={'name': request.user.username})


            order = Order.objects.create(product=product, quantity=quantity, total_price=total_price, customer=customer)
            
            return redirect('order_success')
    else:
        order_form = OrderForm()

    return render(request, 'product/product_detail.html', {
        'product': product,
        'order_form': order_form
    })



@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user.customer) 
    return render(request, 'product/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    
    if request.method == "POST":
        order.is_done = True
        order.save()
        return redirect('order_list')

    return render(request, 'product/order_detail.html', {'order': order})


@login_required
def mark_order_done(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)

    if request.method == "POST" and not order.is_done:
        order.is_done = True
        order.save()

        total_price = float(order.total_price)
        payout_amount = total_price * 0.95

        farmer = order.product.farmer
        farmer_phone_number = farmer.contact

        payout_response = initiate_payout(payout_amount, farmer_phone_number)

        if payout_response.get('status') == 'ACCEPTED':
            print(payout_response)
            
        else:
            logging.error(f"Payout failed: {payout_response['message']}")
            return JsonResponse({"error": "Payout failed. Please try again."})

        logging.info(f"Payout successful for Order {order_id}. Farmer received {payout_amount} ZMW")
        return JsonResponse({"message": "Order marked as done and payout successful."})

    return redirect('order_detail', order_id=order_id)