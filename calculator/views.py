from django.shortcuts import render

# Create your views here.
def baseView(request):
    return render(request, 'home.html')

def marketPageView(request):
    return render(request, 'market.html')

def comparisonPageView(request):
    return render(request, 'comparison.html')

def createItemPageView(request):
    return render(request, 'itemCreation.html')

def myWagePageView(request):
    return render(request, 'wageHour.html')