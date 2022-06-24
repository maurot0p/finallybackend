from rest_framework.serializers import ModelSerializer

from accounting.models import User, Account, Transaction

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__' # serialize all attributes

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        depth=1 #this allows me to access account nubmer from transaction