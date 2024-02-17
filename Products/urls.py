from django.urls import path
from . import views



urlpatterns = [
    path('', views.home),
    path('detail/<int:id>', views.pro_detail),
]
