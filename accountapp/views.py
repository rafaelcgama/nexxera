# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from accountapp.models import Account, Transaction
from accountapp.serializers import AccountSerializer, TransactionSerializer


# Create your views here.
class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
