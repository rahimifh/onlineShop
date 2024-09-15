from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import BlogPost


class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.status

    def location(self, obj):
        return "/blog/post_detail/%s" % (obj.id)


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return [
            "core:home",
            "core:aboutUs",
        ]  # returning static pages; home and contact us

    def location(self, item):
        return reverse(item)  # returning the static pages URL; home and contact us
