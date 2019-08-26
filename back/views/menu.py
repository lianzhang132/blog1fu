from back.models import Menu
from back.models import Permission
from django.shortcuts import render,HttpResponse,redirect
from app01.utils import function
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json




def add(request):
    menu_list=Menu.objects.filter(menu_pid_id__isnull=True)#筛选出一级菜单
    permission_list=Permission.objects.filter(permission_pid_id__isnull=True)#筛选一级权限
    if request.method == 'POST':
        menu_name = request.POST.get("menu_name")
        menu_path = request.POST.get("menu_path")
        menu_pid_id = request.POST.get("menu_pid_id")
        permission_pid_id = request.POST.get("permission_pid_id")

        res = {'status': None, 'info': None}
        if menu_name and menu_path :
            res1 = Menu.objects.create(menu_name=menu_name, menu_path=menu_path, menu_pid_id=menu_pid_id)
            res2 = Permission.objects.create(permission_name=menu_name, permission_path=menu_path, menu_id=menu_pid_id,
                                             permission_pid_id=permission_pid_id)
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))

    return render(request,"menu/add.html",locals())

def list(request):

    menu_list = Menu.objects.all()

    return render(request,'menu/list.html',locals())

def list_part(request):
    menu_list1 = Menu.objects.all()

    where=function.getWhere_menu(request)
    menu_list=Menu.objects.filter(**where).all().order_by("menu_name")

    currentPage=int(request.GET.get('page',1)) #获取当前在第几页
    paginator=Paginator(menu_list,10)

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
        menu_list=paginator.page(currentPage)
    except PageNotAnInteger:
        menu_list = paginator.page(1)
    except EmptyPage:
        menu_list = paginator.page(paginator.num_pages)
    return render(request,'menu/list_part.html',locals())

def delete(request):
    id=request.POST.get('id')
    result=Menu.objects.filter(pk=id).delete()
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
    menu_list=Menu.objects.filter(menu_pid_id__isnull=True)#筛选出一级菜单
    menu_obj = Menu.objects.filter(pk=id).first()
    menu_name=menu_obj.menu_name
    menu_path=menu_obj.menu_path
    menu_pid_id=menu_obj.menu_pid_id
    #当点击提交按钮的时候才执行：
    try:
        if request.method == 'POST':
            menu_name = request.POST.get("menu_name")
            menu_path = request.POST.get("menu_path")
            menu_pid_id = request.POST.get("menu_pid_id")

            obj = Menu.objects.filter(pk=id).update(menu_name=menu_name, menu_path=menu_path,menu_pid_id=menu_pid_id)

            return HttpResponse("修改成功")
    except Exception as e:
        return HttpResponse("修改失败请检查后重新修改")
    return render(request,'menu/update.html',locals())