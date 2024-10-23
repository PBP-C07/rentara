from .models import Vehicle
import django_filters

class VehicleFilter(django_filters.FilterSet):
    class Meta:
        model = Vehicle
        fields = ['brand_type', 'brand']
        