from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

User=get_user_model()

class Business(models.Model):
    business_id = models.IntegerField(primary_key=True,auto_created=True)
    name = models.CharField(max_length=50, null=True)
    business_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=10, null=True)
    business_type = models.CharField(max_length=40, null=True)
    city = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    sector = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(default=0, null=True)
    longitude = models.FloatField(default=0, null=True)


    def __str__(self):
        return self.business_name



class statuses(models.Model):
    status_id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class service_detail(models.Model):
    services_id = models.IntegerField(primary_key=True,auto_created=True)
    service_type = models.CharField(max_length=30,default='0',blank=True,null=True)
    request_sender = models.CharField(max_length=30,default='0',blank=True,null=True)
    phone_number = models.CharField(max_length=10,blank=True,null=True)
    description = models.CharField(max_length=30, default='0', null=False)
    status = models.ForeignKey(statuses, on_delete=models.CASCADE,default="1")
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.request_sender
