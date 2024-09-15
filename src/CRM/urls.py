from django.urls import path
from . import views


app_name = "CRM"

urlpatterns =[
    path('',views.crmCenter,name="CRM_center"),
]
