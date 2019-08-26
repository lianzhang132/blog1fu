from django.shortcuts import render,HttpResponse,redirect
from app01.models import Article
from app01.models import Member
import time
import json  # 使用json格式数据
from blog1 import settings
from bs4 import BeautifulSoup
from app01.views.prelogin import *


@if_sess1
def add(request):
    member_name = request.session.get("member_name")
    article_img = 0
    member_obj=Member.objects.all()
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        article_is_recommend = request.POST.get("article_is_recommend")
        # article_img = request.POST.get("image_name[0]")
        member = request.session.get("member_name")
        article_img = request.session.get("article_img")
        article_addtime = time.strftime( "%Y-%m-%d", time.localtime())
        member_id =int(member_obj.filter(member_name=member).first().member_id)
        # print(content,"nen")
        # 防止xss攻击,过滤script标签
        soup=BeautifulSoup(content,"html.parser")#通过字符串创建BeautifulSoup对象，即将字符串转为对象，然后调用对象里的相关方法
        # print(soup.find_all())#[<img alt="" src="/media/add_article_img/hand.png"/>, <script charset="utf-8" src="/static/blog/kindeditor/kindeditor-all.js"></script>,<img src="/media/add_article_img/thumb_50_img1.jpg" alt="" />]
        for tag in soup.find_all():

            # print(tag.name)#img   script
            if tag.name=="script":
                tag.decompose()
    #     # 构建摘要数据,获取标签字符串的文本前150个符号
        desc = soup.text[0:150] + "..."
        # print(title,content,article_img,member)
        res = {'status': None, 'info': None}
        if title and content and article_img and member:
            obj = Article.objects.create(article_title=title, article_description=desc,
                                         article_is_recommend=article_is_recommend,
                                         article_content=str(soup), member_id=member_id,
                                         article_addtime=article_addtime, article_img=article_img)
            res['status'] = 1
            res['info'] = '操作成功'
        else:
            res['status'] = 0
            res['info'] = '操作失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))

    # print(obj)
    return render(request,'login/add.html',locals())
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

def addjson(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        content = request.POST.get("content")
        article_is_recommend = request.POST.get("article_is_recommend")
        # article_img = request.POST.get("image_name[0]")
        member_id = request.session.get("member_id")
        article_img = request.session.get("article_img")
        article_addtime = time.strftime( "%Y-%m-%d", time.localtime())
        desc = content[0:150] + "..."
        res = {'status': None, 'info': None}
        obj = Article.objects.create(article_title=title, article_description=desc,
                                     article_is_recommend=article_is_recommend,
                                     article_content=content, member_id=member_id,
                                     article_addtime=article_addtime, article_img=article_img)
        if obj:
            res['status'] = 1
            res['info'] = '添加成功'
        else:
            res['status'] = 0
            res['info'] = '添加失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))
def deletejson(request):
    res = {'status': None, 'info': None}
    article_id = request.POST.get("article_id")
    obj=Article.objects.filter(article_id=article_id).delete()
    if obj:
        res['status'] = 1
        res['info'] = '删除成功'
    else:
        res['status'] = 0
        res['info'] = '删除失败 '
    return HttpResponse(json.dumps(res))
def updatejson(request):
    if request.method == 'POST':
        article_id = request.POST.get("article_id")
        title = request.POST.get("title")
        content = request.POST.get("content")
        article_is_recommend = request.POST.get("article_is_recommend")
        # article_img = request.POST.get("image_name[0]")
        member_id = request.session.get("member_id")
        article_img = request.session.get("article_img")
        article_addtime = time.strftime("%Y-%m-%d", time.localtime())
        res = {'status': None, 'info': None}
        obj = Article.objects.filter(article_id=article_id).update(article_title=title, article_description=desc,
                                     article_is_recommend=article_is_recommend,
                                     article_content=content, member_id=member_id,
                                     article_addtime=article_addtime, article_img=article_img)
        if obj:
            res['status'] = 1
            res['info'] = '修改成功'
        else:
            res['status'] = 0
            res['info'] = '修改失败 每个输入都不能为空'
        return HttpResponse(json.dumps(res))

from collections import OrderedDict

def searchjson(request):
    art_list=Article.objects.all()
    list1 = OrderedDict()
    for v in art_list:
        list1[v.article_id] = {'article_id': v.article_id, 'article_title': v.article_title,
                                'article_description': v.article_description,"article_is_recommend":v.article_is_recommend,
                              "article_content":v.article_content,"member_id":v.member_id,"article_addtime":v.article_addtime.strftime("%Y-%m-%d"),
                              "article_img":v.article_img }
    return HttpResponse(json.dumps(list1))