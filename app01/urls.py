"""blog1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path,include
from app01.views import login,article
from app01.views.diary import diary

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login.login,name="login"),
    path('logout/', login.logout,name="logout"),
    re_path(r'^$', login.index1,name="index1"),
    re_path('main_part/', login.main_part, name='main_part'),
    path('enroll/', login.enroll,name="enroll"),
    path('diary/index/', diary.index,name="diary/index/"),
    path('article/add/', article.add,name="article/add/"),
    re_path('article/upload2/', article.upload2, name='article/upload2/'),
    re_path('article/delImg/', article.delImg, name='article/delImg/'),
    re_path(r'diary/info/(\d+)', diary.info,name="diary/info/"),
    path('diary/praise/', diary.praise,name="diary/praise/"),
    re_path(r'diary/comment/(\d+)', diary.comment,name="diary/comment/"),
    re_path(r'diary/diary_person/(\d+)', diary.diary_person,name="diary/diary_person/"),
    re_path(r'modif/(\d+)', login.modif,name="modif/"),

    # re_path('pageList/', login.pageList, name='pageList'),

    path('diary/', login.diary,name="diary"),
    path('search/', login.search,name="search"),
    path('diary_part/', login.diary_part,name="diary_part"),
    path('about/', login.about,name="about"),
    path('gbook/', login.gbook,name="gbook"),
    path('share/', login.share,name="share"),
    path('share1/', login.share1,name="share1"),
    path('share2/', login.share2,name="share2"),
    path('study/', login.study,name="study"),
    path('study1/', login.study1,name="study1"),
    path('study2/', login.study2,name="study2"),
    re_path(r'text/',login.text,name="text"),
    re_path('loginTel/', login.loginTel, name='loginTel'),
    re_path(r'text/(\d+)', login.text,name="text"),
    re_path('findPwd/', login.findPwd, name='findPwd'),
    re_path('get_valid_code_img/', login.get_valid_code_img, name='get_valid_code_img'),

#     文章增删改查 接口
    path('articleaddjson/', article.addjson,name="articleaddjson/"),
    path('articledeletejson/', article.deletejson,name="articledeletejson/"),
    path('articleupdatejson/', article.updatejson,name="articleupdatejson/"),
    path('articlesearchjson/', article.searchjson,name="articlesearchjson/"),
]
