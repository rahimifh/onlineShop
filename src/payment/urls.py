from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    # path("", views.paymentCenter),
    path("request/<int:id>", views.payment_process, name="request"),
    path("verify/", views.verify, name="verify"),
]
