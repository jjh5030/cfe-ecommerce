from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    save_card = forms.BooleanField(initial=True, required=False)
    class Meta:
        model = Address
        exclude = ['user','default_address','billing_address','shipping_address']