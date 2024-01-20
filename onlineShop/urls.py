
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products', include('Products.urls')),
    path('', include('Orders.urls')),
    path('payments', include('Payments.urls')),
]
