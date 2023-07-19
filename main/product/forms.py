from django import forms
from .models import *

class ClothForm(forms.ModelForm):
    class Meta:
        model = ClothModel
        fields = ['name', 'details', 'price', 'size', 'image']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["quantity"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"class":"form-control", "min":1})
        }