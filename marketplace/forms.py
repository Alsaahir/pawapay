from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Farmer, Customer, Product


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class FarmerSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Farmer
        fields = ['name', 'contact']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        farmer = Farmer(
            user=user,
            name=self.cleaned_data['name'],
            contact=self.cleaned_data['contact']
        )
        if commit:
            user.save()
            farmer.save()
        return user
    

class CustomerSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Customer
        fields = ['name', 'contact', 'address']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        customer = Customer(
            user=user,
            name=self.cleaned_data['name'],
            contact=self.cleaned_data['contact'],
            address=self.cleaned_data['address']
        )
        if commit:
            user.save()
            customer.save()
        return user
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']  # Include the fields you want to capture

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter product name'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Enter product price'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter product description'})


class OrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, help_text="Enter the quantity you want to order.")