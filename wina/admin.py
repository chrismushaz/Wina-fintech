from django.contrib import admin
from .models import Institution, Transaction, Booth

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Booth)
admin.site.register(Institution)