from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User


def user_login(request):
    if request.method == 'POST':

        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:users-account', permanent=True)
        else:
            return render(request, '')
    
    return render(request, 'users/login.html')
    

def account(request):

    return render(request, 'users/account.html')


def signup(request):

    if request.method == 'POST':

        email = request.POST["email"]
        password = request.POST["password"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]

        User.objects.create_user(email, password, first_name=fname, last_name=lname)

        return redirect('users:users-account', permanent=True)

    return render(request, 'users/signup.html')