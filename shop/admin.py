from django.contrib import admin

from shop import models


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'price',
    )

    search_fields = ('name',)
    empty_value_display = 'None'


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'discount_name',
        'val',
    )

    search_fields = ('discount_name',)
    empty_value_display = 'None'


class TaxAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'tax_name',
        'val',
    )

    search_fields = ('tax_name',)
    empty_value_display = 'None'


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'order_currency',
        'is_complite',
    )
    empty_value_display = 'None'


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'order_id',
        'item_id',
        'qty',
    )
    empty_value_display = 'None'


admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Discount, DiscountAdmin)
admin.site.register(models.Tax, TaxAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItems, OrderItemsAdmin)
