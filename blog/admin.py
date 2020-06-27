from django.contrib import admin
from .models import BlogType,Blog
# Register your models here.

class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')
    list_per_page = 10
    list_editable = ('type_name',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','blog_type','author','read_num','created_time','last_update_time')
    search_fields = ['title']
    list_per_page = 10

admin.site.register(BlogType,BlogTypeAdmin)
admin.site.register(Blog,BlogAdmin)
