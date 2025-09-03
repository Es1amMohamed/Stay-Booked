from .models import *


def my_footer(request):
    my_footer = Settings.objects.last()

    return {"my_footer": my_footer}