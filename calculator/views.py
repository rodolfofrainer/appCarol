from django.shortcuts import render
from django.contrib import messages
from .forms import createNewItemForm
from .models import ItemCreatedModel

# Create your views here.
def baseView(request):
    return render(request, 'home.html')

def marketPageView(request):
    return render(request, 'market.html')

def comparisonPageView(request):
    return render(request, 'comparison.html')

def createItemPageView(request):
    context = {'form': createNewItemForm()}
    if request.method == 'POST':
        form = createNewItemForm(request.POST)
        if form.is_valid():
            clean_form = form.clean()
            print(clean_form)
            createNewItemForm()
            messages.success(request, f'Item created!')
            return render(request, 'itemCreation.html', context = context)
    else:
        return render(request, 'itemCreation.html', context = context)

def myWagePageView(request):
    return render(request, 'wageHour.html')