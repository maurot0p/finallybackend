from django.db import models
from django.utils.text import slugify
from datetime import datetime

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.username

class Account(models.Model): #id is added automatically, user to account has one to many relationship
    user_id = models.ForeignKey(User, related_name='accounts', on_delete=models.CASCADE) #note: I just realized that after deleting an account, primary key remains same
    account_id = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.account_number
    def get_account_number(self):
        return self.account_number
    def get_current_balance(self):
        return self.current_balance
    def get_balance_by_date(self, date):
        transactions=self.transactions.all().order_by('date')
        balance_at_date=self.current_balance # i have to sort transactions by date
        i=transactions.count()-1
        while i>=0 and transactions[i].date>date:
            if transactions[i].transaction_type=='credit':
                balance_at_date-=transactions[i].amount
            else:
                balance_at_date+=transactions[i].amount
            i=i-1
        return balance_at_date # it works, returns the amount by the end of that day.
            #if i have current balance, and I loop all the transactions from that date to the transaction date, I could recreate the balance at that date.

class Transaction(models.Model):
    CREDIT = 'credit'
    DEBIT = 'debit'
    CHOICES_STATUS = (
        (CREDIT,'Credit'),
        (DEBIT,'Debit')
    )
    account_id = models.ForeignKey(Account, related_name='transactions',on_delete=models.CASCADE)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices= CHOICES_STATUS)
    note = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def save(self, *args, **kwargs): #on save a transaction, you want to update the related account's current balance
        if self.transaction_type=='credit':
            self.account_id.current_balance += self.amount
            self.account_id.save()
        else:
            self.account_id.current_balance -= self.amount
            self.account_id.save()
        super().save(*args, **kwargs)  # Call the "real" save() method.
    def __str__(self):
        return self.note
    def formatDate(self):
        return self.date.strftime('%B %d, %Y')


    