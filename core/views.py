from django.shortcuts import render
from Products.models import Product
# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request,'core/home.html', {'products':products})

def aboutUs(request):
    return render(request, 'core/aboutus.html')