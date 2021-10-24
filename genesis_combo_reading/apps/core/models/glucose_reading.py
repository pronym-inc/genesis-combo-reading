from django.db import models


class GlucoseReading(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True, db_index=True)
    reading_datetime = models.DateTimeField()
    meid = models.CharField(max_length=255, db_index=True)
    blood_glucose = models.PositiveIntegerField()
    measurement_type = models.PositiveIntegerField()
