from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import userRegisterForm, accountForm
from .models import Account
import requests

# home page
def index(request):
    return render(request, 'index.html', {'title': 'Welcome'})

#register user
def register(request):
    if request.method == 'POST':
        user_form = userRegisterForm(request.POST)
        account_form = accountForm(request.POST)    # gets info from form
        if user_form.is_valid():
            user = user_form.save()
            account = account_form.save(commit=False)   # saves form info
            account.user = user

            base_url = "http://127.0.0.1:8000/initial_exchange/"
            endpoint = f"{account.currency}"
            url = base_url + endpoint

            response = requests.get(url)        # sends request to restful web service to do initial exchange conversion

            exchanged_amount = int(response.json()['initial_amount'])   #exchanged initial amount
            account.balance = exchanged_amount
            account.save()      # saves account

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        user_form = userRegisterForm()  # resets forms
        account_form = accountForm()

    return render(request, 'register.html', {'user_form': user_form, 'account_form': account_form, 'title': 'Register'})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)      # gets login info from form and authenticates it
        if user is not None:
            form = login(request, user)
            messages.success(request, f'You are logged in! Welcome {username}')     #logins in user if exists
            return redirect('index')
        else:
            messages.info(request, f'Account does not exist. Please sign up and try again')  # message if user login does not exist
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'Log in'})

@login_required
def logout_view(request):   #logs out user
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('index')