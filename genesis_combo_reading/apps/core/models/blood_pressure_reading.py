from django.db import models


class BloodPressureReading(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True, db_index=True)
    reading_datetime = models.DateTimeField()
    meid = models.CharField(max_length=255, db_index=True)
    systolic_measurement = models.PositiveIntegerField()
    diastolic_measurement = models.PositiveIntegerField()
    pulse = models.PositiveIntegerField()
    mean_pressure = models.PositiveIntegerField(null=True)
    average_measurement = models.PositiveIntegerField(null=True)
    ihb_index = models.PositiveIntegerField(null=True)
    stiffness_index = models.PositiveIntegerField(null=True)
