from django.urls import path
from . import views



urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>/',views.submit_review,name='submit_review'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('add_product/',views.add_product,name='add_product'),
    path('view_product/',views.view_product,name='view_product'),
    path('view_variation/',views.view_variation,name='view_variation'),
    path('add_variation/',views.add_variation,name='add_variation'),
    path('delete_variation/<int:id>/',views.delete_variation,name='delete_variation'),
    path('view_review/',views.view_review,name='view_review'),
    path('delete_product/<slug:slug>/',views.delete_product,name='delete_product'),
    path('edit_product/<slug:slug>/',views.edit_product,name='edit_product'),
    
]
