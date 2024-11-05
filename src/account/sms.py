from __future__ import absolute_import

import json
import os

# import redis
import requests
from django.conf import settings
from sms_ir import SmsIr


SMS_API_KEY = "wZYwHS1oPJTV5pJ8SJUkdfrZf7Vh2iFzFN84sdUPc9bjE4s8fE6BN8k0KzNm4e1Y"
SMS_LINE_NUMBER = "30007487130094"

def smsSender(number, message, business=None):
    sms_ir = SmsIr(
        api_key=SMS_API_KEY,
        linenumber=SMS_LINE_NUMBER,
    )
    if business == None:
        res = sms_ir.send_sms(
            number=number, message=message, linenumber=SMS_LINE_NUMBER
        )
    else:
        res = sms_ir.send_sms(
            number=number, message=message, linenumber=SMS_LINE_NUMBER
        )
        business.SMS_number -= 1
        business.save()
        if business.SMS_number == 20:
            res = sms_ir.send_sms(
                number=business.account.username,
                message="پیامک شما در اپ   محصولات ارسی رو به اتمام است برای مختل نشدن عملکرد داشبورد خود آن را شارژ کنید",
                linenumber=SMS_LINE_NUMBER,
            )
        elif business.SMS_number == 0:
            sms_ir.send_sms(
                number="09365086743",
                message=f"اس ام اس کسب و کار با ای دی {business.id} به انتها رسید پیگیری کنید ",
                linenumber=SMS_LINE_NUMBER,
            )
    return res


# r = redis.Redis(host='localhost', port=6379, db=0)
def validate_phone(username):
    if username[0] == "0":
        phone = username[1:]
    else:
        phone = username
    return phone


def veri_cod(phone, code, templateId=None):
    phone = validate_phone(phone)
    headers = {"Content-Type": "application/json", "X-API-KEY": SMS_API_KEY}
    newTemplate = 100000
    if templateId != None:
        newTemplate = templateId
    data = {
        "mobile": phone,
        "templateId": newTemplate,
        "parameters": [{"name": "Code", "value": code}],
    }
    response = requests.post(
        "https://api.sms.ir/v1/send/verify", data=json.dumps(data), headers=headers
    )
    json_data = json.loads(response.text)
    return json_data
