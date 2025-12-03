import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser, EmailOTP
from datetime import timedelta
from django.utils import timezone
import smtplib
from email.message import EmailMessage
import ssl


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_via_gmail(to_email, otp_code):
    subject = "Your verification code"
    body = f"Your verification code is: {otp_code}"
    from_email = "hafizovm001@gmail.com"
    app_password = "zjkohhcsgehgycpd"

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    context = ssl._create_unverified_context()  

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(from_email, app_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False


def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')

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
        return render(request, 'register.html', {'email': email, 'error': 'Username already exists!'})

    if CustomUser.objects.filter(email=email).exists():
        return render(request, 'register.html', {'username': username, 'error': 'Email already exists!'})

    user = CustomUser.objects.create_user(username=username, email=email, password=password, is_active=False)
    user.save()

    otp_code = generate_otp()
    EmailOTP.objects.create(user=user, code=otp_code, created_at=timezone.now())

    email_sent = send_otp_via_gmail(email, otp_code)
    if not email_sent:
        user.delete()
        return render(request, 'register.html', {'error': 'Failed to send email. Try again.'})

    request.session['pending_user'] = user.id
    request.session['user_email'] = email
    messages.success(request, 'Verification code sent to your email!')
    return redirect('verify_otp')


def verify_otp_view(request):
    user_id = request.session.get('pending_user')
    if not user_id:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('register')

    user = get_object_or_404(CustomUser, id=user_id)
    try:
        otp_obj = user.otp.latest('created_at')
    except EmailOTP.DoesNotExist:
        messages.error(request, 'No verification code found. Register again.')
        return redirect('register')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()

        if otp_obj.created_at + timedelta(minutes=10) < timezone.now():
            otp_obj.delete()
            user.delete()
            messages.error(request, 'Verification code expired. Please register again.')
            return redirect('register')

        if code == otp_obj.code:
            user.is_active = True
            user.is_email_verified = True
            user.save()
            otp_obj.delete()
            if 'pending_user' in request.session:
                del request.session['pending_user']
            if 'user_email' in request.session:
                del request.session['user_email']
            messages.success(request, 'Email verified! You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid verification code!')

    return render(request, 'verify.html', {'email': user.email})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    email = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, email=email, password=password)
    if user:
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'login.html', {'username': email, 'error': 'Wrong email or password!'})


def logout_view(request):
    logout(request)
    return redirect('login')
