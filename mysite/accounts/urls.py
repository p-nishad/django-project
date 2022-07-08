from django.urls import path
from. import views

urlpatterns =[
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('otp/',views.otp,name='otp'),
    
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),  
    path('my_orders/',views.my_orders,name='my_orders'),  
    path('edit_profile/',views.edit_profile,name='edit_profile'),  
    path('edit_admin_profile/',views.edit_admin_profile,name='edit_admin_profile'),
    path('change_password/',views.change_password,name='change_password'), 
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'), 
    path('view_account/',views.view_account,name='view_account'),
    path('delete_user/<int:id>/',views.delete_user,name='delete_user'),
    path('add_user/',views.add_user,name='add_user'),
    path('add_profile/',views.add_profile,name='add_profile'),
    path('edit_user/<int:id>/',views.edit_user,name='edit_user'),
    ]