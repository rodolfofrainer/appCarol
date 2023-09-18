from rest_framework import serializers

class ItemsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2,
        )
