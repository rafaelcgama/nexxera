from django.contrib import admin
from accountapp.models import Account, Transaction

# Register your models here.
admin.site.register([Account, Transaction])
