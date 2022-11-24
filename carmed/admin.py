from django.contrib import admin

# Register your models here.
from carmed.models import Business, Search

admin.site.register(Business)
admin.site.register(Search)
