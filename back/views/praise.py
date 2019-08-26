from django.shortcuts import render,HttpResponse,redirect
from app01.models import Article
from app01.models import Member
from app01.models import Praise
import json  # 使用json格式数据
from blog1 import settings
from app01.utils import function
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

import time
def add(request):
    member_obj=Member.objects.all()
    article_obj=Article.objects.all()
    if request.method == 'POST':
        title = request.POST.get("artical")
        member = request.POST.get("member")
        praise_addtime = time.strftime("%Y-%m-%d", time.localtime())
        member_id =int(member_obj.filter(member_name=member).first().member_id)
        article_id =article_obj.filter(article_title=title).first()
        praise_obj = Praise.objects.filter(member_id_id=member_id, article_id_id=article_id).first()

        if not praise_obj:
            obj = Praise.objects.create(member_id_id=member_id, article_id=article_id, praise_addtime=praise_addtime)
        #     article_obj = Article.objects.filter(article_id=article_id).update(article_praise_num=praise_num)
        #     pra = Praise.objects.create(member_id_id=member_id, article_id_id=article_id, praise_addtime=praise_addtime)
        else:

            return HttpResponse("点赞失败 每个人只能点一次哦")
        # print(member_id)
        # 防止xss攻击,过滤script标签
    #     soup=BeautifulSoup(content,"html.parser")#通过字符串创建BeautifulSoup对象，即将字符串转为对象，然后调用对象里的相关方法
    #     print(soup.find_all())#[<img alt="" src="/media/add_article_img/hand.png"/>, <script charset="utf-8" src="/static/blog/kindeditor/kindeditor-all.js"></script>,<img src="/media/add_article_img/thumb_50_img1.jpg" alt="" />]
    #     for tag in soup.find_all():
    #
    #         print(tag.name)#img   script
    #         if tag.name=="script":
    #             tag.decompose()
    # #     # 构建摘要数据,获取标签字符串的文本前150个符号
    #     desc = soup.text[0:150] + "..."
    #     obj=Praise.objects.create(member_id_id=member_id,article_id=article_id,praise_addtime=praise_addtime)
    # print(obj)
    return render(request,'praise/add1.html',locals())


def list(request):
    member_list = Member.objects.all()
    article_list = Article.objects.all()
    praise_obj = Praise.objects.all()

    # return render(request, 'user/list.html', locals())

    return render(request,'praise/list.html',locals())

def list_part(request):

    pra_obj = Praise.objects.all()
    pra_obj1 = Praise.objects.all()

    where=function.getWhere_praise(request)
    pra_obj=Praise.objects.filter(**where).all()
    # print(com_obj)

    currentPage=int(request.GET.get('page',1)) #获取当前在第几页
    paginator=Paginator(pra_obj,5)

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
        pra_obj=paginator.page(currentPage)
    except PageNotAnInteger:
        pra_obj = paginator.page(1)
    except EmptyPage:
        pra_obj = paginator.page(paginator.num_pages)
    return render(request,'praise/list_part.html',locals())



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
def delete(request):

    id = request.POST.get('id')
    result=Praise.objects.filter(pk=id).delete()

    import json
    res = {'status': None, 'info': None}
    if result:
        res['status'] = 1
        res['info'] = '操作成功'
    else:
        res['status'] = 0
        res['info'] = '操作失败'
    return HttpResponse(json.dumps(res))
def update(request,id):
    member_obj = Member.objects.all()
    article_obj = Article.objects.all()
    praise_obj = Praise.objects.filter(pk=id).first()
    # mem_id=praise_obj.member_id_id
    # art_id=praise_obj.article_id_id
    #当点击提交按钮的时候才执行：
    if request.method == 'POST':
        title = request.POST.get("artical")
        member = request.POST.get("member")
        member_id = int(member_obj.filter(member_name=member).first().member_id)
        article_id = article_obj.filter(article_title=title).first()


        return HttpResponse("修改成功")


    return render(request,'praise/update.html',locals())