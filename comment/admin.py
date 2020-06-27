from django.contrib import admin
from .models import Comment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','root','parent','context','content_object','user','comment_time')
    list_per_page = 10

admin.site.register(Comment,CommentAdmin)