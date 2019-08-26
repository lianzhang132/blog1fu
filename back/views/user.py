from django.shortcuts import render,HttpResponse,redirect
from back.models import Users
from back.models import Role
from collections import OrderedDict
import json  # 使用json格式数据
from blog1 import settings
from bs4 import BeautifulSoup
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app01.utils import function

def add(request):
    role_list=Role.objects.all()
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        user_birthday = request.POST.get("user_birthday")
        user_pwd = make_password(request.POST.get("user_pwd"))
        user_tel = request.POST.get("user_tel")
        user_work = request.POST.getlist("user_work",[])
        user_work1 = ",".join(user_work)

        # print(user_work,user_work1)
        user_is_recommend = request.POST.get("user_is_recommend")
        province = request.POST.get("province")
        city = request.POST.get("city")
        area = request.POST.get("area")
        user_adders=province+str(city)+str(area)

        # print(user_work)
        user_obj = Users.objects.create(user_name=user_name, user_birthday=user_birthday,
                                           user_pwd=user_pwd,user_is_recommend=user_is_recommend,
                                           user_tel=user_tel,user_work=user_work1,user_adders=user_adders)
        for v in user_work:
            role_obj=Role.objects.filter(role_id=v).first()
            role_obj.roleuser.add(user_obj)#多对多添加
        return HttpResponse("添加成功")

    return render(request,'user/add.html',locals())




import os
def upload(request):
    """
    编辑器上传文件接受视图函数
    :param request:
    :return:
    """
    # print(request.FILES)
    img_obj=request.FILES.get("upload_img")
    # print(img_obj.name)
    path=os.path.join(settings.MEDIA_ROOT,"add_article_img",img_obj.name)
    with open(path,"wb") as f:
        for line in img_obj:
            f.write(line)
    response={
        "error":0,
        "url":"/media/add_article_img/%s"%img_obj.name
    }
    return HttpResponse(json.dumps(response))
def delete(request):
    res = {'status': None, 'info': None}
    id = request.POST.get('id')
    if id =="30":
        res['status'] = 2
        res['info'] = '超级管理员不可删除'

    else:

        # id = request.POST.get('id')
        result = Users.objects.filter(user_id=id).delete()
        # result = Users.objects.filter(user_id=id).first()


        if result:
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败'
        return HttpResponse(json.dumps(res))  # 把这个结果告诉给前台，ajax
    return HttpResponse(json.dumps(res))
def update(request,id):
    user_li = Users.objects.filter(user_id=id).first()  #
    work_list1 = user_li.user_work.split(",")
    # work_list1 = user_li.user_work.split(",")
    # print(work_list1,"咋回事")
    work_list = user_li.role_set.all()
    # print(work_list)#列表
    role_list = Role.objects.all()
    user_obj = Users.objects.filter(pk=id).first()
    birthday=user_obj.user_birthday
    tel=user_obj.user_tel
    name=user_obj.user_name
    adders=user_obj.user_adders
    recommend=user_obj.user_is_recommend
    pwd=user_obj.user_pwd
    # try:

    #当点击提交按钮的时候才执行：
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        user_birthday = request.POST.get("user_birthday")
        user_pwd = make_password(request.POST.get("user_pwd"))
        user_tel = request.POST.get("user_tel")
        user_work = request.POST.getlist("user_work",[])
        user_work1 = ",".join(user_work)
        user_adders = request.POST.get("user_adders")
        # for v in work_list:#有问题 此时遍历的是原来的角色集 应该 遍历现在的角色集但是 现在的角色集 还没有添加 故得不到
        #     if Role.objects.filter(role_id=v.role_id):#筛选是否原来就有这条记录 有就什么都不做 没有添加记录
        #         pass
        #     else:
        #         user_obj = Users.objects.filter(user_id=id).update(user_name=user_name, user_birthday=user_birthday,
        #                                         user_pwd=user_pwd,
        #                                         user_tel=user_tel, user_work=user_work1)
        #         v.roleuser.add(user_obj)

        # print(set(work_list1))
        # print(work_list1)
        # print(set(user_work))
        # print(work_list1==user_work)


        # Users.objects.filter(user_id=id).update(user_name=user_name, user_birthday=user_birthday,
        #                                         user_pwd=user_pwd, user_tel=user_tel, user_work=user_work1)
        # # rol = Role.objects.filter(role_id=m).first()
        # user_li.roleuser.clear()
        # print(1, user_obj)
        # user_li.roleuser.add(*user_work)  # 多对多添加


        set1=set(user_work)-set(work_list1)#在更新后的列表中 而不在原来的列表中 此时对差集做增加处理
        set2=set(work_list1)-set(user_work)#不在更新后的列表中 而在原来的列表中 此时对差集做删除处理
        print(set2)
        if set1:
            for m in set1:

                rol=Role.objects.filter(role_id=m).first()
                # rol.roleuser.clear()
                # print(1, user_obj, rol)
                rol.roleuser.add(user_li)  # 多对多添加
                print(1,user_obj,rol)
        if set2:
            for m in set2:
                print(m)
                # Users.objects.filter(user_id=id).update(user_name=user_name, user_birthday=user_birthday,
                #                                         user_pwd=user_pwd,user_tel=user_tel, user_work=user_work1)
                rol = Role.objects.filter(role_id=m).first()
                # print(2, user_obj, rol)
                rol.roleuser.remove(user_li)  # 多对多删除 # 针对第三章表去删除。  要是用这个user_obj 对象 需要增加*
                print(2,user_obj,rol)
        Users.objects.filter(user_id=id).update(user_name=user_name, user_birthday=user_birthday,
                                                user_pwd=user_pwd, user_tel=user_tel, user_work=user_work1)
    #         return HttpResponse("修改成功")
    # except Exception as e:
    #     return HttpResponse(e)
    return render(request,'user/update.html',locals())

