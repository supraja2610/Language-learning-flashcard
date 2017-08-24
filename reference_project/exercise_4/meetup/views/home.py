from django.shortcuts import render

def home(request):
    context = {
        'next': request.path
    }
    return render(request, 'home/home.html', context)