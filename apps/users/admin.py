from django.contrib import admin

from apps.users.models import User, UserCoins
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'age', 'direction', 'balance', 'wallet_adress')
    list_filter = ('username', 'phone', 'age', 'direction', 'balance', 'wallet_adress')

@admin.register(UserCoins)
class UserCoinsAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'last_updated')
    search_fields = ('user__username',)
