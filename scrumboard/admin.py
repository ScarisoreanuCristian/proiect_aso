from django.contrib import admin
from scrumboard.models import List, Card, Message
# Register your models here.

admin.site.register(List)
admin.site.register(Card)
admin.site.register(Message)