from django.contrib.auth.decorators import login_required
from django.db import transaction, OperationalError
from django.db.models import F
from django.shortcuts import render
from . import models
from payapp.forms import TransactionSendForm, TransactionRequestForm
from register.models import Account, User
from django.contrib import messages
from django.db.models import Q
from .models import Transaction, UserRequest
import requests


# function used to send money to another user
@login_required
def send_money(request):
    if request.method == 'POST':
        form = TransactionSendForm(request.POST)
        if form.is_valid():

                src_user = User.objects.get(username = request.user.username)
                dst_username = form.cleaned_data['to_user']
                dst_user = User.objects.get(username=dst_username)  # gets source and destination user

                amount = form.cleaned_data['enter_amount']

                base_url = "http://127.0.0.1:8000/exchange/"
                endpoint = f"{src_user.account.currency}/{dst_user.account.currency}/{amount}"  # uses restful web service to convert currency
                url = base_url + endpoint

                response = requests.get(url)

                exchanged_amount = int(response.json()['final_amount']) # gets exchanged amount

                src_account = Account.objects.get(user = src_user)
                dst_account = Account.objects.get(user= dst_user)   # source and destination account (easier for me than writing user.account everytime)

                if src_account.balance < amount or src_account == dst_account:
                    messages.info(request,f"Either your balance is too low or you are trying to send money to yourself") # cant send if balance is too low or sending to themselves
                else:


                    try:
                        with transaction.atomic():
                            src_account.balance = src_account.balance - amount
                            src_account.save()                                  # user inputted amount gets taken away from source account balance

                            dst_account.balance = dst_account.balance + exchanged_amount
                            dst_account.save()      # exchanged amount gets added to destination account
                    except OperationalError:
                        messages.info(request,f"Transfer operation not possible at the moment.")    # error if transfer doesnt go through
                    else:
                        messages.info(request,f'Transfer operation successful')
                        user_transaction = Transaction(from_user = src_user, to_user = dst_user, enter_amount = amount)
                        user_transaction.save() # saves transaction so it can be viewed by participating users/admin

        return render(request,  'index.html')

    else:
        form = TransactionSendForm()

    return render(request, 'transaction_send.html', {'form': form})

@login_required
def past_transactions(request):
    user_transactions = Transaction.objects.filter(Q(from_user = request.user) | Q(to_user=request.user)) # lets user see past transactions

    return render(request, 'past_transactions.html', {'user_transactions': user_transactions})

#sends request to a user
@login_required
def request_money(request):
    if request.method == 'POST':
        form = TransactionRequestForm(request.POST)
        if form.is_valid():
            money_request = form.save(commit=False)     # gets request info from form
            money_request.to_user = request.user
            money_request.save()        # saves request info so it can be viewed by requested user
            messages.success(request, f'Transaction request sent successfully')
            return render(request, 'index.html')
    else:
        form = TransactionRequestForm()

    return render(request, 'transaction_request.html', {'form': form})

@login_required
def user_requests(request):
    user_requests = UserRequest.objects.filter(from_user=request.user)
    if request.method == 'POST':
        user_request_id = request.POST['user_request_id']
        user_request = UserRequest.objects.get(id=user_request_id)  # gets corresponding request

        if request.POST['action'] == 'reject':
            messages.info(request,f'Request rejected')
            user_request.delete()                               # if user rejects request it deletes it
            return render(request, 'user_requests.html', {'requests': user_requests})

        src_user = User.objects.get(username=user_request.from_user.username)   # everything below is same as above
        dst_user = User.objects.get(username=user_request.to_user.username)

        src_account = Account.objects.get(user=user_request.from_user)
        dst_account = Account.objects.get(user=user_request.to_user)
        amount = user_request.enter_amount

        base_url = "http://127.0.0.1:8000/exchange/"
        endpoint = f"{src_user.account.currency}/{dst_user.account.currency}/{amount}"
        url = base_url + endpoint

        response = requests.get(url)

        exchanged_amount = int(response.json()['final_amount'])

        if src_account.balance < amount or src_account == dst_account:
            messages.info(request, f'Either your balance is too low or you are trying to send money to yourself')
        else:
            try:
                with transaction.atomic():
                    src_account.balance = src_account.balance - amount
                    src_account.save()

                    dst_account.balance = dst_account.balance + exchanged_amount
                    dst_account.save()
            except OperationalError:
                messages.info(request,f'Transfer operation not possible at the moment.')
            else:
                messages.info(request,f'Transfer operation successful')
                user_transaction = Transaction(from_user = user_request.from_user, to_user = user_request.to_user, enter_amount = amount)
                user_transaction.save()
                user_request.delete()


    return render(request, 'user_requests.html', {'requests': user_requests})

# admin can view all transactions
@login_required
def admin_transactions(request):

    if request.user.is_staff:
        all_transactions = Transaction.objects.all() # gets all transactions if user is staff
        return render(request, 'admin_transactions.html', {'all_transactions': all_transactions})
    else:
        return render(request, 'index.html')

# lets admin view all accounts
@login_required
def admin_accounts(request):

    if request.user.is_staff:
        all_users = User.objects.all()  # gets all users
        if request.method == 'POST':
            user_id = request.POST['user_id']
            user = User.objects.get(id = user_id)
            user.is_staff = True        # admin makes another user admin
            user.save()
        return render(request, 'admin_accounts.html', {'all_users': all_users})
    else:
        return render(request, 'index.html')





