from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import createNewItemForm

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
            item = form.save(commit=False)
            print(item)
            createNewItemForm()
            messages.success(request, f'Item created!')
            return HttpResponseRedirect('createItem')
    else:
        return render(request, 'itemCreation.html', context = context)

def myWagePageView(request):
    return render(request, 'wageHour.html')