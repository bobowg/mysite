from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)
    list_display = ('username','nickname','email','is_staff','is_active','is_superuser')

    def nickname(self,obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user','nickname')

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
# admin.site.register(Profile,ProfileAdmin)