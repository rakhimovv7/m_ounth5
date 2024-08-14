from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=255, verbose_name='Телефон номера')
    age = models.PositiveIntegerField(verbose_name='Возраст студента', blank=True, null=True)
    direction = models.CharField(max_length=255, verbose_name='Направление')
    balance = models.IntegerField(verbose_name='Баланс', default=4)
    wallet_adress = models.IntegerField(verbose_name='Кошелек', default=0, blank=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


from django.db import models
from apps.users.models import User

class UserCoins(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coins')
    balance = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Coin Info"

    class Meta:
        verbose_name = 'Коин'
        verbose_name_plural = 'Коины'
