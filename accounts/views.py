from django.shortcuts import render
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required   
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

def register(request):
    return render(request, 'accounts/register.html')

def login(request):
    Site.objects.all()
    return render(request, 'accounts/login.html')

@login_required
@permission_classes([IsAuthenticated])
def change_password_view(request):
    return render(request, 'accounts/password_change_form.html')


def password_reset(request):
    return render(request, 'accounts/password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
    return render(request, 'accounts/password_reset_confirm.html', {"uidb64": uidb64, "token": token})

def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')
