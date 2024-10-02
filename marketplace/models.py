import uuid
from django.db import models
from django.contrib.auth.models import User

class Farmer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.product.name} by {self.customer.name}"

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    company_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - Status: {self.status} - Amount: ZMW {self.amount}"
