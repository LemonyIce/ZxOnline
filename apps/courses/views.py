from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View

from apps.courses.models import *
from apps.operations.models import UserFavorite, UserCourse, CourseComments

from pure_pagination import Paginator, PageNotAnInteger


# Create your views here.


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """
        获取课程列表信息
        """
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")[:3]

        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        s_type = "course"
        if keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(desc__icontains=keywords)
            )

        # 课程排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, per_page=15, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            "keywords": keywords,
            "s_type": s_type
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 获取学习状态
        user_courses = UserCourse.objects.filter(user=request.user, course=course)

        # 不再学习
        p = request.GET.get('remove', '')
        if p and user_courses:
            user_courses.delete()
            request.GET._mutable = True
            request.GET.pop('remove')
            request.GET._mutable = False

        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)
        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
            "user_courses": user_courses
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        course_message = courses_message(request.user, course_id)

        return render(request, "course-video.html", {
            "course": course_message["course"],
            "course_resources": course_message["course_resources"],
            "related_courses": course_message["related_courses"]
        })


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取评论
        :param request:
        :param course_id:
        :param args:
        :param kwargs:
        :return:
        """
        course_message = courses_message(request.user, course_id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(course_message["comments"], per_page=15, request=request)
        comments = p.page(page)

        return render(request, "course-comment.html", {
            "course": course_message["course"],
            "course_resources": course_message["course_resources"],
            "related_courses": course_message["related_courses"],
            "comments": comments
        })


class VideoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        """
        视频播放
        :param request:
        :param course_id:
        :param video_id:
        :param args:
        :param kwargs:
        :return:
        """
        video = Video.objects.get(id=int(video_id))
        course_message = courses_message(request.user, course_id)
        return render(request, "course-play.html", {
            "course": course_message["course"],
            "course_resources": course_message["course_resources"],
            "related_courses": course_message["related_courses"],
            "video": video,
        })


def courses_message(user, course_id):
    """
    查询关联信息
    :param user:
    :param course_id:
    :return: "course": 课程信息,"course_resources": 资源,"related_courses": 相关课程,"comments": 评论
    """
    # 查询是否已经关联
    course = Course.objects.get(id=int(course_id))
    course.click_nums += 1
    course.save()
    user_courses = UserCourse.objects.filter(user=user, course=course)
    if not user_courses:
        user_course = UserCourse(user=user, course=course)
        user_course.save()

        course.students += 1
        course.save()

    # 学习过该课程的所有同学
    user_courses = UserCourse.objects.filter(course=course)
    user_ids = [user_course.user.id for user_course in user_courses]
    all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
    related_courses = []
    for item in all_courses:
        if item.course.id != course.id:
            related_courses.append(item.course)
    course_resources = CourseResource.objects.filter(course=course)
    comments = CourseComments.objects.filter(course=course).order_by("-add_time")
    return {
        "course": course,
        "course_resources": course_resources,
        "related_courses": related_courses,
        "comments": comments
    }


