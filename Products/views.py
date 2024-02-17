from django.shortcuts import render
from .models import product
# Create your views here.

def home(request):
    products = product.objects.all()
    context = {"products":products}
    return render(request,'core/home.html', context)

def pro_detail(request, id):
    pro = product.objects.get(id = id)
    print("*********")
    print(pro.name)
    context = {"product":pro}
    return render(request, "core/detail.html", context)
