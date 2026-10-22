"""
store/forms.py

CONCEPT 4 (DJANGO FORMS & MODELFORMS):
Django Forms handle user input validation, data cleaning, and HTML rendering.
- ModelForm: Automatically creates an HTML form based on a Django Model schema.
  It maps model fields directly to form inputs and saves cleaned data to the database using form.save().
- UserCreationForm: A built-in Django form for registering new users with password hashing.
  We extend it to include first name, last name, and email.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order


# ==============================================================================
# USER SIGNUP FORM
# ==============================================================================
class SignUpForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm to collect first_name, last_name, and email.
    CONCEPT 14 (PYTHON BASICS - CLASSES & INHERITANCE):
    We inherit from UserCreationForm and customize its fields and widgets.
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # Apply clean styling classes to all input fields
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_class} form-input'.strip()


# ==============================================================================
# SHIPPING / CHECKOUT ORDER FORM
# ==============================================================================
class OrderCreateForm(forms.ModelForm):
    """
    CONCEPT 4 (MODELFORM):
    OrderCreateForm takes input for shipping details:
    full_name, phone, address, city, pincode.
    
    When submitted, views.py runs:
    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.save()
    """
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'city', 'pincode']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter full name for delivery',
                'id': 'full_name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '10-digit mobile number',
                'id': 'phone'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Street address, apartment, suite, etc.',
                'rows': 3,
                'id': 'address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City / Town',
                'id': 'city'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Postal / PIN Code',
                'id': 'pincode'
            }),
        }
