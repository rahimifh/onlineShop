import datetime
import os
import random

import jdatetime
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    BASE_LIST = "0123456789abcdefghijklmnopqrstuvwxyz"
    new_name = "".join(random.choices(BASE_LIST, k=10))
    name, ext = get_filename_ext(filename)
    x = datetime.datetime.now()
    final_name = f"Account/{x.year}/{x.month}/{x.day}/{new_name}{ext}"
    return f"test/{final_name}"


class MyAccountManager(BaseUserManager):
    """
    customize create
    """

    def craete_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.craete_user(
            username=username,
            # email = email,
            password=password,
        )
        user.is_Business = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    return f"profile_image/{self.pk}/profile_image.png"


def get_default_profile_image():
    return "profile_default/profile_img_default.jpg"


class Account(AbstractBaseUser):
    name = models.CharField(max_length=40, verbose_name="نام")
    last_Name = models.CharField(max_length=40, verbose_name="نام خانوادگي")
    # STATUS=(('student','Student'),('teacher','Teacher'),)
    username = models.CharField(verbose_name="نام كاربري", max_length=30, unique=True)
    # IID = models.CharField(verbose_name="ایدی",max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    # side =models.CharField(max_length = 10, choices=STATUS, default='student')
    phone = models.CharField(max_length=13, verbose_name="تلفن")
    country = models.CharField(max_length=20, verbose_name="کشور")
    city = models.CharField(max_length=20, verbose_name="شهر")
    email = models.EmailField(verbose_name="ایمیل", max_length=60)
    birthday = models.DateTimeField(verbose_name="تاریخ تولد", null=True, blank=True)
    gender = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="جنسیت"
    )
    education = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="تحصیلات"
    )
    social_media = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="ای دی شبکه اجتماعی"
    )
    address = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="آدرس"
    )
    is_EmailVerified = models.BooleanField(default=False)
    is_Business = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        max_length=255,
        upload_to=get_profile_image_filepath,
        null=True,
        blank=True,
        default=get_default_profile_image,
    )
    

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return f"{self.id} / {self.username}"

    def get_profile_image_filename(self):
        return str(self.profile_image)[
            str(self.profile_image).index("profile_image/" + str(self.pk) + "/") :
        ]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def Jalilibirthday(self):
        return jdatetime.date.fromgregorian(
            day=self.birthday.day, month=self.birthday.month, year=self.birthday.year
        )


class Category(models.Model):
    CATEGORY_LIST = (("فروشگاه", "فروشگاه"), ("خدمات", "خدمات"), ("تولیدی", "تولیدی"))
    title = models.CharField(max_length=30, verbose_name="نام دسته بندی")
    Maincategory = models.CharField(
        max_length=20, choices=CATEGORY_LIST, verbose_name="نوع کسب و کار"
    )

    def __str__(self):
        return self.title


class Business(models.Model):
    LEVEL = (("a", "A"), ("b", "B"), ("c", "C"), ("d", "D"), ("e", "E"))
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="businesses", on_delete=models.CASCADE
    )
    B_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="نام کسب و کار "
    )
    subscription = models.PositiveIntegerField(default=1, verbose_name="ای دی اشتراک")
    expiration = models.DateTimeField(
        null=True, blank=True, verbose_name="انقضای اشتراک"
    )
    SMS_number = models.IntegerField(default=100, verbose_name="تعداد اس ام اس")
    category = models.ManyToManyField(Category, blank=True, verbose_name=" دسته کسب و کار ")
    Nationalcode = models.CharField(max_length=20, verbose_name="کد ملی")
    web_address = models.CharField(max_length=200, null=True, blank=True)
    social_network = models.CharField(max_length=200, null=True, blank=True)
    shop_address = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    B_phone = models.CharField(max_length=13, verbose_name="تلفن")
    Business_level = models.CharField(
        max_length=20, choices=LEVEL, default="e", verbose_name="امتیاز"
    )
    online = models.BooleanField(null=True, default=None)
    ofline = models.BooleanField(null=True, default=None)
    VIP = models.BooleanField(null=True, blank=True)
    profile_image = models.ImageField(
        max_length=255,
        upload_to=upload_image_path,
        null=True,
        blank=True,
        default=get_default_profile_image,
    )
    

    
    sms_template = models.PositiveIntegerField(default=100000, verbose_name="کد قالب sms")

    def __str__(self):
        return f"{self.B_name}"


# Create your models here.
class ver_code(models.Model):
    phone = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    offer = models.BooleanField(default=False)
    offerId = models.PositiveIntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

class sitesToken(models.Model):
    siteUrl = models.CharField(max_length=100)
    Token = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.siteUrl
