from django.db import models

# Create your models here.


class Business(models.Model):
    name = models.CharField(max_length=50)
    business_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    business_type = models.CharField(max_length=40)
    city = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    sector = models.CharField(max_length=200)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)


def __str__(self):
    return self.business_name
