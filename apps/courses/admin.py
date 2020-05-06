from django.contrib import admin

from apps.courses.models import Course, Lesson, Video, BannerCourse, CourseResource, CourseTag


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', ]
    list_filter = ['degree', 'teacher__name', 'learn_times']
    list_editable = ["degree", "desc"]


class BannerCourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', ]
    list_filter = ['teacher__name', 'degree', 'learn_times']
    list_editable = ["degree", "desc"]

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['name', 'add_time']


class CourseTagAdmin(admin.ModelAdmin):
    list_display = ['course', 'tag', 'add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_time']


admin.site.register(Course, CourseAdmin)
admin.site.register(BannerCourse, BannerCourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)
admin.site.register(CourseTag, CourseTagAdmin)
