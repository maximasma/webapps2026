from django import forms
from django.contrib.auth.forms import UserCreationForm

from register.models import User
from register.models import Account

# registration form
class userRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username',max_length=30)
    email = forms.EmailField(label='Email',max_length=30)
    first_name = forms.CharField(label='First Name',max_length=30)
    last_name = forms.CharField(label='Last Name',max_length=30)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


# form for picking currency
class accountForm(forms.ModelForm):
    currencies =[
        ('GBP','GBP'),
        ('USD','USD'),
        ('EUR','EUR'),
    ]
    currency = forms.ChoiceField(choices=currencies)

    class Meta:
        model = Account
        fields = ('currency',)