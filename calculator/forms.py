from django import forms

class createNewItemForm(forms.Form):
    choices = (enumerate(('Walmart', 'Target', 'Costco', 'Safeway', 'Whole Foods', 'Trader Joe\'s', 'Other')))
    name = forms.CharField(label='Product name', max_length=100)
    price = forms.FloatField(label='Product price', min_value=0.0)
    market = forms.ChoiceField(label='Market name', choices=choices)