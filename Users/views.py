from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'you are now logged in successfully!')
            return redirect('homepage:home')
        else:
            messages.error(request,'Username or Password is incorrect! try again...')
    return render(request, 'account/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'you are now logged out successfully!')
    return redirect('homepage:home')
# Create your views here.
