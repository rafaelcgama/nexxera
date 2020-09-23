# Generated by Django 3.1.1 on 2020-09-23 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountapp', '0003_auto_20200923_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('filter_by', models.CharField(blank=True, choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=6, null=True)),
            ],
            options={
                'db_table': 'statement',
            },
        ),
    ]
