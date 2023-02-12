from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.models import User # Import the User database 


class RegisterForm(UserCreationForm):
	email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control'})) #create an email field

	class Meta:
		model = User #Initialise the user database
		fields = ['username','email','password1', 'password2'] #List of fields in UserCreationForm 

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control' #Apply Bootstrap 
		self.fields['password1'].widget.attrs['class'] = 'form-control' # Apply Bootstrap
		self.fields['password2'].widget.attrs['class'] = 'form-control' # Apply Bootstrap


		