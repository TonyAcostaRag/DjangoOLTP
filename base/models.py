from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    age = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.username


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=50,default='Default value')
    balance = models.FloatField(default=0.0, blank=False, null=False)
    open_date = models.DateField(auto_now_add=True, blank=False, null=False)

    def __str__(self):
        return self.user


class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return self.account


class Transaction(models.Model):
    card_id = models.ForeignKey(Card, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0, blank=False, null=False)
    transaction_type = models.CharField(max_length=10) # Deposit, Withdrawal
    create_date = models.DateField(auto_now_add=True)
