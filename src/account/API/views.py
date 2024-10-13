import datetime
import random



from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect
from account.sms import veri_cod
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from account.models import Account, ver_code
import pytz
utc=pytz.UTC
# -------------------------------------------------------------------------


def FindUser(token):
    userToken = token.split(" ")
    user = Token.objects.get(key=userToken[1])
    return user.user


# -------------------------------------------------------------------------


def generate_otp():
    code = str(random.randrange(100000, 999999))
    return code


# -------------------------------------------------------------------------


def check_phone(number) -> (bool, None | Account):
    try:
        user = Account.objects.get(username=number)
        return (True, user)
    except:
        return (False, None)


# -------------------------------------------------------------------------


@api_view(["POST"])
@permission_classes((AllowAny,))
def get_phone_generate_code_to_login(request):
    """{
    "mobile": "090000000000"
    }"""
    data = request.data
    mobile = data["mobile"]
    result, user = check_phone(mobile)
    if result:
        # User is already registered in the system.
        if request.user.username == user.username:
            return Response(
                data={"response": "شما هم اکنون در حساب کاربری خود هستید."},
                status=status.HTTP_200_OK,
            )

        last_user_code = ver_code.objects.filter(phone=mobile).last()
        wait_time = datetime.timedelta(minutes=2)
        if (
            last_user_code is not None
            and (last_user_code.date_created + wait_time) > utc.localize(datetime.datetime.now())
        ):
            return Response(
                data={
                    "response": "از ارسال کد قبلی شما بیشتر از ۲ دقیقه سپری نشده است."
                },
                status=status.HTTP_200_OK,
            )

        code = generate_otp()
        x = veri_cod(phone=mobile, code=code, templateId=100000)
        print(x)
        ver_code.objects.create(phone=mobile, code=code)
        return Response(
            data={
                "response": "کد یکبار مصرف برای شما ارسال شد و پس از ۲ دقیقه منقضی خواهد شد",
                "ok": True,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            data={"response": "این شماره نادرست است یا وجود ندارد!"},
            status=status.HTTP_200_OK,
        )


# -------------------------------------------------------------------------

