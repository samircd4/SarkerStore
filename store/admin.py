from django.contrib import admin
from .models import *

# Register your models here.
class ImagesTabularInline(admin.TabularInline):
    model = Images
    list_display = ['product','img']
    
class TagTabularInline(admin.TabularInline):
    model = Tag

class ColorTabularInline(admin.TabularInline):
    model = Color

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

class VeriantTabularInline(admin.TabularInline):
    model = Veriant

class VeriantAdmin(admin.ModelAdmin):
    list_display = ['ram', 'rom']
    
@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesTabularInline, TagTabularInline, ColorTabularInline,VeriantTabularInline]
    list_display = ['name', 'price','stock', 'status', 'createed_at', 'categorie', 'brand', 'image']

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabularInline]
    list_display = ['phone', 'date', 'first_name', 'last_name', 'address', 'city', 'status' ]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'p_number', 'p_tra_id']

admin.site.register(Categorie)
admin.site.register(Brand)
admin.site.register(PriceFilter)

admin.site.register(Images)
admin.site.register(Tag)
admin.site.register(Color, ColorAdmin)
admin.site.register(Veriant, VeriantAdmin)
admin.site.register(OrderItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment, PaymentAdmin)