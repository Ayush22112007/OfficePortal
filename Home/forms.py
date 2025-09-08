from django import forms
from .models import Details
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class DetailsForm(forms.ModelForm):
    class Meta:
        model = Details
        fields = ['name', 'email', 'age', 'address', 'city', 'state', 'pincode']

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Password'
        })
    )
