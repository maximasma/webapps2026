from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from register.models import Account,User

# exchanges currency
@api_view(["GET"])
def exchange(request, currency1 ,currency2,amount):     # gets info from url
    exchange_rate = {           # static exchange rates
        'GBP_to_USD' : 1.34,
        'EUR_to_USD' : 1.17,
        'USD_to_GBP': 0.74,
        'USD_to_EUR': 0.85,
        'GBP_to_EUR': 1.15,
        'EUR_to_GBP': 0.86,
    }
    amount = float(amount)

    valid_currency = ["GBP", "EUR", "USD"]
    if currency1 in valid_currency and currency2 in valid_currency:  # checks info in url is valid
        if currency1 == currency2:
            final_amount = amount
            return JsonResponse({"final_amount": final_amount})     # currency is same so amount doesnt change
        else:
            final_amount = amount * exchange_rate[f'{currency1}_to_{currency2}']    # gets appropriate exchange rate from dict and gets final amount
            return JsonResponse({"final_amount": final_amount})     # sends final amount back
    else:
        return JsonResponse({'error': 'Invalid Currency'})

# exchange at register
@api_view(["GET"])
def initial_exchange(request, currency):
    initial_exchange_rate = {
        'GBP_to_USD' : 1.34,
        'GBP_to_EUR' : 1.17,
        'GBP_to_GBP': 1,
    }
    inital_amount = initial_exchange_rate[f'GBP_to_{currency}'] * 500   # creates initial amount for user
    return JsonResponse({"initial_amount": inital_amount}) # sends back

