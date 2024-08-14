from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import  AllowAny
from apps.transactions.permissions import UserPermissons
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import serializers
from apps.transactions.models import Transactions
from apps.transactions.serializers import TransactionSerializer
from apps.users.models import User
from django.db import models  # Импортируйте Q

class TransactionsAPIViews(GenericViewSet, 
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [UserPermissons()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        try:
            from_user = get_object_or_404(User, username=str(serializer.validated_data['from_user']))
            to_user = get_object_or_404(User, username=str(serializer.validated_data['to_user']))
            amount = float(serializer.validated_data['amount'])

            if from_user == to_user:
                raise serializers.ValidationError('Нельзя передавать средства самому себе')

            if amount <= 0:
                raise serializers.ValidationError('Сумма перевода должна быть больше нуля')

            if amount > from_user.balance:
                raise serializers.ValidationError('Недостаточно средств для перевода')

            with transaction.atomic():
                if Transactions.objects.filter(from_user=from_user, to_user=to_user, is_completed=False).exists():
                    raise serializers.ValidationError('Транзакция уже завершена')

                from_user.balance -= amount
                to_user.wallet_adress += amount

                from_user.save()
                to_user.save()

                transfer = Transactions(from_user=from_user, to_user=to_user, amount=amount)
                transfer.save()

        except (User.DoesNotExist, ValueError, serializers.ValidationError) as e:
            raise serializers.ValidationError({'detail': str(e)})

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.transactions.models import Transactions
from apps.transactions.serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
from apps.users.models import User

class UserCoinsHistoryAPIView(APIView):
    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, pk=user_id)
        transactions = Transactions.objects.filter(
            models.Q(from_user=user) | models.Q(to_user=user)
        ).order_by('-created_at')
        
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)