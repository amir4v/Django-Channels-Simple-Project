from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    From  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_messages')
    to  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_messages')
    text = models.TextField(null=False, blank=False)