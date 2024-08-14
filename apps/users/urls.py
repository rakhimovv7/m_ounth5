from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from apps.users.views import UserAPIViewsSet, UserRegisterAPI
from apps.transactions.views import TransactionsAPIViews

router = DefaultRouter()
router.register('user', UserAPIViewsSet, 'api_users')
router.register('transactions', TransactionsAPIViews, 'api_transactions')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='api_users_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_users_refresh'),
    path('register/', UserRegisterAPI.as_view(), name='api_users_register'),
]

urlpatterns += router.urls
