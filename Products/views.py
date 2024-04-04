from django.shortcuts import render
from .models import Product
# Create your views here.


def pro_detail(request, id):
    pro = Product.objects.get(id = id)
    return render(request, "core/detail.html",{'products':pro})
