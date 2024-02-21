from django.contrib import admin
from .models import (
    Category,
    Product,
    UserProfile,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
    Subcategory,
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price")
    list_filter = ("category",)
    search_fields = ("title",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating")
    list_filter = ("product", "rating")
    search_fields = ("product__title", "user__username")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Subcategory)
