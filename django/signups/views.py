from django.shortcuts import render
from signups.models import User


def index(request):
    if request.POST:
        user = User(email=request.POST['email'])
        user.save()
        return render(request, 'signups/signed_up.html', {})
    else:
        return render(request, 'signups/index.html', {})
