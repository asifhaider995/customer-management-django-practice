from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomerForm(ModelForm):
	"""docstring for CustomerForm"""
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class OrderForm(ModelForm):
	"""docstring for OrderForm"""
	class Meta:
		model = Order
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	"""docstring for CreateUserForm"""
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
		]		

