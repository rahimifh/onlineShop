from django.shortcuts import render

# Create your views here.

def hello(request):
    
    context = {"name": ['siavash', 'mohamad','ali']}
    return render(request,'core/home.html', context)