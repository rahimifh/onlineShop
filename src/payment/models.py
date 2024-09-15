from django.db import models

from account.models import Business
from Products.models import Product



class order(models.Model):
    Seller = models.CharField(
        max_length=20, default="استارتاپ  ارسی", verbose_name="فروشنده"
    )
    Seller_National_Code = models.CharField(
        max_length=11, default="111", verbose_name="شناسه ملی"
    )
    buyerBussiness = models.ForeignKey(
        Business, related_name="orders", on_delete=models.DO_NOTHING
    )
    products = models.ManyToManyField(
        Product, related_name="products"
    )
    paid = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")
    price = models.PositiveBigIntegerField(verbose_name="قیمت")
    discount = models.PositiveBigIntegerField(verbose_name="تخفیف")
    price_after_discount = models.PositiveIntegerField(
        verbose_name="قیمت بعد از اعمال تخفیف"
    )
    Taxation = models.PositiveBigIntegerField(verbose_name="مالیات")
    final_price = models.PositiveBigIntegerField(verbose_name="قیمت نهایی")
    date_create = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    Expiration_date = models.DateTimeField(
        verbose_name="تاریخ انقضا", null=True, blank=True
    )
    authority = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id} - {self.buyerBussiness}"

    def Meta():
        verbose_name = "سفارش ها"


# class discount(models.Model):
#     code = models.CharField(max_length=20, unique=True)
#     subscriptions = models.ManyToManyField(
#         order, related_name="discounts", verbose_name="اشتراک ها"
#     )
#     percent = models.PositiveSmallIntegerField()
#     unlimited = models.BooleanField(default=False, verbose_name="تخفیف نامحدود")
#     used = models.BooleanField(default=False, verbose_name="استفاده شده")

#     def __str__(self):
#         return self.code
