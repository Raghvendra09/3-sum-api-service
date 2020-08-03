from django.db import models
from django.contrib.postgres.fields import JSONField
import datetime
from django.contrib.auth.models import User
# Create your models here.


class Transactions(models.Model):

    input_list = JSONField(blank=True, null=True)
    target = models.IntegerField()
    result = JSONField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    queried_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaction_history'


