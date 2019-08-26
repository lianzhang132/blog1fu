from back.models import Menu
from back.models import Permission
from django.shortcuts import render,HttpResponse,redirect
from app01.utils import function
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json




def add(request):
    permission_listone=Permission.objects.filter(permission_pid_id__isnull=True)#筛选出一级权限
    # permission_list=Permission.objects.filter()#筛选一级权限
    if request.method == 'POST':
        permission_name = request.POST.get("permission_name")
        permission_path = request.POST.get("permission_path")
        permission_pid_id = request.POST.get("permission_pid_id")

        res = {'status': None, 'info': None}
        if permission_name and permission_path:
            res2 = Permission.objects.create(permission_name=permission_name, permission_path=permission_path,
                                             permission_pid_id=permission_pid_id)
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))
    return render(request,"permission/add.html",locals())

def list(request):

    permission_list = Permission.objects.all()

    return render(request,'permission/list.html',locals())

def list_part(request):
    permission_list1 = Permission.objects.all()

    where=function.getWhere_permission(request)
    permission_list=Permission.objects.filter(**where).all().order_by("permission_id")

    currentPage=int(request.GET.get('page',1)) #获取当前在第几页
    paginator=Paginator(permission_list,10)

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
        permission_list=paginator.page(currentPage)
    except PageNotAnInteger:
        permission_list = paginator.page(1)
    except EmptyPage:
        permission_list = paginator.page(paginator.num_pages)
    return render(request,'permission/list_part.html',locals())

def delete(request):
    id=request.POST.get('id')
    result=Permission.objects.filter(pk=id).delete()
    import json
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))  # 把这个结果告诉给前台，ajax


def update(request,id):
    permission_list=Permission.objects.filter(permission_pid_id__isnull=True)#筛选出一级菜单
    permission_obj = Permission.objects.filter(pk=id).first()
    permission_name=permission_obj.permission_name
    permission_path=permission_obj.permission_path
    permission_pid_id=permission_obj.permission_pid_id
    #当点击提交按钮的时候才执行：
    try:
        if request.method == 'POST':
            permission_name = request.POST.get("permission_name")
            permission_path = request.POST.get("permission_path")
            permission_pid_id = request.POST.get("permission_pid_id")

            obj = Permission.objects.filter(pk=id).update(permission_name=permission_name, permission_path=permission_path,permission_pid_id=permission_pid_id)

            return HttpResponse("修改成功")
    except Exception as e:
        return HttpResponse("修改失败请检查后重新修改")
    return render(request,'permission/update.html',locals())