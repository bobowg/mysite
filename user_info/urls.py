from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('user_info/', views.userInfo, name='user_info'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('login_form/', views.login_for_medal, name='login_form'),
    path('change_nickname/',views.Change_nickname,name='change_nickname'),
    path('bindemail/',views.BindEmail,name='bindemail'),
    path('send_code/',views.send_verification_code,name='send_code'),
    path('change_password/',views.Change_Password,name='change_password'),
    path('forgotpassword/',views.FotgotPassword,name='forgotpassword'),
]