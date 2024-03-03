from django.contrib import admin
from store.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')
admin.site.register(Product,ProductAdmin)
