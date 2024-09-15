# forms.py
from django import forms

class CustomerSearchForm(forms.Form):
    query = forms.CharField(label='Search for Customer', max_length=100, required=False)
    phone_number = forms.CharField(label='Search by phone number', max_length=15, required=False)
    score = forms.IntegerField(label='Search by Score', required=False)
