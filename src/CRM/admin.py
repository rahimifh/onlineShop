from unicodedata import category
from django.contrib import admin
from .models import consulting,Category
# Register your models here.



@admin.register(consulting)
#------ برای این که داخل پنل ادمین هر کدام از فیلد هایی که در قسمت زیر امده را نشان دهد-------
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastName', 'date','active']
    list_filter = ['date']

admin.site.register(Category)