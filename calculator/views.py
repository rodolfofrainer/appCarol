from django.shortcuts import render

# Create your views here.
def base(request):
    context = {
        'user': request.user, 
        'is_user_authenticated': request.user.is_authenticated
        }
    return render(request, 'home.html', context=context)
