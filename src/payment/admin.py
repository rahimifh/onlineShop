from django.contrib import admin

from .models import  order

# Register your models here.




@admin.register(order)
class orderAdmin(admin.ModelAdmin):
    list_display = [
        # order.__str__,
        "final_price",
        "paid",
        "date_create",
        "Expiration_date",]

