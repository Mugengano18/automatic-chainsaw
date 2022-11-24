from django import forms
from carmed.models import Business, Search


class Retail_info(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'business_name', 'email', 'phone_number', 'business_type', 'city', 'district',
                  'sector']


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['address']
