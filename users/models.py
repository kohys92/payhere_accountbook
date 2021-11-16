from django.db import models


class User(models.Model):
    email      = models.EmailField(unique = True)
    password   = models.CharField(max_length = 500)
    last_name  = models.CharField(max_length = 45)
    first_name = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'