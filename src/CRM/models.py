# from pydoc import describe
# from turtle import title
# from unicodedata import category, name
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=150)
    def __str__(self):
        return self.title



class consulting(models.Model):
    name= models.CharField(max_length=30 , verbose_name="نام")
    lastName = models.CharField(max_length=30 , verbose_name="نام خانوادگی")
    phone = models.CharField(max_length=13 , verbose_name="شماره تماس")
    company = models.CharField(max_length=50 , verbose_name="شرکت")
    description =models.TextField(verbose_name="توضیحات")
    date = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ و زمان")
    active = models.BooleanField(default=False,verbose_name="پاسخ داده شده / پاسخ نداده شده")
    category = models.ManyToManyField(Category, verbose_name="عنوان")
