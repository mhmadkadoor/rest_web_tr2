from django.contrib import admin
from .models import Product, Hotdeals
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category', 'price')
    list_display_links = ('title',)
    list_editable = ('category', "price")
    list_filter = ('category',)
    search_fields = ('title', 'description' 'category',)

class HotdealsAdmin(admin.ModelAdmin):
    list_display = ('title','description', "category", 'oldPrice', 'newPrice', 'end_time')
    list_display_links = ('title',)
    list_editable = ('category', 'oldPrice', 'newPrice',)
    list_filter = ('category',)
    search_fields = ('sender_name', 'description' 'category',)



admin.site.register(Product, ProductAdmin)
admin.site.register(Hotdeals, HotdealsAdmin)
