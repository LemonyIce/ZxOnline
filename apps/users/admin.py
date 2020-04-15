from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import UserProfile


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'nick_name', 'mobile', 'email', 'is_staff', 'is_active']
    search_fields = ['username', 'nick_name', 'mobile', 'email', ]
    list_filter = ['is_staff', 'is_active', 'add_time']
    pass


admin.site.site_title = "知行教育后台"
admin.site.site_header = '知行教育'
admin.site.site_footer = "lyshop"
admin.site.register(UserProfile, UserProfileAdmin)
