"""zxSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from django.views.generic import TemplateView

from extra_apps import xadmin

from apps.users.views import LoginView, LogoutView

from zxSchool.settings import MEDIA_ROOT

urlpatterns = [
    # 主页
    path('', TemplateView.as_view(template_name="index.html")),
    path('index/', TemplateView.as_view(template_name="index.html"),  name="index"),

    # 登录页
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    # 后台管理
    path('admin/', admin.site.urls),
    # 备用后台管理
    path('xadmin/', xadmin.site.urls),

    # 访问上传文件
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
