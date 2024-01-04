from django.shortcuts import render
from users.models import User

def home(request):

    if request.user.is_authenticated:
        user_obj = User.objects.filter(email=request.user.email).first()

        context = {
            'user_has_bikes' : (list(user_obj.bike_set.all()) == [])
        }
    
        return render(request, 'common/home.html', context)

    return render(request, 'common/home.html')

