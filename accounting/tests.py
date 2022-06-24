from django.test import TestCase
from datetime import date,timedelta
from accounting.models import User, Account, Transaction
class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        user = User.objects.create(username='mauricio',password='12345')
        account1= Account.objects.create(user_id=user, account_id='00504041', account_number='000405061',current_balance=10000)
        transaction = Transaction.objects.create(account_id=account1,date=date.today(),transaction_type='credit',note='coffee',amount=2000)
        transaction2 = Transaction.objects.create(account_id=account1,date=date.today()-timedelta(3),transaction_type='debit',note='coffee',amount=8000) #this occured on the 18th
        transaction3 = Transaction.objects.create(account_id=account1,date=date.today()+timedelta(3),transaction_type='credit',note='coffee',amount=8000) #future transaction
    def testTransactions(self):
         account = Account.objects.get(id=1)
         self.assertEqual(account.current_balance,12000)
         self.assertEqual(account.current_balance,12000)

    def testGetBalanceByDate(self):
         account = Account.objects.get(id=1)
         self.assertEqual(account.get_balance_by_date(date(2022,6,24)),4000) #24-3=21, if you run this tests are subject to date today
         self.assertEqual(account.get_balance_by_date(date(2022,6,21)),2000)
         self.assertEqual(account.get_balance_by_date(date(2022,6,20)),10000) 
         self.assertEqual(account.get_balance_by_date(date(2022,6,22)),2000) # on the 22th, my future transactio hasnt happened
         self.assertEqual(account.get_balance_by_date(date(2022,6,27)),12000) # on the 27th, my future transactio has happened

