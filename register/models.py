

from django.db import models
from django.contrib.auth.models import AbstractUser

# User model
class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)   # used to give users access to hidden pages


    def __str__(self):
        return self.username

# account model
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    def __str__(self):
        details =''
        details += f'balance: {self.balance} '
        details += f'currency: {self.currency}'
        return details






