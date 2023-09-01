from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import createNewItemForm
from .models import MarketCreatedModel

# Create your views here.
def baseView(request):
    return render(request, 'home.html')

def marketPageView(request):
    return render(request, 'market.html')

def comparisonPageView(request):
    return render(request, 'comparison.html')

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
    else:
        form = createNewItemForm(request.user, initial={'price': 0})
    context = {'form': form}
    return render(request, 'itemCreation.html', context=context)

def myWagePageView(request):
    return render(request, 'wageHour.html')