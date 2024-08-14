from django.urls import path
from apps.transactions.views import TransactionsAPIViews, UserCoinsHistoryAPIView

urlpatterns = [
    path('coins/<int:user_id>/coin/', UserCoinsHistoryAPIView.as_view(), name='user-coins-history'),
]