from django.contrib import admin

from products.models import Category, Product


class ProductAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


class CategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
