from django_filters.rest_framework import FilterSet
from .models import Property

class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'country' : ['exact'],
            'city' : ['exact'],
            'price_per_night' : ['lt', 'gt'],
            'max_guests' : ['exact'],
            'rules': ['exact'],
        }