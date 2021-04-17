import datetime
import random
import uuid

from Store.models import Customer, Coupons
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.shortcuts import render, redirect
from twilio.rest import Client

otp = 0
phone_number = 0


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            ref = uuid.uuid4().hex
            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif Customer.objects.filter(phone_number=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                Customer.objects.create(user=user, phone_number=phone, referralCode=ref)
                return JsonResponse('true', safe=False)
        else:
            return render(request, 'accounts/user_signup.html')


def send_referral(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        print(phone)
        user = request.user
        customer = Customer.objects.get(user=user)
        refcode = customer.referralCode
        # account_sid = 'ACd9915d30c853769677f3d1a886342df4'
        # auth_token = '36175db6b3cf07e32217d333e048580b'
        # client = Client(account_sid, auth_token)
        #
        # message = client.messages.create(
        #     body=f"Your OTP is {otp}",
        #     from_='+17149301536',
        #     to=f'+917904897551'
        # )
        link = f"http://127.0.0.1:8000/user_referral_signup/{refcode}"
        print(link)
        return redirect('user_profile')


def referral_signup(request, referral):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif User.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif Customer.objects.filter(phone_number=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                customer = Customer.objects.create(user=user, phone_number=phone)
                ref = referral
                if ref is not None:
                    refCoupon = 30
                    Coupons.objects.create(customer=customer, coupon=refCoupon, StartDate=datetime.datetime.now(),
                                           EndDate=datetime.datetime.now())
                    customer.objects.filter(referralCode=ref)
                return JsonResponse('true', safe=False)
        else:
            return render(request, 'accounts/user_signup.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                # return redirect(otp_validate)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        return render(request, 'accounts/user_login.html')


# def admin_login(request):
#     return render(request, 'accounts/admin_login.html')


def otp_generate(request):
    if request.method == 'POST':
        global phone_number
        phone_number = request.POST['phone']
        user1 = Customer.objects.get(phone_number=phone_number)
        baseuser = user1.user
        print(baseuser)
        request.session['Phone'] = phone_number
        if user1 is not None:
            random_number = random.randint(1000, 9999)
            global otp
            otp = random_number
            print(phone_number)
            account_sid = 'ACd9915d30c853769677f3d1a886342df4'
            auth_token = '36175db6b3cf07e32217d333e048580b'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f"Your OTP is {otp}",
                from_='+17149301536',
                to=f'+917904897551'
            )
            print(message.sid)
            print(otp)
            context = {'user': user1}
            print(context)
            return redirect('otp_val')
    else:
        return render(request, 'accounts/otp.html')


def otp_validate(request):
    if request.method == 'POST':
        phone = request.session['Phone']
        print(phone)
        user1 = Customer.objects.get(phone_number=phone)
        baseuser = user1.user
        print(baseuser)
        print(user1)
        user_otp = request.POST['otp']
        print(user_otp)
        global otp
        print(otp)
        print(type(otp), type(user_otp))
        if otp == int(user_otp):
            print('hggg')
            auth.login(request, baseuser)
            return redirect('store')
        return redirect('otp_gen')
        # else:
        #     # error msg
        #     pass
    else:
        return render(request, 'accounts/otp2.html')


def user_signout(request):
    if request.user.is_authenticated:
        user = request.user
        auth.logout(request)
        return render(request, 'store/store.html')
    else:
        return redirect('store')
