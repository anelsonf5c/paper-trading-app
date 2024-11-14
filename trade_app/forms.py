# forms.py
from django import forms

class BuyForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        error_messages={'min_value': 'Quantity must be at least 1.'}
    )

class SellForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        error_messages={'min_value': 'Quantity must be at least 1.'}
    )
