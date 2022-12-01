from django import forms
from carmed.models import Business, service_detail


class Retail_info(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'business_name', 'email', 'phone_number', 'business_type', 'city', 'district',
                  'sector']
        

class ServiceForm(forms.ModelForm):
    class Meta:
        model = service_detail
        fields = ['name','type','description']




from django.db import models

# Create your models here.


