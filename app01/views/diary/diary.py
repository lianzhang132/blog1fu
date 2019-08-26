from django.shortcuts import render,HttpResponse,redirect
from app01.models import Article
from app01.models import Praise
from app01.models import Comment
from app01.models import Click
import time
from app01.views.prelogin import *

@if_sess1
def index(request):
    now_id = request.session.get('member_id')
    member_name = request.session.get("member_name")
    art_obj=Article.objects.all()
    art_obj_praise=Article.objects.all().order_by('article_praise_num')[:4]
    art_obj_1=Article.objects.filter(article_is_recommend=1).first()

    return render(request, "login/diary.html", locals())



def info(request,id):
    member_name = request.session.get("member_name")
    comment_obj=Comment.objects.filter(article_id=id).all()
    res=comment_obj.count()#计算有多少子对象
    art_obj=Article.objects.filter(article_id=id).first()
    art_obj_praise = Article.objects.all().order_by('article_praise_num')[:4]
    art_obj_1 = Article.objects.filter(article_is_recommend=1).first()
    art_obj_last=Article.objects.values("article_id").last()
    art_last_id=art_obj_last["article_id"]
    member_id = request.session.get("member_id")
    click_addtime = time.strftime("%Y-%m-%d", time.localtime())
    cli=Click.objects.create(member_id=member_id, article_id=id, click_addtime=click_addtime)
    num=int(Article.objects.get(article_id=id).article_clicknum)+1
    Article.objects.filter(article_id=id).update(article_clicknum=num)


    if int(id)==1 :
        comment_content = request.POST.get("")
        art_obj_last = Article.objects.filter(article_id=id).first()
        art_obj_next = Article.objects.filter(article_id__gt=id).first()
    elif art_last_id==id:
        art_obj_last = Article.objects.filter(article_id__lt=id).first()
        art_obj_next = Article.objects.filter(article_id=id).first()
    else:
        art_obj_last=Article.objects.filter(article_id__lt=id).first()
        art_obj_next=Article.objects.filter(article_id__gt=id).first()

    return render(request, "login/text.html", locals())


def diary_person(request,id):

    member_name = request.session.get("member_name")
    now_id = request.session.get('member_id')
    art_obj=Article.objects.filter(member_id=id).all()
    art_obj_praise = Article.objects.all().order_by('article_praise_num')[:4]
    art_obj_1 = Article.objects.filter(article_is_recommend=1).first()

    return render(request, "login/diary_person.html", locals())
def praise(request):
    import json
    res={"status":None,"info":None}
    praise_num=request.POST.get("praise")
    article_id=request.POST.get("article_id")
    member_id = request.session.get("member_id")
    praise_addtime = time.strftime("%Y-%m-%d", time.localtime())
    praise_obj=Praise.objects.filter(member_id_id=member_id,article_id_id=article_id).first()
    # print(article_id,praise_num,member_id,praise_obj)

    if not praise_obj:
        res["status"]=1
        res["info"]="点赞成功"
        article_obj = Article.objects.filter(article_id=article_id).update(article_praise_num=praise_num)
        pra = Praise.objects.create(member_id_id=member_id, article_id_id=article_id, praise_addtime=praise_addtime)
    else:
        res["status"]=0
        res["info"]="点赞失败 每个人只能点一次哦"


    return HttpResponse(json.dumps(res))

    # return render(request, "login/text.html", locals())


def comment(request,id):
    if request.method == 'POST':
        # article_img = request.session.get("article_img")
        valid_code_str = request.session.get("valid_code_str")
        key = request.POST.get("key")
        if key.upper() == valid_code_str.upper():
            member_id = request.session.get("member_id")
            comment_content = request.POST.get("saytext")
            comment_addtime = time.strftime("%Y-%m-%d", time.localtime())
            print(id,member_id,comment_content,comment_addtime)
            comment_obj=Comment.objects.create(article_id=id,comment_addtime=comment_addtime,comment_content=comment_content,
                                               member_id=member_id)
        else:

            return redirect("/diary/info/{}".format(id))


    return redirect("/diary/info/{}".format(id))
