from django.db import models


# Create your models here.


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


class Search(models.Model):
    address = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class service_detail(models.Model):

    services_id = models.IntegerField(primary_key=True,auto_created=True)
    name = models.CharField(max_length=30, default='0', null=False)
    type = models.CharField(max_length=20,default='0',null=False)
    description = models.CharField(max_length=30, default='0', null=False)

    def __str__(self):
        return self.name
