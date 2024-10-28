from django.contrib import admin

from .models import Category, Product,SpecialOrder,SpecialSale

admin.site.register(SpecialSale)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SpecialOrder)
class SpecialOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'discount',
        'available',
        'created',
        'updated',
    ]
    list_filter = ['category','available', 'created', 'updated']
    list_editable = ['price','discount', 'available']
    prepopulated_fields = {'slug': ('name',)}
