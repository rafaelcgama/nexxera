from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

TRANSACTION_CHOICES = (
    ('Credit', 'Credit'),
    ('Debit', 'Debit')
)


# Create your models here.
class Account(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    owner = models.CharField(max_length=50, blank=False, null=False)
    dob = models.DateField(blank=False, null=False)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = 'account'


class Transaction(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_CHOICES, blank=False, null=False)
    amount = models.DecimalField(max_digits=13, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))],
                                 null=False, blank=False)

    class Meta:
        db_table = 'transaction'
