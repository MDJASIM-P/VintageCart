from django import forms
from .models import *
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageModel
        fields = ['email', 'message']
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'message':forms.Textarea(attrs={'class':'form-control'})
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = ['title','feedback']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'feedback':forms.Textarea(attrs={'class':'form-control'}),
        }
        
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class SellerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form_control'}),
            'email':forms.EmailInput(attrs={'class':'form_control'}),
            'password1':forms.PasswordInput(attrs={'class':'form_control'}),
            'password2':forms.PasswordInput(attrs={'class':'form_control'}),
        }

class SellerLogInForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget= forms.PasswordInput())
        
