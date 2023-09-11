import django_filters
from .models import ItemCreatedModel

class ItemCreatedFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = ItemCreatedModel
        fields = ['price', 'market_id']