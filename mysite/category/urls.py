from django.urls import path
from . import views

urlpatterns = [
    
    path('view_category/',views.view_category,name='view_category'),
    path('add_category/',views.add_category,name='add_category'),
    # path('delete_category/<slug:slug>/',views.delete_category,name='delete_category'),
        ]