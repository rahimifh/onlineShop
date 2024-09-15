from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path


from .sitemaps import BlogSitemap, StaticSitemap  # import StaticSitemap

sitemaps = {
    "static": StaticSitemap,  # add StaticSitemap to the dictionary
    "blog": BlogSitemap,  # add DynamicSitemap to the dictionary
}

urlpatterns = [
    # **************************MVT******************************
    path("", include("core.urls")),
    path("Dash/", include("dashboard.urls", namespace="dashboard")),
    path("account/", include("account.urls", namespace="account")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("CRM/", include("CRM.urls", namespace="CRM")),
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls", namespace="blog")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
