from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Account,Transaction, User
from .serializers import AccountSerializer,UserSerializer,TransactionSerializer
from datetime import date,datetime
from decimal import Decimal

# Create your views here.
@api_view(['GET','POST']) #this is a decorator
def getRoutes(request):

    routes = [
          {
            'Endpoint': 'user',
            'method': 'GET',
            'body': None,
            'description': 'Returns user'
        },
        {
            'Endpoint': 'accounts/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of accounts'
        },
        {
            'Endpoint': 'accounts/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single account object'
        },
        {
            'Endpoint': 'accounts/id/transactions',
            'method': 'GET',
            'body': None,
            'description': 'Returns all accounts transactions'
        },
          {
            'Endpoint': 'transactions',
            'method': 'GET',
            'body': None,
            'description': 'Returns all transactions'
        },
          {
            'Endpoint': 'accounts/id/date',
            'method': 'GET',
            'body': None,
            'description': 'Get balance of account at a certain date'
        },
        {
            'Endpoint': 'accounts/create',
            'method': 'POST',
            'body': {"account_id": "","account_number":"","current_balance":""},
            'description': 'Create new acount'
        },
        {
            'Endpoint': 'transactions/create',
            'method': 'POST',
            'body': {"date": "","transaction_type":"","note":"","amount":""},
            'description': 'Create new transaction'
        },
    
    ]
    return Response(routes)

@api_view(['GET'])
def getUser(request,pk):
    user = User.objects.get(id=pk) 
    serializer = UserSerializer(user, many= False) 
    return Response(serializer.data) 


@api_view(['GET']) 
def getAccounts(request):
    accounts = Account.objects.all() #have to serialize this python object
    serializer = AccountSerializer(accounts, many= True) #many says to serialize multiple objects, will return a query set
    return Response(serializer.data) #serializer itself is an object

@api_view(['POST'])
def createAccount(request):
    data = request.data
    account = Account.objects.create(
        user_id = User.objects.get(id=2),
        account_id = data['account_id'],
        account_number = data['account_number'],
        current_balance = data['current_balance']
    )
    serializer = AccountSerializer(account,many=False)
    return Response(serializer.data)

@api_view(['GET']) 
def getAccount(request,pk): #get a single account
    accounts = Account.objects.get(id=pk) 
    serializer = AccountSerializer(accounts, many= False) #many false returns a single object
    return Response(serializer.data) #serializer itself is an object

@api_view(['GET'])
def getTransactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createTransaction(request,pk):
    data = request.data
    transaction = Transaction.objects.create(
        account_id = Account.objects.get(id=pk),
        date = datetime.strptime(data['date'], '%m-%d-%Y').date(),
        transaction_type = data['transaction_type'],
        note = data['note'],
        amount = Decimal(data['amount'])
    )
    serializer = TransactionSerializer(transaction,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getAccountTransactions(request,pk):
    account = Account.objects.get(id=pk) 
    transactions = account.transactions.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getBalanceByDate(request,pk,date):
    account = Account.objects.get(id=pk) 
    date_obj = datetime.strptime(date, '%m-%d-%Y').date()
    #need to convert date string to date
    balance = account.get_balance_by_date(date_obj)
    return Response(balance)