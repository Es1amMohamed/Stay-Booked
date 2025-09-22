from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_account_activation_email(activation_link, user_email):

    send_mail(
        subject="Activate your account",
        message=f" Please click the link below to activate your account : {activation_link}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
    )
