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


admin.site.register(Course, CourseAdmin)
admin.site.register(BannerCourse, BannerCourseAdmin)

