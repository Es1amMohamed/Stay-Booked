
from django.shortcuts import render
from django.core.paginator import Paginator
from rooms.models import *
from .models import *
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    settings = Settings.objects.last()
    hotels = Hotel.objects.all()
    image = Image.objects.all()[:3]
    paginator = Paginator(hotels, 3)
    page = request.GET.get("page")
    page_ogj = paginator.get_page(page)
    context = {"hotels": page_ogj, "settings": settings, "image": image}

    return render(request, "websitesettings/home.html", context)


def services(request):
    services = Services.objects.all()[:3]
    services_2 = Services.objects.all()[3:6]
    services_3 = Services.objects.all()[6:]
    context = {"services": services, "services_2": services_2, "services_3": services_3}
    return render(request, "websitesettings/services.html", context)


def about_us(request):
    hotels = Hotel.objects.all()
    context = {"hotels": hotels}

    return render(request, "websitesettings/about_us.html", context)
