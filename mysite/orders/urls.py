from django.urls import path
from. import views


urlpatterns = [ 
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('success/',views.success,name='success'),
    path('view_order/',views.view_order,name='view_order'),
    path('view_payment/',views.view_payment,name='view_payment'),
    path('cancel_order/<int:pk>/',views.cancel_order,name='cancel_order'),
    ]