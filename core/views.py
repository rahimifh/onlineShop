from django.shortcuts import render
from Products.models import product
# Create your views here.


def home(request):
    products = product.objects.all()
    context = {"products":products}
    return render(request,'core/home.html', context)

def aboutUs(request):
    return render(request, 'core/aboutus.html')


