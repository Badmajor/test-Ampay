from django.contrib import admin

from .models import Item, Order, Discount, Tax, OrderItem


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price',)



class ItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    inlines = (ItemInline,)
    list_display = ('price', 'discount', 'tax',)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')

admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)