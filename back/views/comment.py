from django.shortcuts import render,HttpResponse,redirect
from app01.models import Comment
from app01.models import Member
from app01.models import Article
import json  # 使用json格式数据
from blog1 import settings
from bs4 import BeautifulSoup
from app01.utils import function
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


def add(request):
    member_obj=Member.objects.all()
    article_obj=Article.objects.all()
    if request.method == 'POST':
        title = request.POST.get("article_title")
        content = request.POST.get("content")
        member = request.POST.get("member_name")
        comment_addtime = request.POST.get("comment_addtime")
        member_id =int(member_obj.filter(member_name=member).first().member_id)
        article_id =int(Article.objects.filter(article_title=title).first().article_id)

        # print(comment_addtime)
        # 防止xss攻击,过滤script标签
        soup=BeautifulSoup(content,"html.parser")#通过字符串创建BeautifulSoup对象，即将字符串转为对象，然后调用对象里的相关方法
        # print(soup.find_all())#[<img alt="" src="/media/add_article_img/hand.png"/>, <script charset="utf-8" src="/static/blog/kindeditor/kindeditor-all.js"></script>,<img src="/media/add_article_img/thumb_50_img1.jpg" alt="" />]
        for tag in soup.find_all():

            # print(tag.name)#img   script
            if tag.name=="script":
                tag.decompose()
        # print(content,comment_addtime)
        res = {'status': None, 'info': None}
        if content and comment_addtime :
            obj = Comment.objects.create(article_id=article_id,
                                         comment_content=str(soup), member_id=member_id,
                                         comment_addtime=comment_addtime)
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))


    return render(request,'comment/add.html',locals())


def list(request):
    member_list = Member.objects.all()
    article_list = Article.objects.all()
    # com_obj = Comment.objects.all()

    # return render(request, 'user/list.html', locals())

    return render(request,'comment/list.html',locals())

def list_part(request):

    com_obj = Comment.objects.all()
    com_obj1 = Comment.objects.all()

    where=function.getWhere_comment(request)
    com_obj=Comment.objects.filter(**where).all()
    # print(com_obj)

    currentPage=int(request.GET.get('page',1)) #获取当前在第几页
    paginator=Paginator(com_obj,5)

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
        com_obj=paginator.page(currentPage)
    except PageNotAnInteger:
        com_obj = paginator.page(1)
    except EmptyPage:
        com_obj = paginator.page(paginator.num_pages)
    return render(request,'comment/list_part.html',locals())
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
    path=os.path.join(settings.MEDIA_ROOT,"add_comment_img",img_obj.name)
    with open(path,"wb") as f:
        for line in img_obj:
            f.write(line)
    response={
        "error":0,
        "url":"/media/add_comment_img/%s"%img_obj.name
    }
    return HttpResponse(json.dumps(response))
def add1(request):
    return render(request,"article/add1.html")
def delete(request):
    id = request.POST.get('id')
    result=Comment.objects.filter(pk=id).delete()

    import json
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))
    # return redirect("back/comment/list/")
def update(request,id):
    member_obj = Member.objects.all()
    article_obj = Article.objects.all()
    comment_obj = Comment.objects.filter(pk=id).first()
    content=comment_obj.comment_content
    comment_addtime=comment_obj.comment_addtime
    member_name = comment_obj.member.member_name
    article_title = comment_obj.article.article_title
    try:
        #当点击提交按钮的时候才执行：
        if request.method == 'POST':
            title = request.POST.get("article_title")
            content = request.POST.get("content")
            member = request.POST.get("member_name")
            comment_addtime = request.POST.get("comment_addtime")
            member_id = int(member_obj.filter(member_name=member).first().member_id)
            article_id = int(article_obj.filter(article_title=title).first().article_id)
            print(member_id)
            # 防止xss攻击,过滤script标签
            soup = BeautifulSoup(content, "html.parser")  # 通过字符串创建BeautifulSoup对象，即将字符串转为对象，然后调用对象里的相关方法
            print(
                soup.find_all())  # [<img alt="" src="/media/add_article_img/hand.png"/>, <script charset="utf-8" src="/static/blog/kindeditor/kindeditor-all.js"></script>,<img src="/media/add_article_img/thumb_50_img1.jpg" alt="" />]
            for tag in soup.find_all():

                print(tag.name)  # img   script
                if tag.name == "script":
                    tag.decompose()
            obj = Comment.objects.create(article_id=article_id,
                                         comment_content=str(soup), member_id=member_id, comment_addtime=comment_addtime)


            return HttpResponse("修改成功")
    except Exception as e:
        return HttpResponse("修改失败 请按要求填写")



    return render(request,'comment/update.html',locals())