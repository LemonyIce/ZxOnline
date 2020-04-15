from django.contrib import admin

from apps.operations.models import UserAsk, CourseComments, UserCourse, UserFavorite, UserMessage
from apps.operations.models import Banner


class UserAskAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['add_time']


class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'url', "index"]
    search_fields = ['title', 'image', 'url', "index"]
    list_filter = ['title', "index"]


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']

    def save_models(self):
        obj = self.new_obj
        if not obj.id:
            obj.save()
            course = obj.course
            course.students += 1
            course.save()


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'has_read', 'add_time']


class CourseCommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['add_time']


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_type', 'add_time']


admin.site.register(UserAsk, UserAskAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(CourseComments, CourseCommentsAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)

