from django import forms
from .models import Customer


class CompleteSignUp(forms.ModelForm):
    username = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Customer
        fields = ["phone_number", "username"]
