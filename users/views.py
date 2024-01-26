from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.urls import reverse


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
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')

@login_required
def account(request):

    if request.method == 'POST':
        if 'edit_info_button' in request.POST:
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
            return redirect('users:users-account')
        elif 'account_info_button' in request.POST:
            weight = request.POST['weight']

            request.user.weight = weight
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
        send_mail('Thanks for Using SuspensionTracker.com', "You've made an account at SuspensionTracker.com, time to throw away that old notepad with your settings on it.", '', [request.user.email], fail_silently=False)

        return redirect('users:users-account', permanent=True)

    return render(request, 'users/signup.html')

def user_logout(request):

    logout(request)

    return redirect('common:common-home')


def reset_link(request):
    
    #TODO: add domain https://suspensiontracker.com infront of pass_reset_url
    pass_reset_url = reverse('users:users-reset_pass')
    user_id = f'?key={request.user.id}'


    send_mail('Suspension Tracker Password Reset', f'Click this link to reset your password\n {pass_reset_url + user_id}', '', [request.user.email], fail_silently=False)

    return redirect('users:users-account')

def reset_pass(request):

    key = request.GET['key']

    if request.method == 'POST':

        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if pass1 == pass2:
            selected_user = User.objects.get(id=key)
            selected_user.set_password(pass1)
            selected_user.save()
            return redirect('users:users-account')

    return render(request, 'users/reset.html')

def forgot_pass(request):

    if request.method == 'POST':
        email = request.POST['email']
    
        forgotten_user = User.objects.get(email=email)

        pass_reset_url = reverse('users:users-reset_pass')
        user_id = f'?key={forgotten_user.id}'

        send_mail('Suspension Tracker Password Reset', f'Click this link to reset your password\n {pass_reset_url + user_id}', '', [forgotten_user.email], fail_silently=False)
        
        login_url = reverse('users:users-login')
        var = '?next=/users/account/'

        return redirect(login_url+var)        

    return render(request, 'users/forgotPass.html')