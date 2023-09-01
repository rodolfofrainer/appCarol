from django import forms
from .models import ItemCreatedModel, MarketCreatedModel

class createNewItemForm(forms.ModelForm):
    class Meta:
        model=ItemCreatedModel
        fields = ['name', 'price', 'market_id']
    name = forms.CharField(label='Product name', max_length=100)
    price = forms.FloatField(label='Product price', min_value=0.0)
    market_id = forms.ModelChoiceField(queryset=MarketCreatedModel.objects.all(), empty_label="Select a market", to_field_name="name")