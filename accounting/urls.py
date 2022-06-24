from django.urls import path
from .import views

urlpatterns = [
    path('',views.getRoutes, name='routes'),
    path('accounts/',views.getAccounts,name='accounts'),
    path('accounts/create',views.createAccount,name='create-account'),
    path('accounts/<str:pk>/',views.getAccount,name='account'),
    path('accounts/<str:pk>/transactions',views.getAccountTransactions,name='account'),
    path('accounts/<str:pk>/transactions/create',views.createTransaction,name='create-transaction'),
    path('transactions/',views.getTransactions,name='transactions'),
    path('accounts/<str:pk>/<str:date>',views.getBalanceByDate,name='account-date'),

]