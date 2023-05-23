from django.db import models
from django.contrib.auth.models import User


class History(models.Model):

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    total_area = models.IntegerField()
    number_of_levels = models.IntegerField()
    buildingType = models.IntegerField()
    condition = models.IntegerField()
    ceilings = models.FloatField()
    parking = models.BooleanField()
    firealarm = models.BooleanField()
    security = models.BooleanField()
    video_surveillance = models.BooleanField()
    alarm_system = models.BooleanField()
    optics = models.BooleanField()
    predicted_price = models.IntegerField()

    updated_at = models.DateTimeField(auto_now=True)