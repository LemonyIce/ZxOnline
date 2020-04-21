
from django import forms
from captcha.fields import CaptchaField
from apps.utils.redis_tools import redis_save
from apps.users.models import UserProfile


class LoginForm(forms.Form):
    """
    账号密码
    """
    username = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
    """
    发送短信的验证码
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    """
    动态登录
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        """
        重写验证
        :return:
        """
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        redis_code = redis_save({"key": mobile, "model": "get"})
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data


class RegisterGetForm(forms.Form):
    """"
    注册页初始化
    """
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    """
    注册页提交
    """
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True)

    def clean_mobile(self):
        """
        重写手机号码验证
        :return: mobile
        """
        mobile = self.data.get("mobile")
        user = UserProfile.objects.filter(mobile=mobile)
        if user:
            raise forms.ValidationError("该手机号码已经注册")
        return mobile

    def clean_code(self):
        """
        重写验证码验证
        :return:code
        """
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        redis_code = redis_save({"key": mobile, "model": "get"})
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return code
