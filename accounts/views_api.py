from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status



@api_view(['POST'])
def register_api(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        current_site = get_current_site(request)
        domain = current_site.domain
        activation_link = f"http://{domain}/accounts/activate/{uid}/{token}/"

        send_mail(
            subject="Activate your account",
            message=f" Please click the link below to activate your account : {activation_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return Response({
            'user': serializer.data,
            'access': str(token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        if not serializer.validated_data['user'].is_active:
            return Response({"error": "Account is not active"}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        login(request, user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'redirect_url': reverse('accounts:test')
        }, status=status.HTTP_200_OK)
        return redirect('accounts:test')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def activate_account(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        print("Account Activated Successfully")
        login(request, user)
        return Response({"success": " Account Activated Successfully"}, status=200)
    else:
        return Response({"error": "Invalid activation link"}, status=400)
    
