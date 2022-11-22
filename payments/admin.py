from django.contrib import admin
from .models import Item, Order, OrderItem, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'currency')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', )
    inlines = [OrderItemInline]


@admin.register(Discount)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'percent', )


@admin.register(Tax)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', )

