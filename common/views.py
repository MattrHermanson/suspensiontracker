from django.shortcuts import render, redirect
from users.models import User
from django.core.mail import send_mail

def home(request):

    if request.user.is_authenticated:
        user_obj = User.objects.filter(email=request.user.email).first()

        context = {
            'user_has_bikes' : (list(user_obj.bike_set.all()) == [])
        }
    
        return render(request, 'common/home.html', context)

    return render(request, 'common/home.html')


def contact(request):

    if request.method == 'POST':

        fname = request.POST['firstname']
        lname = request.POST['lastname']
        subject = request.POST['subject']
        msg = request.POST['msg']

        
        send_mail(f'[Suspension Tracker Contact] ({fname} {lname}) {subject}', msg, '', ['matth2004@outlook.com'], fail_silently=False)
        return redirect('common:common-contact')

    return render(request, 'common/contact.html')


def feedback(request):

    if request.method == 'POST':
        
        feedback_type = request.POST['feedback_type']
        desc = request.POST['desc']

        send_mail(f'[Suspension Tracker {feedback_type.capitalize()}]', desc, '', ['matth2004@outlook.com'], fail_silently=False)
        return redirect('common:common-feedback')

    return render(request, 'common/feedback.html')