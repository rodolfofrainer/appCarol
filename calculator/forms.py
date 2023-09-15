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

class ItemsCalculateForm(forms.Form):
    item = forms.ChoiceField(choices=[])  # Initialize with empty choices
    amount = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ItemsCalculateForm, self).__init__(*args, **kwargs)

        if request:
            queryset = ItemCreatedModel.objects.filter(market_id__user_id=request.user.id)
            items_set = set()
            for item in queryset:
                items_set.add(item.name)

            items_list = sorted(list(items_set))

            if len(items_list) < 1:
                items_list = []

            print(items_list)
            self.fields['item'].choices = [item for item in items_list]