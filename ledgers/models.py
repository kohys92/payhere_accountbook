from django.db import models

from users.models import User


class Ledger(models.Model):
    date     = models.DateField(auto_now_add = True)
    note     = models.CharField(max_length = 200)
    income   = models.IntegerField(default = 0, null = True, blank = True)
    expense  = models.IntegerField(default = 0, null = True, blank = True)
    total    = models.IntegerField()
    category = models.CharField(max_length = 45)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ledgers'
