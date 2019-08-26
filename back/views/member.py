from django.shortcuts import render,HttpResponse,redirect
from app01.models import Article
from app01.models import Member
import json  # 使用json格式数据
from blog1 import settings
from django.contrib.auth.hashers import make_password, check_password
from app01.utils import function
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



def add(request):
    member_obj=Member.objects.all()
    if request.method == 'POST':
        member_name = request.POST.get("member_name")
        member_tel = request.POST.get("member_tel")
        member_email = request.POST.get("member_email")
        member_nickname = request.POST.get("member_nikname")
        member_pwd = make_password(request.POST.get("member_pwd"))

        res = {'status': None, 'info': None}
        if  member_name and  member_tel and  member_email and  member_pwd :
            obj = Member.objects.create(member_name=member_name, member_tel=member_tel,
                                        member_email=member_email, member_nickname=member_nickname,
                                        member_pwd=member_pwd)
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))
    # print(obj)
    return render(request,'member/add1.html',locals())


def list(request):
    member_obj = Member.objects.all()

    return render(request,'member/list.html',locals())

def list_part(request):
    member_obj = Member.objects.all()
    member_obj1 = Member.objects.all()

    where=function.getWhere_member(request)
    member_obj=Member.objects.filter(**where).all().order_by("member_id")

    currentPage=int(request.GET.get('page',1)) #获取当前在第几页
    paginator=Paginator(member_obj,5)

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
        member_obj=paginator.page(currentPage)
    except PageNotAnInteger:
        member_obj = paginator.page(1)
    except EmptyPage:
        member_obj = paginator.page(paginator.num_pages)
    return render(request,'member/list_part.html',locals())

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
def add1(request):
    return render(request,"article/add1.html")
#多对多删除
def delete1(request,id):
    # member_obj = Member.objects.all()
    #Member_id:1  author_id:2
    Member_obj = Member.objects.filter(pk=id).first()

    # Member_obj.authors.remove(2)#删除书和作者关系表中的一条记录
    # Member_obj.authors.remove(1,2)#删除书和作者关系表中的多条条记录
    # Member_obj.authors.remove(*[1, 2])#删除书和作者关系表中的多条条记录
    Member_obj.clear()
    return  HttpResponse('删除成功')

def delete(request):
    id = request.POST.get('id')
    result=Member.objects.filter(pk=id).delete()
    # print( id,result)

    import json
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))  # 把这个结果告诉给前台，ajax
    # return redirect("/back/member/list/")
def update(request,id):
    member_obj = Member.objects.filter(pk=id).first()
    name=member_obj.member_name
    tel=member_obj.member_tel
    email=member_obj.member_email
    nickname=member_obj.member_nickname
    pwd=member_obj.member_pwd
    try:

        #当点击提交按钮的时候才执行：
        if request.method=="POST":
            member_name = request.POST.get("member_name")
            member_tel = request.POST.get("member_tel")
            member_email = request.POST.get("member_email")
            member_nickname = request.POST.get("member_nikname")
            member_pwd = make_password(request.POST.get("member_pwd"))
            Member.objects.filter(pk=id).update(member_name=member_name,member_tel=member_tel,
                                       member_email=member_email,member_nickname=member_nickname,member_pwd=member_pwd)
            return HttpResponse("修改成功")
    except Exception as e:
        return HttpResponse("修改失败请按要求填写")

    return render(request,'member/update.html',locals())