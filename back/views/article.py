from django.shortcuts import render,HttpResponse,redirect
from app01.models import Article
from app01.models import Member
import json  # 使用json格式数据
from blog1 import settings
from bs4 import BeautifulSoup
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from app01.utils import function
from app01.views.prelogin import *


# @if_sess2
def add(request):
    member_obj=Member.objects.all()
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        member = request.POST.get("member")
        article_addtime = request.POST.get("article_addtime")
        article_img = request.session.get("article_img")
        member_id =int(member_obj.filter(member_name=member).first().member_id)
        # print(member_id)
        # print(article_img)
        # 防止xss攻击,过滤script标签
        soup=BeautifulSoup(content,"html.parser")#通过字符串创建BeautifulSoup对象，即将字符串转为对象，然后调用对象里的相关方法
        # print(soup.find_all())#[<img alt="" src="/media/add_article_img/hand.png"/>, <script charset="utf-8" src="/static/blog/kindeditor/kindeditor-all.js"></script>,<img src="/media/add_article_img/thumb_50_img1.jpg" alt="" />]
        for tag in soup.find_all():

            # print(tag.name)#img   script
            if tag.name=="script":
                tag.decompose()
    #     # 构建摘要数据,获取标签字符串的文本前150个符号
        desc = soup.text[0:150] + "..."
        # print(str(soup))
        import json
        res = {'status': None, 'info': None}
        # print(bool(article_img),bool(article_addtime),bool(content),bool(title),"za会是")
        # print(content)
        # print(bool(article_img),bool(article_addtime),content,bool(title),"za会是")

        if article_img and article_addtime and content and title:
            # print(11)
            obj = Article.objects.create(article_title=title, article_description=desc, article_img=article_img,
                                         article_content=content, member_id=member_id, article_addtime=article_addtime)
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))


    return render(request,'article/add1.html',locals())


def list(request):

    member_list = Member.objects.all()

    return render(request,'article/list.html',locals())

def list_part(request):
    article_list = Article.objects.all().order_by("article_addtime")

    where=function.getWhere(request)
    articles_list=Article.objects.filter(**where).all().order_by("article_praise_num")

    currentPage=int(request.GET.get('page',1)) #获取当前在第几页
    paginator=Paginator(articles_list,7)

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
        articles_list=paginator.page(currentPage)
    except PageNotAnInteger:
        articles_list = paginator.page(1)
    except EmptyPage:
        articles_list = paginator.page(paginator.num_pages)
    return render(request,'article/list_part.html',locals())



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
def list_delete(request,id):
    Article.objects.filter(pk=id).delete()
    return redirect("back/article/list/")
def delete(request):
    id=request.POST.get('id')
    result=Article.objects.filter(article_id=id).delete()
    import json
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))  # 把这个结果告诉给前台，ajax
def multidelete(request):
    ids = request.POST.getlist("checkbox1",[])
    # print(ids)

    res = {'status': None, 'info': None}
    if ids:
        for m in ids:
            Article.objects.filter(article_id=m).delete()
        res['status'] = 1
        res['info'] = '批量删除成功'
    else:
        res['status'] = 0
        res['info'] = '批量删除失败'
    return HttpResponse(json.dumps(res))

def update(request,id):
    member_obj = Member.objects.all()
    article_obj = Article.objects.filter(pk=id).first()
    article_content=article_obj.article_content
    article_addtime=article_obj.article_addtime
    member_name = article_obj.member.member_name
    article_title = article_obj.article_title
    article_img = article_obj.article_img
    article_clicknum = article_obj.article_clicknum
    article_is_recommend = article_obj.article_is_recommend
    # print(article_clicknum,article_is_recommend)
    #当点击提交按钮的时候才执行：
    try:

        if request.method == 'POST':
            title = request.POST.get("article_title")
            content = request.POST.get("content")
            article_img = request.POST.get("article_img")
            article_is_recommend = request.POST.get("article_is_recommend")
            member = request.POST.get("member_name")
            article_addtime = request.POST.get("article_addtime")
            member_id = int(member_obj.filter(member_name=member).first().member_id)
            # print(member_id,member)
            # 防止xss攻击,过滤script标签
            soup = BeautifulSoup(content, "html.parser")  # 通过字符串创建BeautifulSoup对象，即将字符串转为对象，然后调用对象里的相关方法
            # print(
            #     soup.find_all())  # [<img alt="" src="/media/add_article_img/hand.png"/>, <script charset="utf-8" src="/static/blog/kindeditor/kindeditor-all.js"></script>,<img src="/media/add_article_img/thumb_50_img1.jpg" alt="" />]
            for tag in soup.find_all():
                if tag.name == "script":
                    tag.decompose()
            desc = soup.text[0:150] + "..."
            obj = Article.objects.filter(pk=id).update(article_title=title, article_description=desc,article_img=article_img,article_is_recommend=article_is_recommend,
                                         article_content=str(soup), member_id=member_id, article_addtime=article_addtime)

            return HttpResponse("修改成功")
    except Exception as e:
        return HttpResponse("修改失败请检查后重新修改")
    return render(request,'article/update.html',locals())
import os
from app01.utils import function
import os.path
def upload2(request):
    img_obj=request.FILES.get("file")#通过前台提交过来的图片资源   img_obj.name  avatar.jpg
    range_num=function.range_num(15)#生成一个15位随机数

    # print(img_obj.name)
    img_type=os.path.splitext(img_obj.name)[1]#.jpg  获取文件名后缀
    new_img_path=os.path.join(settings.MEDIA_ROOT,"add_article_img",range_num+img_type)#E:\ftp\code\www\pro\media\add_article_img\676161546271228.jpg        #/media/add_article_img/123456.jpg


    img_type2 = img_type.replace(".", "")  #png
    request.session['article_img'] = "/media/add_article_img/"+range_num+img_type


    # print(new_img_path)
    with open(new_img_path,"wb") as f:
        for line in img_obj:
            f.write(line)
    response={
        "status":1,
        "message":"上传成功",
        'file':"/media/add_article_img/"+range_num+img_type,
        'file_type':img_type2
    }

    return HttpResponse(json.dumps(response))

def delImg(request):
    img_path=request.POST.get('path')#/media/add_article_img/722264423391172.jpg
    img_name=os.path.split(img_path)[1]#获取图片名称 722264423391172.jpg
    img_new_path=os.path.join(settings.MEDIA_ROOT,"add_article_img",img_name)#E:\ftp\code\www\pro\media\add_article_img\722264423391172.jpg
    if not os.remove(img_new_path):
        response={
            "status":1,
            "message":"删除成功"
        }
        return HttpResponse(json.dumps(response))