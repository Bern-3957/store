from django.contrib import admin
from .models import ProductCategory, Product, Basket
# Register your models here.


@admin.register(ProductCategory)
class ProductCategory(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'description',)
    search_fields = ('name',)
    ordering = ('name', )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category',)
    fields = ('name', 'description', ('price', 'quantity',), 'image', 'category',)
    # readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
