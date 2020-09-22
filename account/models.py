from django.db import models

# Create your models here.
class Account(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False, unique=True)
    owner = models.CharField(max_length=50, blank=False, null=False)
    dob = models.DateField(blank=False, null=False)
    email = models.EmailField()

    class Meta:
        db_table = 'account'

class Transaction(models.Model):
    id = models.ForeignKey(Account, on_delete=models.CASCADE())
    date = models.DateField(blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    transaction_type = models.CharField(max_length=6, black=False, null=False)
    amount = models.DecimalField(null=False, blank=False)
