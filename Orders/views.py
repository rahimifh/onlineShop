from django.shortcuts import render

# Create your views here.

def list_of_orders(request):
    return render(request,'Orders/order.html')
