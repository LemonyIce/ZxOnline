from django.conf.urls import url
from django.urls import path

from apps.organizations.views import *

urlpatterns = [
    # 机构首页
    url(r'^list/$', OrgView.as_view(), name="list"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),

    # 机构详情
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    # 教师
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
    # 课程
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),
    # 详情
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name="desc"),

    # 讲师列表页
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
