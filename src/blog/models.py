import datetime
import os
import random

import jdatetime

# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone




def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    BASE_LIST = "0123456789abcdefghijklmnopqrstuvwxyz"
    new_name = "".join(random.choices(BASE_LIST, k=10))
    _, ext = get_filename_ext(filename)
    x = timezone.now()
    final_name = f"blog/{x.year}/{x.month}/{x.day}/{new_name}{ext}"
    return f"{final_name}"


# ======================================================================


class Albom(models.Model):
    Al_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="نام عکس "
    )
    profile_image = models.FileField(max_length=255, upload_to=upload_image_path)

    def __str__(self):
        return self.Al_name


# ======================================================================


class File_Album(models.Model):
    F_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="نام عکس "
    )
    profile_image = models.FileField(upload_to=upload_image_path)

    def __str__(self):
        return self.F_name


# ======================================================================
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    is_top = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name


# ======================================================================

# class BlogPostManager(models.Manager):
#     def get_queryset(self) -> QuerySet:
#         return super().get_queryset().filter(status="publish")


class BlogPost(models.Model):
    STATUS_CHOICES = (("draft", "پیش نویس"), ("publish", "انتشار"))
    category = models.ForeignKey(
        BlogCategory, on_delete=models.RESTRICT, null=True, blank=True
    )
    title = models.CharField(max_length=250, null=True, blank=True)
    summary = models.CharField(
        max_length=400, null=True, blank=True, verbose_name="خلاصه "
    )
    text = RichTextUploadingField(verbose_name="محتوا", null=True, blank=True)
    post_image = models.ImageField(upload_to=upload_image_path)
    is_top = models.BooleanField(default=False, blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True, verbose_name=("تگ"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    date_published = models.DateTimeField(
        default=timezone.now, verbose_name="تاریخ انتشار"
    )
    date_updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft", verbose_name="وضعیت"
    )

    class Meta:
        ordering = ("-date_published",)

    # objects = BlogPostManager()

    def __str__(self):
        return self.title

    @property
    def confirmed_comments(self):
        return self.comments.filter(status="confirmed")

    def JaliliDatepublished(self):
        return jdatetime.date.fromgregorian(
            day=self.date_published.day,
            month=self.date_published.month,
            year=self.date_published.year,
        )

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={"post_id": self.id})


# ======================================================================

# class CommentManager(models.Manager):
#     def get_queryset(self) -> QuerySet:
#         return super().get_queryset().filter(status="confirmed")


class Comment(models.Model):
    STATUS_CHOICES = (("checking", "در حال بررسی"), ("confirmed", "تایید شده"))
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField()
    reply = (
        models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True),
    )
    is_reply = models.BooleanField(default=False, verbose_name="آیا این یک پاسخ است؟")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="checking", verbose_name="وضعیت"
    )

    # objects = CommentManager()

    class Meta:
        ordering = ("date_created",)

    def __str__(self):
        repl = "reply" if self.is_reply else "comment"
        return f'{repl} from "{self.user}" to "{self.post.id}-{self.post}"'


# ======================================================================
class Like(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="likes")
    user = models.CharField(max_length=200, null=True, blank=True)
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return f"like for {self.post}"
