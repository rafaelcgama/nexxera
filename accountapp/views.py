from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from accountapp.models import Account, Transaction
from rest_framework.response import Response
from accountapp.serializers import AccountSerializer, TransactionSerializer

def is_valid_queryparam(param):
    return param != '' and param is not None

def BootstrapFilterView(request):
    qs = ''
    types = ['Credit', 'Debit']

    # inputs
    account_number = request.GET.get('account_number')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    transaction_type = request.GET.get('transaction_type')

    if account_number is not None:

        qs = Transaction.objects.all()

        if is_valid_queryparam(account_number):
            qs = qs.filter(account_id__id=account_number)

        if is_valid_queryparam(date_min):
            qs = qs.filter(date__gte=date_min)

        if is_valid_queryparam(date_max):
            qs = qs.filter(date__lt=date_max)

        if is_valid_queryparam(transaction_type):
            if transaction_type != 'All':
                qs = qs.filter(transaction_type=transaction_type)

    context = {
        'queryset': qs,
        'types': types
    }

    return render(request, "bootstrap_form.html", context)



# Create your views here.
class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        transaction_data = request.data
        sign = '' if transaction_data['transaction_type'] == 'Credit' else '-'

        new_transaction = Transaction.objects.create(
            account_id=Account.objects.get(id=transaction_data['account_id']),
            date=transaction_data['date'],
            description=transaction_data['description'],
            transaction_type=transaction_data['transaction_type'],
            amount=f'{sign}{transaction_data["amount"]}'
        )
        new_transaction.save()

        serializer = TransactionSerializer(new_transaction)

        return Response(serializer.data)
