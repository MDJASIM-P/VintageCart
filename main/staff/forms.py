from django import forms
from .models import *
from django.contrib.auth.models import User
# class StaffCreationForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'password']
#         def fun(self):
#             self.is_staff=True