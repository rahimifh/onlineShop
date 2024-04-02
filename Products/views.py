from django.shortcuts import render
from .models import product
# Create your views here.


def pro_detail(request, id):
    pro = product.objects.get(id = id)
    context = {"product":pro}
    return render(request, "core/detail.html", context)
