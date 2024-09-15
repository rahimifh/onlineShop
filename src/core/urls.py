from django.urls import path
from . import views

app_name = "core"

urlpatterns =[
    path('', views.Core, name="home"),
    path('aboutUs/', views.aboutUs, name="aboutUs"),
    path('vip_projects/<str:switch>', views.vip_projects, name="vip_projects"),
    path('example/', views.examble, name="examble"),
    path('last_games/', views.last_games, name="last_games"),
    path('TemplateDetail/<int:id>/', views.TemplateDetail, name="TemplateDetail"),
    path('priceTable/', views.priceTable, name="priceTable"),

]

