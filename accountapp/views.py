from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from accountapp.models import Account, Transaction
from rest_framework.response import Response
from accountapp.serializers import AccountSerializer, TransactionSerializer


def is_valid_query_param(param):
    return param != '' and param is not None


def get_balance(start_balance, qs, date=None, start=False):
    if start and date is not None:
        qs = qs.filter(date__lt=date)

    balance = qs.aggregate(Sum('amount'))['amount__sum']
    balance = balance if balance is not None else 0

    return start_balance + balance


@api_view(['GET'])
def get_statement(request):
    qs = ''
    is_json = 'json' in request.accepted_renderer.media_type
    types = ['Credit', 'Debit']

    # inputs
    account_number = request.GET.get('account_number')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    transaction_type = request.GET.get('transaction_type')

    start_balance = 0
    end_balance = 0
    if account_number is not None and len(account_number):

        qs = Transaction.objects.all()

        if is_valid_query_param(account_number):
            qs = qs.filter(account_id__id=account_number)

        if is_valid_query_param(date_min):
            start_balance = get_balance(start_balance, qs, date_min, start=True)
            qs = qs.filter(date__gte=date_min)

        if is_valid_query_param(date_max):
            qs = qs.filter(date__lte=date_max)

        if is_valid_query_param(transaction_type):
            if transaction_type != 'All':
                qs = qs.filter(transaction_type=transaction_type).order_by('date')

        end_balance = get_balance(start_balance, qs)

    context = {
        'start_balance': start_balance,
        'transactions': list(qs.values()) if (is_json and not isinstance(qs, str)) else qs,
        'end_balance': end_balance
    }

    # If client wants JSON
    if is_json:
        return JsonResponse(context, safe=False)

    # If the client wants HTML
    context.update({'types': types})
    return render(request, "statement.html", context)


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
        response = Response(serializer.data)
        response.status_code = 201

        return response
