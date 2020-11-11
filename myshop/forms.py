from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from .models import UserProfile, Order, Item, Refund


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ["username", "password1", "password2"]


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['amount']


class ItemCreateForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class RefundForm(ModelForm):

    class Meta:
        model = Refund
        fields = []

