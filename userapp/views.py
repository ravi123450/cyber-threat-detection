from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
import random
from django.contrib.auth import logout
import pickle
import os
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

import urllib.request
import urllib.parse


def index(request):
    return render(request,'user/index.html')



def about(request):
    return render(request,'user/about.html')



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid details !')
            return redirect('admin_login')
    return render(request,'user/admin-login.html')



def contact(request):
    return render(request,'user/contact.html')

def otp(request):
    user_id = request.session.get('user_id')  # Retrieve the user session ID
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user')
        return redirect('user_register')

    # Preprocess email for masking
    email = user.user_email  # Ensure the `user_email` field exists in the User model
    if email:
        username, domain = email.split('@', 1)  # Split username and domain
        
        # Mask email as per requirement: first letter, '****', last 3 letters before '@', and domain
        if len(username) > 3:
            masked_email = f"{username[:1]}****{username[-3:]}@{domain}"
        else:
            # If the username is less than 4 characters, just mask as much as possible
            masked_email = f"{username[:1]}{'*' * (len(username) - 1)}@{domain}"
    else:
        masked_email = "Email not available"

    if request.method == "POST":
        otp_entered = request.POST.get('otp')  # Get OTP entered by the user
        if str(user.otp) == otp_entered:
            messages.success(request, 'OTP verification and Registration successfully completed!')
            user.status = "Verified"
            user.save()  # Save the updated user instance
            return redirect('user_login')
        else:
            messages.error(request, 'Invalid OTP entered')
            return redirect('otp')

    # Pass preprocessed email to the template
    return render(request, 'user/otp.html', {'user': user, 'masked_email': masked_email})





def services(request):
    return render(request,'user/service.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(user_email=email)   
            if user.user_password == password:
                request.session['user_id'] = user.user_id
                if user.status == 'Accepted':
                    messages.success(request, 'Login Successful')
                    return redirect('user_dashboard')
                elif user.status == 'Pending':
                    messages.info(request, 'Otp verification is compalsary otp is sent to ' + str(user.user_phone))
                    return redirect('otp')
                else:
                    messages.error(request, 'Your account is not approved yet.')
                    return redirect('user_login')
            else:
                messages.error(request, 'Invalid Login Details')
                return redirect('user_login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid Login Details')
            return redirect('user_login')
    return render(request,'user/user-login.html')


def user_dashboard(request):
    return render(request,'user/user-dashboard.html')


def user_profile(request):
    user_id  = request.session['user_id']
    user = User.objects.get(pk= user_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            profile = request.FILES['profile']
            user.user_profile = profile
        except MultiValueDictKeyError:
            profile = user.user_profile
        password = request.POST.get('password')
        location = request.POST.get('location')
        user.user_name = name
        user.user_email = email
        user.user_phone = phone
        user.user_password = password
        user.user_location = location
        user.save()
        messages.success(request , 'updated succesfully!')
        return redirect('user_profile')
    return render(request,'user/user-profile.html',{'user':user})





def generate_otp(length=4):
    otp = ''.join(random.choices('0123456789', k=length))
    return otp




def user_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        location = request.POST.get('address')
        profile = request.FILES.get('profile')
        try:
            User.objects.get(user_email =   email)
            messages.info(request, 'Email Already Exists!')
            return redirect('user_register')
        except:
            otp = generate_otp()
            user = User.objects.create(user_name=name, user_email=email, user_phone=phone, user_profile=profile, user_password=password, user_location=location,otp=otp)
            print(user)
            user_id_new = request.session['user_id'] = user.user_id
            print(user_id_new)
            mail_message = f"Registration Successfully\n Your 4 digit Pin is below\n {otp}"
            send_mail("User Password", mail_message, settings.EMAIL_HOST_USER, [email])
            messages.success(request, "Your account was created..")
            return redirect('otp')
    return render(request,'user/user-register.html')





def user_logout(request):
    logout(request)
    return redirect('user_login')


def cyber_sec(request):
    return render(request,'user/cyber-security.html',{})
