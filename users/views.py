from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def user_login(request):
    redirect_to = request.GET['next']
    
    if request.method == 'POST':

        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect_to) 
        else:

            #TODO notify person that login info was incorrect
            return render(request, 'users:users-login')

    return render(request, 'users/login.html')

@login_required
def account(request):

    if request.user.is_authenticated:

        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']

            if fname:
                fname = fname[0].upper() + fname[1:].lower()
                request.user.first_name = fname
            if lname:
                lname = lname[0].upper() + lname[1:].lower()
                request.user.last_name = lname
            if email:
                request.user.email = email
            if password:
                ...

            request.user.save()


        current_user = request.user

        context = {}
        context['fname'] = current_user.first_name
        context['lname'] = current_user.last_name
        context['email'] = current_user.email

        return render(request, 'users/account.html', context)

    


def signup(request):

    if request.method == 'POST':

        email = request.POST["email"]
        password = request.POST["password"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]

        User.objects.create_user(email, password, first_name=fname, last_name=lname)

        return redirect('users:users-account', permanent=True)

    return render(request, 'users/signup.html')

def user_logout(request):

    logout(request)

    return redirect('common:common-home')