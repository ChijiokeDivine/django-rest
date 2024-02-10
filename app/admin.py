from django.contrib import admin
from .models import Niche, Product, Category, CartOrderItems

admin.site.register(Niche)
admin.site.register(Product)
admin.site.register(Category)

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['item', 'image', 'qty', 'price', 'total']
admin.site.register(CartOrderItems,CartOrderItemsAdmin)