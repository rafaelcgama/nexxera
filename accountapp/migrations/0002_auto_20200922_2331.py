# Generated by Django 3.1.1 on 2020-09-22 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=6),
        ),
    ]
