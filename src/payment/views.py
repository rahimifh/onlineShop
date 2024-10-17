import datetime
import json
import os

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render




import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from myshop.assets import API_BASE_URL, CALL_BACK_URL
from orders.models import Order

MERCHANT = "746e9bf3-38af-41ca-a2fd-b48a90fcdc6b"
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
CallbackURL = CALL_BACK_URL
@login_required()
def payment_process(request):
    APIBaseUEL = API_BASE_URL
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    final_price = order.get_total_cost() 
    if request.method == "POST":
        req_data = {
            "merchant_id": MERCHANT,
            "amount": final_price * 10,
            "callback_url": CallbackURL,
            "description": f"خرید  {order.user.first_name} ",
            "metadata": {
                "mobile": order.user.username,
               
            },
        }
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req = requests.post(
            url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header
        )
        try:
            authority = req.json()["data"]["authority"]
            order.stripe_id = authority
            order.save()
        except:
            e_code = req.json()["errors"]["code"]
            e_message = req.json()["errors"]["message"]
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
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
        {"order": order, "user": request.user, "baseUrl": APIBaseUEL},
    )
def verify(request):
    Authority = request.GET.get("Authority", None)
    order = Order.objects.get(stripe_id=Authority)
    status = request.GET.get("Status", None)
    if status == "OK":
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_cost() * 10,
            "authority": Authority,
        }
        req = requests.post(
            url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header
        )
        if len(req.json()["errors"]) == 0:
            t_status = req.json()["data"]["code"]
            if t_status == 100:
               
                order.paid = True
                order.save()
                return render(
                    request,
                    "payment/paymentResponse.html",
                    {
                        "message": "پرداخت موفقیت آمیز بود ",
                        "response": str(req.json()["data"]["message"]),
                        "payCode": order.stripe_id,
                        "new_order": order,
                    },
                )
            elif t_status == 101:
       
                order.paid = True
                order.save()
                return render(
                    request,
                    "payment/paymentResponse.html",
                    {
                        "message": "پرداخت موفقیت آمیز بود ",
                        "response": str(req.json()["data"]["message"]),
                        "payCode": order.stripe_id,
                        "new_order": order,
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
                        "new_order": order,
                    },
                )
    return render(
        request,
        "payment/paymentResponse.html",
        {"message": "پرداخت ناموفق ", "response": "", "status": False},
    )


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
