from django import forms
from .models import Transaction, UserRequest

# send money form
class TransactionSendForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['to_user', 'enter_amount']

# request money form
class TransactionRequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ['from_user', 'enter_amount']