from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from apps.users.models import UserProfile
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm
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
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "templates/register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form
            })
