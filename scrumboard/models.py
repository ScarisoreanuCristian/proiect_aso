import json
from datetime import datetime

from django.db import models


# Create your models here.

class List(models.Model):
    name = models.CharField(max_length=50)


class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # relation with foreign key below
    # EACH Card must belong to a List
    list = models.ForeignKey(List, related_name="cards", on_delete=models.CASCADE)
    story_pints = models.IntegerField(null=True, blank=True)
    business_value = models.IntegerField(null=True, blank=True)


class Message(models.Model):
    value = models.CharField(max_length=100000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    from_user = models.IntegerField(default=None)
    to_user = models.IntegerField(default=None)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
