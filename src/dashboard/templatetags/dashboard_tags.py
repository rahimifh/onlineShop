from django import template
from django.shortcuts import redirect
from django.utils import timezone
from jalali_date import date2jalali

from account import models as account_models
from Products import models as product_models

register = template.Library()


# @register.inclusion_tag("dashboard/_DashHeader.html")
# def include_dashboard_header(request):
#     try:
#         business = account_models.Business.objects.get(account=request.user)
#     except:
#         context = {
#             "remaining_contacts_count": "-",
#             "number_of_new_customers": "-",
#             "last_order_expiration_date": "-",
#             "last_offer_title": "-",
#         }
#         return context

#     business_offers = offer_models.Offer.objects.filter(
#         owner=business.account, end_date__gt=timezone.now()
#     )
#     remaining_contacts_count = business.SMS_number

#     business_orders = business.orders.filter(Expiration_date__gt=timezone.now())
#     if business_orders.exists():
#         last_order = business_orders.last()
#         last_order_expiration_date = date2jalali(last_order.Expiration_date).strftime(
#             "%y/%m/%d"
#         )
#     else:
#         last_order_expiration_date = "سفارش فعالی ندارید"

#     if not business_offers.exists():
#         number_of_new_customers = "کمپین فعالی ندارید"
#         last_offer_title = "کمپین فعالی ندارید."
#     else:
#         last_offer = business_offers.last()
#         number_of_new_customers = last_offer.customers.count()

#         # all_customers_of_business = set(customer for offer in business_offers for customer in offer.Campaign.all())
#         # number_of_customers = len(all_customers_of_business)

#         last_offer_title = last_offer.title

#     context = {
#         "remaining_contacts_count": remaining_contacts_count,
#         "number_of_new_customers": number_of_new_customers,
#         "last_order_expiration_date": last_order_expiration_date,
#         "last_offer_title": last_offer_title,
#     }
#     return context
