from back.models import Role
from back.models import Permission
from django.shortcuts import render,HttpResponse,redirect
from app01.utils import function
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json




def add(request):
    permission_list=Permission.objects.filter(permission_pid_id__isnull=False)
    permission_listone=Permission.objects.filter(permission_pid_id__isnull=True)
    if request.method == 'POST':
        role_name = request.POST.get("role_name")
        role_access = request.POST.getlist("role_access",[])#django的数据类型 不可用python语法遍历 此处的列表类型数据
        #故作以下处理 用，间隔便于后期处理
        role_access1 = ",".join(role_access)
        # print(role_name,role_access)

        res = {'status': None, 'info': None}
        if role_name and role_access:
            res2=Role.objects.create(role_name=role_name,role_access=role_access1)
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))
    return render(request,"role/add.html",locals())

def list(request):

    role_list = Role.objects.all()

    return render(request,'role/list.html',locals())

def list_part(request):
    role_list1 = Role.objects.all()

    where=function.getWhere_role(request)
    role_list=Role.objects.filter(**where).all().order_by("role_name")

    currentPage=int(request.GET.get('page',1)) #获取当前在第几页
    paginator=Paginator(role_list,5)

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
        role_list=paginator.page(currentPage)
    except PageNotAnInteger:
        role_list = paginator.page(1)
    except EmptyPage:
        role_list = paginator.page(paginator.num_pages)
    return render(request,'role/list_part.html',locals())

def delete(request):
    res = {'status': None, 'info': None}
    id=request.POST.get('id')
    if id=="18":
        res['status'] = 2
        res['info'] = '超级管理员不可删除'
    else:

        result=Role.objects.filter(pk=id).delete()
        if result:
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败'
        return HttpResponse(json.dumps(res))  # 把这个结果告诉给前台，ajax
    return HttpResponse(json.dumps(res))

def update(request,id):
    list1=[]
    permission_list = Permission.objects.filter(permission_pid_id__isnull=False)
    permission_listone = Permission.objects.filter(permission_pid_id__isnull=True)
    permission_list=Permission.objects.all()
    role_obj = Role.objects.filter(pk=id).first()
    role_access=role_obj.role_access.split(",")
    role_name=role_obj.role_name
    #当点击提交按钮的时候才执行：
    try:
        if request.method == 'POST':
            role_name = request.POST.get("role_name")
            role_access = request.POST.getlist("role_access", [])  # django的数据类型 不可用python语法遍历 此处的列表类型数据
            # 故作以下处理 用，间隔便于后期处理
            role_access1 = ",".join(role_access)
            Role.objects.filter(pk=id).update(role_name=role_name, role_access=role_access1)

            return HttpResponse("修改成功")
    except Exception as e:
        return HttpResponse("修改失败请检查后重新修改")
    return render(request,'role/update.html',locals())