import random
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, EmailOTP


def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if not username or not email or not password:
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'error': 'All fields are required!'
            })

        if password != confirm:
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'error': 'Passwords do not match!'
            })

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'email': email,
                'error': 'Username already exists!'
            })

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'username': username,
                'error': 'Email already exists!'
            })

        user = CustomUser(
            username=username,
            email=email,
            is_active=False
        )
        user.set_password(password)
        user.save()

        otp_code = str(random.randint(100000, 999999))
        EmailOTP.objects.create(user=user, code=otp_code)

        send_mail(
            subject="Your verification code",
            message=f"Your verification code is: {otp_code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect(f"/verify/{user.id}/")


def verify_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    otp = user.otp 

    if request.method == 'GET':
        return render(request, "verify.html", {"email": user.email})

    elif request.method == 'POST':
        code = request.POST.get("code")

        if otp.is_expired():
            return render(request, "verify.html", {
                "error": "The code has expired. Register again.",
                "email": user.email
            })

        if code == otp.code:
            user.is_active = True
            user.is_email_verified = True
            user.save()
            otp.delete()
            return redirect("login")  

        return render(request, "verify.html", {
            "error": "Invalid code!",
            "email": user.email
        })

