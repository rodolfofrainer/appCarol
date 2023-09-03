from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import createNewItemForm, CreateNewMarketForm
from .models import MarketCreatedModel, ItemCreatedModel

# Create your views here.


def baseView(request):
    return render(request, 'home.html')


@method_decorator(login_required, name='dispatch')
class MarketPageView(View):
    template_name = 'market.html'
    form_class = CreateNewMarketForm

    def get_context_data(self, **kwargs):
        context = {
            'form': self.form_class(),
        }
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={'distance':0,'favorite': 0})
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = request.user
            item.save()
            messages.success(request, f'Market created successfully!')
            print('Market created successfully!')
            return redirect('market_page')
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
    


@login_required
def comparisonPageView(request):
    return render(request, 'comparison.html')


@method_decorator(login_required, name='dispatch')
class CreateItemView(View):
    template_name = 'itemCreation.html'
    form_class = createNewItemForm

    def get_context_data(self, **kwargs):
        context = {}
        try:
            list_of_markets = MarketCreatedModel.objects.filter(
                user_id=self.request.user.id)
            list_of_items = ItemCreatedModel.objects.filter(
                market_id=list_of_markets[0].id)
        except IndexError:
            list_of_markets = []
            list_of_items = []
        context.update({
            'list_of_markets': list_of_markets,
            'list_of_items': list_of_items,
        })
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user, initial={'price': 0.00})
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        form.fields['market_id'].queryset = MarketCreatedModel.objects.filter(
            user_id=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = request.user.id
            item.save()
            messages.success(request, f'Item created successfully!')
            return redirect('create_item')
        else:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)


@login_required
def myWagePageView(request):
    return render(request, 'wageHour.html')
