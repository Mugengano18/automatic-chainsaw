from django.contrib import admin

# Register your models here.
from carmed.models import Business


class postBusiness(admin.ModelAdmin):
    list_display = ['business_id', 'business_name', 'business_type']
    ordering = ['business_id']

admin.site.register(Business,postBusiness)
admin.site.register(service_detail)



# Register your models here.

