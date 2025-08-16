from django.contrib import admin

from .models import Category, Product


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
