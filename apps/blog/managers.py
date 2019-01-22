import datetime
from django.db import models
from django.db.models import Q


class PostManager(models.Manager):
    ''' manager to return only published Posts '''
    def _latest(self, qs):
        """ Private method for filter out future pub dates """
        return qs.filter(publish_date__lte=datetime.datetime.now())

    def latest_public(self):
        """ Only the Latest Public Posts """
        qs = self.filter(is_published=True)
        return self._latest(qs)
