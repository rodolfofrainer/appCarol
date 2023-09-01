from django import forms
from .models import ItemCreatedModel, MarketCreatedModel

class createNewItemForm(forms.ModelForm):
    class Meta:
        model = ItemCreatedModel
        fields = ('name', 'price', 'market_id')
        labels = {
            'name': 'Item Name',
            'price': 'Item Price',
            'market_id': 'Market',
        }
        
    
    def __init__(self, user, *args, **kwargs):
        super(createNewItemForm, self).__init__(*args, **kwargs)
        self.fields['market_id'].queryset = MarketCreatedModel.objects.filter(user_id=user.id)
        self.fields['price'].widget.attrs['min'] = 0