from django.contrib import admin
from .models import Product, ProductImage

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)