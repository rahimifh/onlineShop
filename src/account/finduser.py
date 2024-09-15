from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from account.models import Business


def FindUser(token):
    userToken = token.split(" ")
    user = Token.objects.get(key=userToken[1])
    return user.user


def check_business(id, user):
    try:
        business = get_object_or_404(Business, id=id, account=user)
    except:
        return (False, "کسب و کار مد نظر متعلق به حساب ارسال کننده درخواست نمی باشد ")
    return (True, business)
