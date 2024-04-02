from django.urls import path
from . import views



urlpatterns = [
    path('Payments', views.payment_gate),

]
