from . import models

from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password

from rest_framework.exceptions import ValidationError, PermissionDenied

from django_otp import user_has_device, match_token, devices_for_user, verify_token
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import messages
import qrcode

from django.views.decorators.csrf import csrf_exempt
from django.core import exceptions
import base64
import json


# rest framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

#simple jwt imports
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

def authenticate(request) -> dict:

    data = request.POST

    print(data, "------------")
    email = data.get('email') or None
    password = data.get('password') or None

    res = dict()

    if (email is None) or (password is None):

        raise ValidationError("email and password are needed for login")

    user = models.User.objects.filter(email=email)

    if not user.exists():
        res['status'] = False
        res['error'] = "user does not exist, Please singup"
        return res

    user = user.first()
    password_check = user.check_password(password)
    if not password_check:
        res['status'] = False
        res['error'] = "Invalid password"
        return res

    totp_registered_status = user_has_device(user)

    if not totp_registered_status:
        request.user = user
        res['user'] = user
        res['status'] = True
        # request.
        data = {
            'otp_registered' :  not user_has_device(user), 
        }
        res['response'] = data
        return res

    request.user = user
    res['user'] = user
    data = {
        'otp_registered' :  user_has_device(user),
        
    }
    res['response'] = data
    res['status'] = True
    return res

@csrf_exempt
def regiser_user(request) -> dict:
    
    data = request.POST
    email = data.get('email') or None
    first_name = data.get('fname') or None
    last_name = data.get('lname') or None
    password = data.get('password') or None
    conf_password = data.get('confPassword') or None

    print(data, "======================")

    if (email is None) or \
        (first_name is None) or \
        (last_name is None) or \
        (password is None) or \
        (conf_password is None):
        return {'status': False, "detail" : 'required fileds are missing' ,'code':400}
    if (password != conf_password):
        return {'status': False, "detail" : 'password and confirm password is not matching' ,'code':400}
    
    try:
        validate_password(password)
    except Exception as weak_password:
        # print(weak_password)
        return {'status':False, "detail":"password is too weak." + " ".join(weak_password)}
    
    check_user = models.User.objects.filter(email=email)

    if check_user.exists():
        return {'status': False, "detail": "user with email already exists."}

    new_user_obj = {
        'username' : first_name + "_" + last_name,
        'email' : email,
        'first_name' : first_name,
        'last_name' : last_name
    }

    user = models.User(**new_user_obj)
    user.set_password(password)
    user.save()

    # device = user.totpdevice_set.create(confirmed=False)
    # url = device.config_url
    device = TOTPDevice.objects.create(user=user, name=first_name + '_default',confirmed=False )
    device.save()
    url = device.config_url
    return  {"status":True, 'url': url}


def confirm_otp(request):

    totp = request.GET['otpTestVerify'] or None
    user = request.user
    user = models.User(id=user.id)
    auth_device = dict()
    user_devices = list(devices_for_user(user, confirmed=False))
    
    for device in user_devices:
        flag = device.verify_token(totp)
        print(flag, "------------++++++")
        if flag:
            auth_device['id'] = device.id
            auth_device['device'] = device
            break
    
    validated_device_id = auth_device.get('id') or None
    if validated_device_id is None:
        messages.warning(request, "invalid OTP try adding device again! or wait for next otp")
        return redirect('complete-setup')
    update_device = TOTPDevice.objects.filter(id=validated_device_id)
    update_device.update(confirmed=True)
    messages.success(request, "Congrats your data is saved! proceed login with this device")
    return redirect('login')

@csrf_exempt
# @api_view(['POST'])
def verify_otp(request):

    data = json.loads(request.body.decode('utf-8'))
    otp = data.get('otp')
    print(data)
    user = request.user

    print(request.user)
    user = models.User.objects.filter(id=user.id)
    if not user.exists():
        raise ValidationError("invalid user")
    user = user.first()

    auth_device = dict()
    user_devices = list(devices_for_user(user, confirmed=True))
    print(user_devices)
    for device in user_devices:
        flag = device.verify_token(otp)
        # print(flag, otp, "------------++++++")
        if flag:
            auth_device['id'] = device.id
            auth_device['device'] = device
            break

    validated_device_id = auth_device.get('id') or None
    print(validated_device_id, "======")
    if validated_device_id is None:
        return JsonResponse({"status":False, "detail":"invalid auth code"})
    
    res = JsonResponse({
        'status':True,
        'oas_refresh' : str(RefreshToken.for_user(user)),
        'redirect_url' : 'home/'
    })
    res.set_cookie('oas_access', str(AccessToken.for_user(user)))
    res['Authorization'] = 'oas_access '+str(AccessToken.for_user(user))
    return res

    
    

    

    