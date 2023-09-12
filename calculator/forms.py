from django import forms
from decimal import Decimal
from .models import ItemCreatedModel, MarketCreatedModel, UserProfileModel


class CreateNewItemForm(forms.ModelForm):
    class Meta:
        model = ItemCreatedModel
        fields = ('name', 'price', 'market_id')
        labels = {
            'name': 'Item Name',
            'price': 'Item Price',
            'market_id': 'Market',
        }

    def __init__(self, user, *args, **kwargs):
        super(CreateNewItemForm, self).__init__(*args, **kwargs)
        self.fields['market_id'].queryset = MarketCreatedModel.objects.filter(
            user_id=user.id)
        self.fields['price'].widget.attrs['min'] = Decimal('0.00')


class CreateNewMarketForm(forms.ModelForm):
    class Meta:
        model = MarketCreatedModel
        fields = ['name', 'distance', 'favorite']
        labels = {
            'distance': 'Distance in minutes',
        }


class WageForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = ['wage']
        
        labels = {
            'wage': 'What\'s your hourly wage?',
        }