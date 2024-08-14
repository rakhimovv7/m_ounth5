from django.db import models
from apps.users.models import User

class Transactions(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_completed:
            raise ValueError("Transaction is already completed.")
        
        if self.amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")
        
        from_user = self.from_user
        to_user = self.to_user

        # Check if the from_user has enough balance
        if from_user.balance < self.amount:
            raise ValueError("Insufficient funds for the transaction.")

        # Process the transaction
        from_user.balance -= self.amount
        to_user.wallet_adress += self.amount

        self.is_completed = True

        from_user.save()
        to_user.save()

        super(Transactions, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
