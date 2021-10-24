from django.db import models


class LogEntry(models.Model):
    datetime_added = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    decrypted_content = models.TextField(db_index=True, null=True)
    decryption_succeeded = models.BooleanField()
    processing_succeeded = models.BooleanField()
