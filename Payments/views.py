from django.shortcuts import render

# Create your views here.
def payment_gate(request):
    return render(request,'payment.html')