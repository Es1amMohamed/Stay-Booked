from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_new_room_email(hotel_name, room_name, room_price, room_id, guest_username, guest_email):
    subject = f"New Room Available at {hotel_name}"
    message = f"""
        Hello {guest_username},

        A new room has just been added at {hotel_name}!

        Room: {room_name}
        Price: {room_price}

        Check it out here: http://127.0.0.1:8000/rooms/{room_id}/
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[guest_email],
        fail_silently=True,
    )


@shared_task
def send_reservation_confirmation_email(user_email,username, reservation_id, room_id, check_in, check_out):
    subject = "Reservation Confirmation"
    message = f"""
        Dear {username},

        Your reservation has been created successfully.
        Reservation ID: {reservation_id}
        Room ID: {room_id}
        Check-in: {check_in}
        Check-out: {check_out}

        Thank you for booking with us!
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=True,
    )