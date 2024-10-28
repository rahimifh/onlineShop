from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('aboutus', views.about, name='about'),
    path('list/', views.product_list, name='product_list'),
    path(
        'list/<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category',
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail,
        name='product_detail',
    ),
    path('addorder/', views.add_order, name="add_order"),
    
]
