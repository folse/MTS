from django.db import models

from django.contrib.auth.models import User

import datetime

class PayAccount(models.Model):
    user = models.ForeignKey(User)
    real_name = models.CharField(max_length=32, db_index=True)
    identity_card = models.CharField(max_length=32, db_index=True)
    bank = models.CharField(max_length=32, db_index=True)
    pay_name = models.CharField(max_length=32, db_index=True)
    pay_account = models.CharField(max_length=32, db_index=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    
    def save(self, force_insert=False, force_update=False):
        super(PayAccount, self).save(force_insert, force_update)