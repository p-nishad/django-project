from django.contrib import admin
from . models import Cart,CartItem, WishlisItem, Wishlist

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')
    
class CartItmeAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['wish_id','date_added']
    list_display_links = ['wish_id','date_added']
    
class WishlistItemAdmin(admin.ModelAdmin):
     list_display = ['user','product','wish']
     list_display_links = ['user','product','wish']

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItmeAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(WishlisItem,WishlistItemAdmin)