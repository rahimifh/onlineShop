from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from account.models import Account

# class crm(models):
#     phone = models.CharField(max_length=13)
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    image = models.ImageField(
        upload_to='Category/',
        blank=True
    )
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    description = RichTextUploadingField(blank=True)
    Specifications = RichTextUploadingField(blank=True)
    price = models.PositiveBigIntegerField(default=0)
    discount = models.PositiveBigIntegerField(default=0, max_length=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
    def get_final_price(self):
        return abs(int((self.price * (self.discount - 100)) / 100))
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])




class SpecialOrder(models.Model):

    user = models.ForeignKey(Account,  related_name='special',null=True,  on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to="SpecialOrder/", null=True, blank=True)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"

    def __str__(self):
        return self.name




class SpecialSale(models.Model):
    products = models.ManyToManyField(Product, related_name="special")

    