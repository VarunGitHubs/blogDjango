from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm
# Create your views here.

class UserRegisterView(generic.CreateView):
	form_class = RegisterForm # Initialise registation form 
	#form_class = UserCreationForm
	template_name = 'registration/register.html' # Specify the HTML page to view
	success_url = reverse_lazy('login') #If Signup is successful --> Login page 

