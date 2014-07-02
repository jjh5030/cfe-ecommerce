from django.contrib import admin
from .models import Order, ShippingStatus

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['order_id']
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Order, OrderAdmin)


class ShippingStatusAdmin(admin.ModelAdmin):
    class Meta:
        model = ShippingStatus

admin.site.register(ShippingStatus, ShippingStatusAdmin)