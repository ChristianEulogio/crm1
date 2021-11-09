from django.forms import ModelForm
#importamos la plantilla para crear el user
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields= '__all__'

#del formulario usercreationform lo modificamos y agregamos email 2 
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']