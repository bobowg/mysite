from django.contrib import admin
from .models import ReadNum,ReadDetail
# Register your models here.

class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num','content_object')
    list_per_page = 10
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('date','read_num','content_object')
    list_per_page = 10
admin.site.register(ReadNum,ReadNumAdmin)
admin.site.register(ReadDetail,ReadDetailAdmin)