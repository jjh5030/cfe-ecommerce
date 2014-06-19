from django.contrib import admin
from .models import Cart

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart

admin.site.register(Cart, CartAdmin)