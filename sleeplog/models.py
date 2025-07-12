from django.db import models
from django.conf import settings

class SleepLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.FloatField(help_text="Duration in hours")
    quality = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sleep log for {self.user.username} on {self.date}"

    class Meta:
        ordering = ['-date']