def threelink(request):
    return render(request,"user/add.html",locals())


def list(request):
    user_obj=Users.objects.all()

    return render(request,'user/list.html',locals())
def list_part(request):
    # for v in menu_listone:
    #     # 得到每个一级权限下的所有二级菜单
    #     # permission2 = Permission.objects.filter(permission_pid_id=v.permission_id,permission_id__in=per_list).all()
    #     menu2 = Menu.objects.filter(menu_pid_id=v.menu_id, menu_id__in=per_list).all()
    #     permission_listnow[v.menu_id] = {
    #         'id': v.menu_id,
    #         'name': v.menu_name,
    #         'path': v.menu_path,
    #         # 'children': permission2,
    #         'children_menu': menu2
    #     }

    role_list=Role.objects.all()
    # user_obj=Users.objects.all()
    work_name=[]
    user_obj_list=[]
    user_obj_dic={}
    user_ids=[]
    where=function.getWhere_user(request)
    user_obj1=Users.objects.filter(**where).all().order_by("user_id")#筛选符合要求所有的用户对象集
    #遍历所有的 用户对象
    # for v in user_obj:
    #     user_li = Users.objects.filter(user_id=v.user_id).first()#
    #     work_list1 = user_li.user_work.split(",")
    #     print(work_list1)
    #     work_list = Role.objects.filter(role_id__in=work_list1).all()

        # user_obj_dic[v.user_work] = work_list
        # user_obj_dic[v.user_id] = v.user_id
        # user_obj_dic[v.user_birthday] = v.user_birthday
        # user_obj_dic[v.user_tel] = v.user_tel
        # user_obj_dic[v.user_name] = v.user_name
        # user_obj_dic[v.user_adders] = v.user_adders
        # user_obj_dic[v.user_pwd] = v.user_pwd
        # user_obj_dic[v.user_is_recommend] = v.user_is_recommend
        # user_obj_list.append(user_obj_dic)

        # print(user_obj_dic)
        # if v.user_id not in user_ids:
        #     user_obj_list.append(user_obj_dic)
    # print(user_obj_list)

    # user_obj1 = user_obj_list
    currentPage=int(request.GET.get('page',1)) #获取当前在第几页
    paginator=Paginator(user_obj1,5)


    if paginator.num_pages>11:
        if currentPage-5<1:
            pageRange=range(1,11)
        elif currentPage+5>paginator.num_pages:
            pageRange = range(currentPage-5, paginator.num_pages+1)
        else:
            pageRange = range(currentPage - 5,currentPage+5)
    else:
        pageRange = range(1,paginator.num_pages+1)

    try:
        # user_obj1=paginator.page(1)
        user_obj1=paginator.page(currentPage)
    except PageNotAnInteger:
        user_obj1 = paginator.page(1)
    except EmptyPage:
        user_obj1 = paginator.page(paginator.num_pages)
    return render(request,'user/list_part.html',locals())