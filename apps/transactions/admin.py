from django.contrib import admin
from .models import Transactions

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'amount', 'created_at', 'is_completed']
    list_filter = ['from_user', 'to_user', 'created_at', 'is_completed']
    search_fields = ['from_user__username', 'to_user__username']

admin.site.register(Transactions, TransactionsAdmin)

