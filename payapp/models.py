

from django.db import models
from register.models import User

# table to hold transaction info
class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_to')
    enter_amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        details = ''
        details += f'From user           : {self.from_user}\n'
        details += f'To user     : {self.to_user}\n'
        details += f'Amount        : {self.enter_amount}\n'
        return details

# table for pending user requests
class UserRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivered_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivered_to')
    enter_amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        details = ''
        details += f'From user           : {self.from_user}\n'
        details += f'To user           : {self.to_user}\n'
        details += f'Amount        : {self.enter_amount}\n'
        return details
