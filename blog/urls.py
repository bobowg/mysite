from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('blog/',views.blog_list,name='blog_list'),
    path('blog/<int:blog_id>',views.blog_detail,name='blog_detail'),
    path('type/<int:type_id>',views.blog_with_type,name='blog_with_type'),
    path('date/<int:year>/<int:month>',views.blogs_with_days,name='blogs_with_days'),
]