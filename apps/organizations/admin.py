from django.contrib import admin
from apps.organizations.models import Teacher, CourseOrg, City


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CourseOrgAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', ]
    list_filter = ['click_nums', 'fav_nums']
    style_fields = {
        "desc": "ueditor"
    }


class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "desc"]
    search_fields = ["name", "desc"]
    list_filter = ["add_time"]


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(City, CityAdmin)
