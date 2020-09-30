import os
from faker import Faker
from datetime import date
from decimal import Decimal

from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import path, reverse
from django.conf.urls import include

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from .views import get_balance

from factory.django import DjangoModelFactory
from factory import SubFactory, fuzzy

# Create your tests here.
fake = Faker()
fake.seed_instance(0)
urlpatterns = [
    path('api/v1/', include('accountapp.urls'))
]


##### FACTORIES ######
# Create Account Factory
class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account
        django_get_or_create = ('id', 'owner', 'dob', 'email')

    id = fake.pyint(min_value=0)
    owner = fake.name()
    dob = fake.date_of_birth()
    email = fake.email()


# Create Transaction Factory
class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction
        django_get_or_create = ('account_id', 'date', 'description', 'transaction_type', 'amount')

    account_id = SubFactory(AccountFactory)
    date = fake.date_this_century()
    description = fake.text()
    transaction_type = fuzzy.FuzzyChoice(['Credit', 'Debit'])
    amount = fake.pydecimal(right_digits=2, positive=True)


##### MODEL TESTS #####
class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = AccountFactory()

    def test_account_creation(self):
        self.assertIsInstance(self.account, Account)

    def test_dtypes(self):
        self.assertIsInstance(self.account.id, int)
        self.assertIsInstance(self.account.owner, str)
        self.assertIsInstance(self.account.dob, date)
        self.assertIsInstance(self.account.email, str)

    def test_all_fields_populated(self):
        self.assertTrue(self.account.id)
        self.assertTrue(self.account.owner)
        self.assertTrue(self.account.dob)
        self.assertTrue(self.account.email)


class TransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = AccountFactory()
        cls.transaction = TransactionFactory(account_id=cls.account)

    def test_account_creation(self):
        self.assertIsInstance(self.transaction, Transaction)

    def test_dtypes(self):
        self.assertIsInstance(self.transaction.account_id_id, int)
        self.assertIsInstance(self.transaction.date, date)
        self.assertIsInstance(self.transaction.description, str)
        self.assertIsInstance(self.transaction.transaction_type, str)
        self.assertIsInstance(self.transaction.amount, type(fake.pydecimal()))

    def test_all_fields_populated(self):
        self.assertTrue(self.transaction.account_id)
        self.assertTrue(self.transaction.date)
        self.assertTrue(self.transaction.transaction_type)
        self.assertTrue(self.transaction.amount)


##### VIEW TESTS #####
class AccountViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.new_account = {
            'id': '1',
            'owner': 'Test',
            'dob': '1984-06-06',
            'email': 'test@test.com'
        }
        self.response = self.client.post(reverse('account-list'),
                                         self.new_account,
                                         format='json',
                                         )

    # Test List and Create
    def test_create_list(self):
        url_list_create = reverse('account-list')

        # Test Create
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().owner, self.new_account['owner'])

        # Test List
        response_list = self.client.get(url_list_create,
                                        self.new_account,
                                        format='json'
                                        )
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().owner, self.new_account['owner'])

    # Test Retrieve
    def test_retrieve(self):
        account_retrieve = Account.objects.get(id=self.new_account['id'])
        resp_retrieve = self.client.get(
            reverse('account-detail', kwargs={'pk': account_retrieve.id}),
            format='json'
        )
        self.assertEqual(resp_retrieve.status_code, status.HTTP_200_OK)

    # Test Update giving all attributes and the change to be executed
    def test_update_all_attrs(self):
        account_update = Account.objects.get()
        change_account = {
            'id': '123',
            'owner': 'Johnny',
            'dob': '1974-03-06',
            'email': 'new_test@test.com'
        }
        resp_update = self.client.put(
            reverse('account-detail', kwargs={'pk': account_update.id}),
            change_account,
            format='json'
        )
        self.assertEqual(resp_update.status_code, status.HTTP_200_OK)

    # Test Update giving only the attribute to be changed
    def test_update_one_attrib(self):
        account_update = Account.objects.get()
        change_account = {'name': 'Something new'}
        resp_update = self.client.patch(
            reverse('account-detail', kwargs={'pk': account_update.id}),
            change_account,
            format='json'
        )
        # force_authenticate(resp_update, user=self.username, token=self.user.auth_token)
        self.assertEqual(resp_update.status_code, status.HTTP_200_OK)

    # Test Delete
    def test_delete(self):
        account_delete = Account.objects.get()
        resp_delete = self.client.delete(
            reverse('account-detail', kwargs={'pk': account_delete.id}),
            format='json',
            follow=True)
        self.assertEquals(resp_delete.status_code, status.HTTP_204_NO_CONTENT)


class TransactionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account = AccountFactory()

    def setUp(self):
        self.client = APIClient()
        self.new_transaction = {
            'account_id': str(self.account.id),
            'date': '2020-09-20',
            'description': 'Fish',
            'transaction_type': 'Credit',
            'amount': '50.00'
        }

        self.response = self.client.post(reverse('transaction-list'),
                                         self.new_transaction,
                                         format='json',
                                         )

    # Test List and Create
    def test_create_list(self):
        url_list_create = reverse('transaction-list')

        # Test Create
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().amount, Decimal(self.new_transaction['amount']))

        # Test List
        response_list = self.client.get(url_list_create,
                                        self.new_transaction,
                                        format='json'
                                        )
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().amount, Decimal(self.new_transaction['amount']))

    # Test Retrieve
    def test_retrieve(self):
        transaction_retrieve = Transaction.objects.get(account_id=self.new_transaction['account_id'])
        resp_retrieve = self.client.get(
            reverse('transaction-detail', kwargs={'pk': transaction_retrieve.id}),
            format='json'
        )
        self.assertEqual(resp_retrieve.status_code, status.HTTP_200_OK)

    # Test Update giving all attributes and the change to be executed
    def test_update_all_attrs(self):
        transaction_update = Transaction.objects.get()
        change_transaction = {
            'account_id': self.account.id,
            'date': '2020-09-21',
            'description': 'Cake',
            'transaction_type': 'Debit',
            'amount': '10.00'
        }
        resp_update = self.client.put(
            reverse('transaction-detail', kwargs={'pk': transaction_update.id}),
            change_transaction,
            format='json'
        )
        self.assertEqual(resp_update.status_code, status.HTTP_200_OK)

    # Test Update giving only the attribute to be changed
    def test_update_one_attrib(self):
        transaction_update = Transaction.objects.get()
        change_transaction = {'description': 'Soda'}
        resp_update = self.client.patch(
            reverse('transaction-detail', kwargs={'pk': transaction_update.id}),
            change_transaction,
            format='json'
        )
        # force_authenticate(resp_update, user=self.username, token=self.user.auth_token)
        self.assertEqual(resp_update.status_code, status.HTTP_200_OK)

    # Test Delete
    def test_delete(self):
        transaction_delete = Transaction.objects.get()
        resp_transaction = self.client.delete(
            reverse('transaction-detail', kwargs={'pk': transaction_delete.id}),
            format='json',
            follow=True)
        self.assertEquals(resp_transaction.status_code, status.HTTP_204_NO_CONTENT)


class StatementViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account = AccountFactory()
        cls.transaction = TransactionFactory()

    def setUp(self):
        self.client = APIClient()
        self.transactions = TransactionFactory()
        self.base_end_point = '/api/v1/statement/'
        self.base_url = self.base_end_point + '?account_number={account_id}&date_min={date_min}&date_max={date_max}&transaction_type={transaction_type}'
        self.new_statement = {
            'account_id': self.account.id,
            'date_min': '2020-09-03',
            'date_max': '2020-09-15',
            'transaction_type': 'All'
        }

    def test_main_page(self):
        response = self.client.get(self.base_end_point, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_statement(self):
        search_url = self.base_url.format_map(self.new_statement)
        response = self.client.get(search_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.base_end_point)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertTemplateUsed(response, 'bootstrap_form.html')

    def test_get_balance_start(self):
        qs = Transaction.objects.all()
        start_balance = get_balance(0, qs, date=self.transaction.date, start=True)

        self.assertIsInstance(Decimal(start_balance), Decimal)
        self.assertTrue(0 == start_balance)


##### SERIALIZERS TESTS #####
class EmployeeSerializerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account = AccountFactory()

    def setUp(self):
        self.serializer = AccountSerializer(self.account)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'owner', 'dob', 'email']))

    def test_columns_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.account.id)
        self.assertEqual(data['owner'], self.account.owner)
        self.assertEqual(data['dob'], self.account.dob.strftime("%Y-%m-%d"))
        self.assertEqual(data['email'], self.account.email)


class SalarySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = AccountFactory()
        cls.transaction = TransactionFactory(account_id=cls.account)

    def setUp(self):
        self.serializer = TransactionSerializer(self.transaction)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()),
                         set(['account_id', 'date', 'description', 'transaction_type', 'amount', 'id']))

    def test_columns_content(self):
        data = self.serializer.data
        self.assertEqual(data['account_id'], self.account.id)
        self.assertEqual(data['date'], self.transaction.date.strftime("%Y-%m-%d"))
        self.assertEqual(data['description'], self.transaction.description)
        self.assertEqual(data['transaction_type'], self.transaction.transaction_type)
        self.assertEqual(data['amount'], str(self.transaction.amount))


##### TEST MANAGE #####
class TestEnvVariable(TestCase):

    def test_django_env_variable(self):
        django_settings = os.getenv('DJANGO_SETTINGS_MODULE')

        self.assertTrue(django_settings)
        self.assertIsInstance(django_settings, str)
        self.assertEqual(django_settings, 'nexxera.settings')
