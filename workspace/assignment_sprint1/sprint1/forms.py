# Imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Sign up form (additional) fields
class SignUpForm(UserCreationForm):
    firstName = forms.CharField(required=True)   # Note for later: help_text can be an additional parameter
    lastName = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=[(1, "Male"), (2, "Female"), (3, "Other")])
    dateOfBirth = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    phoneNumber = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=False)
    address = forms.CharField(required=True)

class Meta:
    model = User
    fields = ('username', 'firstName', 'lastName', 'gender', 'dateOfBirth', 'email', 'phoneNumber', 'address', 'password1', 'password2', )
    
