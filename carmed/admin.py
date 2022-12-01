from django.contrib import admin

# Register your models here.
from carmed.models import Business, service_detail, statuses


class postBusiness(admin.ModelAdmin):
    list_display = ['business_id', 'business_name', 'business_type']
    ordering = ['business_id']

admin.site.register(Business,postBusiness)
admin.site.register(service_detail)
admin.site.register(statuses)



# Register your models here.

