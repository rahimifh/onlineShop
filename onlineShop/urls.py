
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Products.urls')),
    path('orders', include('Orders.urls')),
    path('payments', include('Payments.urls')),
]
