from django.shortcuts import render,redirect
from .models import ContactUs
from django.contrib import messages
from .forms import ContactForm

# Create your views here.
def contactUs(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ContactUs.objects.create(name=cd['name'],email=cd['email'],message=cd['message'])
            messages.success(request, 'Thank you! you have successfully sent your message!')
            return redirect('contact:contactus')
    form = ContactForm(request.POST)
    return render(request,'core/contact.html',{'form':form})
