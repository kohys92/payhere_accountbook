from django.db import models
from users.models import User


class Ledger(models.Model):
    IS_REMOVED = (
        (0, 'exist'),
        (1, 'removed'),
    )

    created_at    = models.DateField(auto_now_add = True)
    note          = models.CharField(max_length = 200)
    income        = models.IntegerField(default = 0, null = True, blank = True)
    expense       = models.IntegerField(default = 0, null = True, blank = True)
    total_income  = models.IntegerField(default = 0, null = True, blank = True)
    total_expense = models.IntegerField(default = 0, null = True, blank = True)
    category      = models.CharField(max_length = 45)
    is_removed    = models.IntegerField(default = 0, choices = IS_REMOVED)
    user          = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ledgers'
