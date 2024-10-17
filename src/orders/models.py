
from account.models import Account
from coupons.models import Coupon
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(Account, related_name="customer", on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام حانوادگی")
    phone = models.CharField(max_length=15, verbose_name="تلفن")
    address = models.CharField(max_length=250,verbose_name="آدرس")
    postal_code = models.CharField(max_length=20,verbose_name="کد پستی")
    city = models.CharField(max_length=100,verbose_name="شهر")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost_before_discount(self):

        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):

        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount)
        return 0

    def get_total_cost(self):

        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        if not self.stripe_id:
            # no payment associated
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # Stripe path for test payments
            path = '/test/'
        else:
            # Stripe path for real payments
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

    def get_items(self):
        return OrderItem.objects.filter(order=self)
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'shop.Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
