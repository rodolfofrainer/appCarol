from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import CreateNewItemForm, CreateNewMarketForm, WageForm
from .models import MarketCreatedModel, ItemCreatedModel, UserProfileModel

# Create your views here.


class basePageView(View):
    template_name = 'home.html'
    context = {}
    
    def get(self, request, **kwargs):
        queryset = ItemCreatedModel.objects.filter(market_id__user_id=request.user.id)
        items_set = []
        for i in queryset:
            items_set.append(i.name)
        items_set = set(items_set)
        self.context['items'] = sorted(list(items_set))
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class MarketPageView(View):
    template_name = 'market.html'
    form_class = CreateNewMarketForm

    def get_context_data(self, **kwargs):
        context = {'form': self.form_class(),}
        context['list_of_markets'] = MarketCreatedModel.objects.filter(
                user_id=self.request.user.id)
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
    form_class = CreateNewItemForm
    context = {}

    def get_context_data(self, **kwargs):
        list_of_markets = []
        list_of_items = {}
        try:
            list_of_markets = MarketCreatedModel.objects.filter(
                user_id=self.request.user.id)
            for market in list_of_markets:
                list_of_items[market.name] = ItemCreatedModel.objects.filter(
                    market_id=list_of_markets[market.id])
        except IndexError:
            pass
        self.context['list_of_markets'] = list_of_markets

        return self.context

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


@method_decorator(login_required, name='dispatch')
class myWagePageView(View):
    template_name = 'wageHour.html'
    form_class = WageForm

    def get_context_data(self, **kwargs):
        user_wage = UserProfileModel.objects.get(user=self.request.user).wage
        context = { 'wage': user_wage }
        return context
    
    def get(self, request, *args, **kwargs):
        user_profile = UserProfileModel.objects.get(user=request.user)
        initial_data = {'wage': user_profile.wage}
        form = self.form_class(initial=initial_data)
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user_profile = UserProfileModel.objects.get(user=request.user)
    
        if form.is_valid():
            item = form.save(commit=False)
            user_profile.wage = item.wage
            user_profile.save()
            messages.success(request, 'Wage updated successfully!')
            return redirect('mywage_page')

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context=context)
