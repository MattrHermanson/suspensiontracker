from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def setup(request):

    return render(request, 'tracker/setup.html')

@login_required
def home(request):

    return render(request, 'tracker/home.html')