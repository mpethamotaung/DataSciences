from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }