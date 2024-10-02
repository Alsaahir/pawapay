from django.contrib import admin
from .models import Transaction, Product, Farmer, Order, Customer



admin.site.site_header = "AGRITECH ADMIN"

admin.site.register(Transaction)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Farmer)
admin.site.register(Customer)
