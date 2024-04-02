from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [

    path('detail/<int:id>', views.pro_detail,name='detail'),
]
