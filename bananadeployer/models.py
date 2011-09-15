import datetime
from django.contrib.auth.models import User

from django.db import models



class BananaHistory(models.Model):
    user = models.ForeignKey(User)
    what = models.TextField('what happened')
    head = models.TextField('git head')
    when = models.DateTimeField('when did it happen',  auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.what




