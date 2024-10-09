# cart/forms.py
from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100, label='Full Name')
    address = forms.CharField(max_length=255, label='Address')
    phone = forms.CharField(max_length=15, label='Phone Number')
