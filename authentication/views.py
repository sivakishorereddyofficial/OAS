from django.shortcuts import render, redirect
from django.contrib.auth import get_user, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages


from . import APIs, utils

from django_otp import user_has_device
from django_otp.oath import totp

@csrf_exempt
def register_user(request):
    test = APIs.regiser_user(request)
    return test


def login_homepage(request):
    print(request.user.is_anonymous)
    if request.user.is_anonymous:
        print("i am some anonymous user")
        return render(request, 'login.html') 
    # if(request.user.is_anonymous):
    #     return render(request, 'login.html')
    # for key in request.session.keys():
    #     del request.session[key]
    else:
        print("i am some anonymous user wrongggggggggg", user_has_device(request.user))

        if not user_has_device(request.user):
            return redirect('complete-setup', permanent=True)

        else:
            return redirect('otp-challenge')


def register(request):
    return render(request, 'signup.html')

def register2fa(request):
    if request.user.is_anonymous:
        return redirect('login')
    if user_has_device(request.user):
        return redirect('otp-challenge')

    user = request.user
    try:
        device = user.totpdevice_set.get()
        totp_qr_url =  device.config_url
    except Exception as e:
        device = user.totpdevice_set.create(confirmed=False)
        totp_qr_url =  device.config_url
    qr_img = utils.generate_qr(totp_qr_url)
    return render(request, 'register2Fa.html', context={'totp_qr_img' : qr_img})

def otp_challenge(request):
    if request.user.is_anonymous:
        return redirect('login')
    if not user_has_device(request.user):
        return redirect('complete-setup')
    return render(request, 'otp_page.html')

def login_verify_user(request):
    res = APIs.authenticate(request)
    print(res, '---------------------')

    status = res.pop('status')
    if not status:
        messages.error(request, res['error'])
        return redirect('login')
    
    login(request, res.pop("user"))
    response = res.pop('response')

    if not response['otp_registered']:
        return redirect('complete-setup')

    return redirect('otp-challenge')

def logout_user(request):
    if request.user.is_anonymous:
        return redirect('login')
    logout(request)
    return redirect('login')

@csrf_exempt
def register_user(request):

    if request.method == 'POST':
        res = APIs.regiser_user(request)
        print(res, "-------------")
        status = res.get('status')
        if status:
            messages.info(request, res.get('user reistered successfully login with your email and password'))
            return redirect('login')
        messages.warning(request, res.get('detail'))
        return redirect("register")
    else:
        return JsonResponse({"detail":"Method Not allowed"}, status=400)



        
