from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

@login_required
def createItemPageView(request):
    if request.method == 'POST':
        form = createNewItemForm(request.user, request.POST)
        form.fields['market_id'].queryset = MarketCreatedModel.objects.filter(user_id=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = request.user.id
            item.save()
            messages.success(request, f'Item created!')
            return redirect('create_item')
    
    form = createNewItemForm(request.user, initial={'price': 0})
    
    list_of_markets = MarketCreatedModel.objects.filter(user_id=request.user.id)
    list_of_items = ItemCreatedModel.objects.filter(market_id=list_of_markets[0].id)
    context = {
        'form': form,
        'list_of_markets': list_of_markets,
        'list_of_items': list_of_items,
        }
    return render(request, 'itemCreation.html', context=context)

@login_required
def myWagePageView(request):
    return render(request, 'wageHour.html')