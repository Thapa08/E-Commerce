from django.contrib import admin
from .models import Customer,Product,Order_placed,Cart
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','name','city','district','zip_code','state']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','selling_price','discounted_price','description','brand','category','image']

@admin.register(Order_placed)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']