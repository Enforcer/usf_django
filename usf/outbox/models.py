from django.db import models


class OutboxEntry(models.Model):
    task_name = models.CharField()
    arguments = models.JSONField()
    when_created = models.DateField(auto_now_add=True)
