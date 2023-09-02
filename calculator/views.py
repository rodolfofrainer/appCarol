from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import createNewItemForm
from .models import MarketCreatedModel, ItemCreatedModel

# Create your views here.
def baseView(request):
    return render(request, 'home.html')

@login_required
def marketPageView(request):
    return render(request, 'market.html')

@login_required
def comparisonPageView(request):
    return render(request, 'comparison.html')

@method_decorator(login_required, name='dispatch')
class CreateItemView(View):
    template_name='itemCreation.html'
    form_class = createNewItemForm
    
    def get_context_data(self, **kwargs):
        context={}
        list_of_markets = MarketCreatedModel.objects.filter(user_id=self.request.user.id)
        list_of_items = ItemCreatedModel.objects.filter(market_id=list_of_markets[0].id)
        context.update({
            'list_of_markets': list_of_markets,
            'list_of_items': list_of_items,
        })
        return context
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user, initial={'price': 0.00})
        context=self.get_context_data()
        context['form']=form
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        form.fields['market_id'].queryset = MarketCreatedModel.objects.filter(user_id=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = request.user.id
            item.save()
            messages.success(request, f'Item created!')
            return redirect('create_item')
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)

@login_required
def myWagePageView(request):
    return render(request, 'wageHour.html')