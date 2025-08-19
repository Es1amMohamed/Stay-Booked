from django.shortcuts import render
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required   

def register(request):
    return render(request, 'accounts/register.html')

def login(request):
    Site.objects.all()
    return render(request, 'accounts/login.html')
@login_required
def test(request):
    return render(request, 'accounts/test.html')