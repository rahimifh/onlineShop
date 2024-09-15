from django import template

from .. import models

register = template.Library()


@register.simple_tag
def get_top_posts():
    return models.BlogPost.objects.filter(status="publish", is_top=True)[:3]


@register.simple_tag
def get_tags():
    return models.Tag.objects.all()


@register.simple_tag
def get_categories():
    return models.BlogCategory.objects.all()


@register.simple_tag
def get_archive_dates():
    return models.BlogPost.objects.filter(status="publish").dates(
        "date_published", "month", order="DESC"
    )
