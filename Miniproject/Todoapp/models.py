from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    due_datetime = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return self.title
