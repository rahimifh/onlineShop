from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views
from .views import LikeViewSet, PostViewSet

# ---- ساخت یک کانتینر برای کلاس های DefaultRouter و SimpleRouter -------
router2 = SimpleRouter(trailing_slash=False)
router = DefaultRouter()

router.register(r"post", PostViewSet)

urlpatterns = [
    path("banner/", views.banner),
    path(
        "like/",
        LikeViewSet.as_view({"get": "list", "post": "create"}),
        name="like_list",
    ),
]
urlpatterns += router.urls
