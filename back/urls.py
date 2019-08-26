from django.contrib import admin
from django.urls import path,re_path
from back.views import index
from back.views import user
from back.views import article
from back.views import comment
from back.views import member
from back.views import praise
from back.views import login
from back.views import menu
from back.views import permission
from back.views import role
from back.views import statistics
urlpatterns = [
    re_path('index/index/', index.index, name='index/index/'),
    re_path('index/left/', index.left, name='index/left/'),
    re_path('index/main/', index.main, name='index/main/'),
    re_path('index/footer/', index.footer, name='index/footer/'),
    re_path('index/top/', index.top, name='index/top/'),
    re_path('article/list/', article.list, name='article/list/'),
    re_path('user/list/', user.list, name='user/list/'),
    re_path('article/add/', article.add, name='article/add/'),
    re_path('article/add1/', article.add1, name='article/add1/'),
    re_path('article/upload2/', article.upload2, name='article/upload2/'),
    re_path('article/delImg/', article.delImg, name='article/delImg/'),
    re_path('user/add/', user.add, name='user/add/'),
    re_path('article/upload/', article.upload, name='article/upload/'),
    re_path('comment/upload/', comment.upload, name='comment/upload/'),
    re_path('comment/list/', comment.list, name='comment/list/'),
    re_path('comment/add/', comment.add, name='comment/add/'),
    re_path('praise/list/', praise.list, name='praise/list/'),
    re_path('praise/add/', praise.add, name='praise/add/'),
    re_path('member/list/', member.list, name='member/list/'),
    re_path('member/add/', member.add, name='member/add/'),
    re_path('statistics/click/', statistics.click, name='statistics/click/'),

    re_path(r"member/delete/", member.delete, name='member/delete/'),
    re_path(r"member/update/(\d+)", member.update, name='member/update/'),
    re_path(r"praise/delete/", praise.delete, name='praise/delete/'),
    re_path(r"praise/update/(\d+)", praise.update, name='praise/update/'),
    re_path('praise/list_part/', praise.list_part, name='praise/list_part/'),
    re_path(r"comment/delete/", comment.delete, name='comment/delete/'),
    re_path(r"comment/update/(\d+)", comment.update, name='comment/update/'),
    re_path("article/delete/", article.delete, name='article/delete/'),
    re_path("article/multidelete/", article.multidelete, name='article/multidelete/'),
    re_path(r"article/update/(\d+)", article.update, name='article/update/'),
    re_path('article/list_part/', article.list_part, name='article/list_part/'),
    re_path('user/list_part/', user.list_part, name='user/list_part/'),
    re_path('comment/list_part/', comment.list_part, name='comment/list_part/'),
    re_path('praise/list_part/', praise.list_part, name='praise/list_part/'),
    re_path('member/list_part/', member.list_part, name='member/list_part/'),
    re_path(r"user/delete/", user.delete, name='user/delete/'),
    re_path(r"user/update/(\d+)", user.update, name='user/update/'),
    path("login/login/", login.login, name='login/login/'),
    path('logout/', login.logout,name="logout"),
    path("user/threelink/", user.threelink, name='user/threelink/'),


    re_path(r"menu/add/", menu.add, name='menu/add/'),
    re_path(r"menu/list/", menu.list, name='menu/list/'),
    re_path('menu/list_part/', menu.list_part, name='menu/list_part/'),
    re_path(r"menu/delete/", menu.delete, name='menu/delete/'),
    re_path(r"menu/update/(\d+)", menu.update, name='menu/update/'),

    re_path(r"permission/add/", permission.add, name='permission/add/'),
    re_path(r"permission/list/", permission.list, name='permission/list/'),
    re_path('permission/list_part/', permission.list_part, name='permission/list_part/'),
    re_path(r"permission/delete/",permission.delete, name='permission/delete/'),
    re_path(r"permission/update/(\d+)", permission.update, name='permission/update/'),

    re_path(r"role/add/", role.add, name='role/add/'),
    re_path(r"role/list/", role.list, name='role/list/'),
    re_path('role/list_part/', role.list_part, name='role/list_part/'),
    re_path(r"role/delete/", role.delete, name='role/delete/'),
    re_path(r"role/update/(\d+)", role.update, name='role/update/'),

]
