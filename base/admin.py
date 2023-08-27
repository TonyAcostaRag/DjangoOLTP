from django.contrib import admin
from .models import User, Account, Card, Transaction

# Register your models here.
admin.site.register(User)
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Transaction)