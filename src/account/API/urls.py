from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (




    get_phone_generate_code_to_login,

)

router = DefaultRouter()

urlpatterns = [

    path("get_phone_generate_code_login/", get_phone_generate_code_to_login,name="get-phone-gen-code-login"),


]
urlpatterns += router.urls
