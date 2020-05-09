from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from apps.courses.models import Course
from apps.operations.models import UserFavorite, UserCourse, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.users.models import UserProfile
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm, \
    UserInfoForm, UploadImageForm, ChangePwdForm, UpdateMobileForm
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from apps.utils.redis_tools import redis_save
from zxSchool.settings import YP, REDIS
import redis


# Create your views here.
def message_nums(request):
    """
    登录状态
    """
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class LoginView(View):
    """
    账号登录
    """
    def get(self, request, *args, **kwargs):
        # 是否有登录信息，注意django全局公用session
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        # banners = Banner.objects.all()[:3]
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "templates/login.html", {
            "login_form": login_form,
            "next": next,
            # "banners":banners
        })

    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        # banners = Banner.objects.all()[:3]
        if login_form.is_valid():
            # 用于通过用户和密码查询用户是否存在
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # 查询到用户
                login(request, user)
                # 登录成功之后应该怎么返回页面
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                # 未查询到用户
                # return render(request, "login.html", {"msg": "用户名或密码错误",
                #                                       "login_form": login_form, "banners": banners})
                return render(request, "templates/login.html", {"msg": "用户名或密码错误",
                                                                "login_form": login_form})
        else:
            # return render(request, "login.html", {"login_form": login_form, "banners": banners})
            return render(request, "templates/login.html", {"login_form": login_form, })


class LogoutView(View):
    """
    注销
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class SendSmsView(View):
    """
    发送验证码
    """
    def post(self, request, *args, **kwargs):
        import time
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            code = generate_random(4, 0)
            # re_json = send_single_sms(YP["apikey"], code, mobile=mobile)
            re_json = {
                "code": 0,
            }  # 测试用标记注释，这里注释掉的是短信发送接口
            if re_json["code"] == 0:
                re_dict["status"] = "success"
                redis_save({
                    "key": mobile,
                    "value": code,
                    "model": "set",
                    "overtime": 300
                })
            else:
                re_dict["msg"] = re_json["msg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)


class DynamicLoginView(View):
    """
    动态登录
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        # banners = Banner.objects.all()[:3]
        return render(request, "templates/login.html", {
            "login_form": login_form,
            "next": next,
            # "banners": banners
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        # banners = Banner.objects.all()[:3]
        if login_form.is_valid():
            # 查没有注册账号，没有就注册一个
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                user = UserProfile(username=mobile)
                # 密码为10位随机字符数字
                password = generate_random(10, 2)
                user.set_password(password)
                # 注意密码不能保存明文需要经过加密
                user.mobile = mobile
                user.save()
                UserMessage(user=request.user, message="您使用了动态登录，您的初始密码为" + password+"请尽快修改").save()
            login(request, user)
            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "templates/login.html", {"login_form": login_form,
                                                            "d_form": d_form,
                                                            # "banners":banners,
                                                            "dynamic_login": dynamic_login
                                                            })


class RegisterView(View):
    """
    注册
    """
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "templates/register.html", {
            "register_get_form": register_get_form
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()

            UserMessage(user=request.user, message="感谢您注册本站").save()

            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "templates/register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form
            })


class UserInfoView(LoginRequiredMixin, View):
    """
    个人中心
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "info"
        captcha_form = RegisterGetForm()
        return render(request, "usercenter-info.html", {
            "captcha_form": captcha_form,
            "current_page": current_page
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            UserMessage(user=request.user, message="您修改了个人信息，请注意账号安全").save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(user_info_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    """
    修改头像
    """
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })


class ChangePwdView(LoginRequiredMixin, View):
    """
    修改密码
    """
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():

            pwd1 = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd1)
            user.save()
            UserMessage(user=request.user, message="您在最近修改了一次密码，请注意账号安全").save()

            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class ChangeMobileView(LoginRequiredMixin, View):
    """
    修改电话
    """
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data["mobile"]
            if request.user.mobile == mobile:
                return JsonResponse({
                    "mobile": "此号码为当前您绑定的号码"
                })
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "mobile": "该手机号码已经被占用"
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile
            user.save()
            UserMessage(user=request.user, message="您修改了绑定电话，新的的电话为"+mobile).save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(mobile_form.errors)


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "mycourse"
        my_courses = UserCourse.objects.filter(user=request.user)
        all_course = []
        for course in my_courses:
            a_course = Course.objects.get(id=course.course_id)
            all_course.append(a_course)

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, per_page=16, request=request)
        courses = p.page(page)
        return render(request, "usercenter-mycourse.html", {
            "all_courses": courses,
            "current_page": current_page
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我的收藏主页+机构
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavorg"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)

            # 对收藏数据进行分页
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(org_list, per_page=10, request=request)
            all_org = p.page(page)

        return render(request, "usercenter-fav-org.html", {
            "org_list": all_org,
            "current_page": current_page
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我的收藏教师
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_teacher"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            org = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(org)

            # 对课程机构数据进行分页
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(teacher_list, per_page=10, request=request)
            teacher = p.page(page)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher,
            "current_page": current_page
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    课程收藏
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass
            # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(course_list, per_page=16, request=request)
        all_course = p.page(page)
        return render(request, "usercenter-fav-course.html", {
            "course_list": all_course,
            "current_page": current_page
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    用户消息
    """
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user).order_by("-add_time")
        current_page = "message"
        UserMessage.objects.filter(user=request.user).update(has_read=True)
        # 对讲师数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=20, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page
        })


def message_nums(request):
    """
    用户消息提示
    这个一个全局方法
    """
    if request.user.is_authenticated:
        unread_nums = request.user.usermessage_set.filter(has_read=False).count()
        return {'unread_nums': unread_nums}
    else:
        return {}
