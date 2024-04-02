from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request,'Invalid username or Password')
            return redirect('users:login')
        else:
            login(request, user)
            messages.success(request,'You are now logged in successfully!')
            return redirect('homepage:home')

    return render(request,'account/login.html')

def log_out(request):
    logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('homepage:home')
