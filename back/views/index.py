from django.shortcuts import render,HttpResponse,redirect
from app01.views.prelogin import *
from back.models import Users
from back.models import Permission
from back.models import Menu
from back.models import Role
from collections import OrderedDict

@if_sess2
def index(request):

    return render(request,'index/index.html',locals())

def top(request):
    user_name = request.session.get("user_name")
    return render(request,'index/top.html',locals())

def left(request):
    user_id = request.session.get("user_id")#得到管理员id
    user_obj = Users.objects.filter(user_id=user_id).first()

    permission_listnow=OrderedDict()
    role_list=user_obj.role_set.all()
    per_list=[]

    # # print(type(role_list))
    for role in role_list:
        per = Role.objects.filter(role_name=role).first()
        mm = per.role_access.split(",")#以逗号分割为一种python的格式字符串与储存时结合使用
        for n in mm:
            if n not in permission_listnow:
                per_list.append(n)
    # 得到所有当前用户角色下拥有的所有一级权限
    # permission_listone=Permission.objects.filter(permission_pid_id__isnull=True,
    #                                              permission_id__in=per_list).all()
    # 得到所有当前用户角色下拥有的所有一级菜单
    menu_listone=Menu.objects.filter(menu_pid_id__isnull=True,
                                                 menu_name__in=per_list).all()

                # permission_listnow.append(per_obj)
        # permission_all = OrderedDict()
        # permission = Permission.objects.filter(pid__isnull=True).all()
    for v in menu_listone:
        #得到每个一级权限下的所有二级菜单
        # permission2 = Permission.objects.filter(permission_pid_id=v.permission_id,permission_id__in=per_list).all()
        menu2 = Menu.objects.filter(menu_pid_id=v.menu_id,menu_name__in=per_list).all()
        permission_listnow[v.menu_id] = {
            'id': v.menu_id,
            'name': v.menu_name,
            'path': v.menu_path,
            # 'children': permission2,
            'children_menu': menu2
            }
    # for v in permission_listone:
    #     #得到每个一级权限下的所有二级权限
    #     permission2 = Permission.objects.filter(permission_pid_id=v.permission_id,permission_id__in=per_list).all()
    #     menu2 = Menu.objects.filter(menu_pid_id=v.permission_id,menu_id__in=per_list).all()
    #     permission_listnow[v.permission_id] = {
    #         'id': v.permission_id,
    #         'name': v.permission_name,
    #         'path': v.permission_path,
    #         'children': permission2,
    #         'children_menu': menu2
    #         }
    # print(permission_listone)
    # print(permission_listnow)
        # mm=role.role_access
        # print(per,str(mm)[0])
        # for m in mm:
        #     print(m)

    # 多对多 反向多对多查询例子
    # 作者和书   唐海龙写了哪些书
    # 反向查询--根据 表名_set
    # def book_lists6(request):
    #     author_obj = Author.objects.filter(name='唐海龙').first()
    #     print(author_obj.book_set.all())
    #     return HttpResponse('ok')

    return render(request,'index/left.html',locals())

def footer(request):
    return render(request,'index/footer.html')

def main(request):
    return render(request,'index/main.html')

