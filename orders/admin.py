from django.contrib import admin

from .models import Item, Order


class ItemInline(admin.TabularInline):
    model = Item
    fields = ["product", "quantity"]
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    readonly_fields = ["total"]


admin.site.register(Order, OrderAdmin)
