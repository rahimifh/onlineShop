import datetime
import json
import os

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from Products.models import Product
from account.models import Business

from .models import  order

# import pytz


MERCHANT = "84f0fa5b-aec4-48dd-8212-a85b27642f76"
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = "email@example.com"  # Optional
mobile = "09384104825"  # Optional
# Important: need to edit for real server.
CallbackURL = os.environ.get('CALL_BACK_URL')


def paymentCenter(request):
    sub = Product.objects.all()
    return render(request, "payment/subscription_list.html", {"sub": sub})


def send_request(request):
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email},
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(
        url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header
    )
    authority = req.json()["data"]["authority"]

    if len(req.json()["errors"]) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()["errors"]["code"]
        e_message = req.json()["errors"]["message"]
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required(login_url="/account/login/")
def payment_process(request, id):
    APIBaseUEL = os.environ.get('API_BASE_URL')
    
    plan = Product.objects.get(id=id)
    try:
        business = Business.objects.get(account=request.user)
    except:
        return redirect("account:signupBusiness")
    if request.method == "POST":
        code = request.POST.get("code")
        # utc=pytz.UTC
        # now = utc.localize(datetime.datetime.now())
        time_change = datetime.timedelta(days=31)
        new_time = datetime.datetime.now() + time_change
        final_price = plan.final_price
        # if code != "00":
        #     try:
        #         Dis = discount.objects.get(code=code)
        #     except:
        #         return render(
        #             request,
        #             "payment/PurchaseInvoice.html",
        #             {"plan": plan, "business": business, "baseUrl": APIBaseUEL},
        #         )
        #     if Dis.used == True:
        #         return render(
        #             request,
        #             "payment/PurchaseInvoice.html",
        #             {
        #                 "plan": plan,
        #                 "business": business,
        #                 "mess": "این کد تخفیف استفاده شده است.",
        #                 "baseUrl": APIBaseUEL,
        #             },
        #         )
        #     percent = 100 - Dis.percent
        #     final_price = percent * plan.final_price / 100
        #     if Dis.unlimited == False:
        #         Dis.used = True
        #         Dis.save()

        new_order = order.objects.create(
            buyerBussiness=business,
            plan=plan,
            price=plan.price,
            price_after_discount=plan.price_after_discount,
            Taxation=plan.Taxation,
            final_price=final_price,
            Expiration_date=new_time,
        )

        req_data = {
            "merchant_id": MERCHANT,
            "amount": final_price * 10,
            "callback_url": CallbackURL,
            "description": f"خرید اشتراک {plan.title} توسط {business}",
            "metadata": {
                "mobile": business.account.username,
                "email": business.account.email,
            },
        }
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req = requests.post(
            url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header
        )
        print(req.json())
        authority = req.json()["data"]["authority"]
        new_order.authority = authority
        new_order.save()
        req = requests.post(
            url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header
        )
        if len(req.json()["errors"]) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()["errors"]["code"]
            e_message = req.json()["errors"]["message"]
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    return render(
        request,
        "payment/PurchaseInvoice.html",
        {"plan": plan, "business": business, "baseUrl": APIBaseUEL},
    )


def verify(request):
    Authority = request.GET.get("Authority", None)
    Order = order.objects.get(authority=Authority)
    status = request.GET.get("Status", None)
    if status == "OK":
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": Order.final_price,
            "authority": Authority,
        }
        req = requests.post(
            url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header
        )
        if len(req.json()["errors"]) == 0:
            t_status = req.json()["data"]["code"]
            if t_status == 100:
                print("status 100")
                Order.paid = True
                Order.save()
                business = Order.buyerBussiness
                business.SMS_number = business.SMS_number + Order.plan.SMS_number
                if Order.plan.code == "TOT":
                    business.subscription = Order.plan.id
                    business.expiration = Order.Expiration_date
                business.save()
                return render(
                    request,
                    "payment/paymentResponse.html",
                    {
                        "message": "پرداخت موفقیت آمیز بود ",
                        "response": str(req.json()["data"]["message"]),
                        "payCode": Order.authority,
                        "new_order": Order,
                    },
                )
            elif t_status == 101:
                print("status 101")
                Order.paid = True
                Order.save()
                business = Order.buyerBussiness
                business.SMS_number = business.SMS_number + Order.plan.SMS_number
                if Order.plan.code == "TOT":
                    business.subscription = Order.plan.id
                    business.expiration = Order.Expiration_date
                business.save()
                return render(
                    request,
                    "payment/paymentResponse.html",
                    {
                        "message": "پرداخت موفقیت آمیز بود ",
                        "response": str(req.json()["data"]["message"]),
                        "payCode": Order.authority,
                        "new_order": Order,
                    },
                )
            else:
                return render(
                    request,
                    "payment/paymentResponse.html",
                    {
                        "message": "پرداخت ناموفق ",
                        "response": str(req.json()["data"]["message"]),
                        "status": False,
                        "new_order": Order,
                    },
                )
    return render(
        request,
        "payment/paymentResponse.html",
        {"message": "پرداخت ناموفق ", "response": "", "status": False},
    )
