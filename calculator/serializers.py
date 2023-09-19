from rest_framework import serializers

from calculator.models import ItemCreatedModel


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCreatedModel
        fields = ['pk', 'market_name', 'name', 'price',  'market_id']

    market_name = serializers.SerializerMethodField(
        method_name='get_market_name')

    def get_market_name(self, item: ItemCreatedModel):
        return item.market_id.name.title()
