from django.urls import path
from .views import home,aboutUs



urlpatterns = [
    path('', home),
    path('aboutus/', aboutUs),

]
