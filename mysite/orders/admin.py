from django.contrib import admin
from.models import Payment,Order,OrderProduct

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct  
    extras = 0
class OrderAdmin(admin.ModelAdmin):
    list_display =  ['order_number','full_name','phone','email','city','order_total','shipping','status','is_ordered']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number','first_name','email','phone']
    readonly_fields =['is_ordered','order_total']
    list_display_links = ['order_number','full_name','phone','shipping','email','city','order_total']
    inlines = [OrderProductInline]
    list_per_page = 20

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','amount','order_id','razorpay_payment_id','paid']
    list_filter = ['user','amount','paid']
    search_fields = ['user','amount','email','city']
    list_display_links = ['user','amount','order_id']
    list_per_page = 20
    
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity','product_price','ordered']
    list_filter =['user','product']
    
              

          
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Payment,PaymentAdmin)