from django import forms


class ChargeForm(forms.Form):
    product = forms.IntegerField()
