from faker import Faker
from django.test import TestCase
from .models import Account, Transaction
from factory import DjangoModelFactory, SubFactory

# Create your tests here.
fake = Faker()
fake.seed_instance(0)


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
    transaction_type = fake.email(),
    amount =
