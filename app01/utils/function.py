from django.shortcuts import render,HttpResponse,redirect
import random
from app01.models import Comment
from app01.models import Member
from app01.models import Article


def range_num(num):
    # 定义一个种子，从这里面随机拿出一个值，可以是字母
    seeds = "1234567890"
    # 定义一个空列表，每次循环，将拿到的值，加入列表
    random_num = []
    # choice函数：每次从seeds拿一个值，加入列表
    for i in range(num):
        random_num.append(random.choice(seeds))
    # 将列表里的值，变成四位字符串
    return "". join(random_num)#5454
def getWhere(request):
    where = dict()
    article_title=request.POST.get('article_title','')
    article_is_recommend = request.POST.get('article_is_recommend', '')
    member_id = request.POST.get('member_id', '')
    if article_title:
        where['article_title__icontains']=article_title
    if article_is_recommend!='':
        where['article_is_recommend'] = article_is_recommend
    if member_id:
        where['member'] = member_id
    # print(where)
    return where
def getWhere_user(request):
    where = dict()
    user_name=request.POST.get('user_name','')
    user_is_recommend = request.POST.get('user_is_recommend', '')
    user_work = request.POST.get('user_work', '')
    user_tel = request.POST.get('user_tel', '')
    # print(user_name,user_work,user_tel,user_is_recommend)
    if user_name:
        where['user_name__icontains']=user_name
    if user_is_recommend!='':
        where['user_is_recommend'] = user_is_recommend
    if user_work:
        where['user_work'] = user_work
    if user_tel:
        where['user_tel'] = user_tel
    # print(where)
    return where
def getWhere_member(request):
    where = dict()
    member_name=request.POST.get('member_name','')
    member_nickname = request.POST.get('member_nickname', '')
    member_email = request.POST.get('member_email', '')
    member_tel = request.POST.get('member_tel', '')
    # print(user_name,user_work,user_tel,user_is_recommend)
    if member_name:
        where['member_name__icontains']=member_name
    if member_nickname:
        where['member_nickname__icontains'] = member_nickname
    if member_email:
        where['member_email__icontains'] = member_email
    if member_tel:
        where['member_tel'] = member_tel
    # print(where)
    return where
def getWhere_comment(request):
    where = dict()
    member_id=request.POST.get('member_id','')
    # member_id=Member.objects.filter(member_name=member_name).first().member_id
    article_id = request.POST.get('article_id', '')
    # article_id=Article.objects.filter(article_title=article_title).first().article_id
    comment_content = request.POST.get('comment_content', '')

    # print(user_name,user_work,user_tel,user_is_recommend)
    if comment_content:
        where['comment_content__icontains']=comment_content
    if article_id:
        where['article'] = article_id
    if member_id:
        where['member'] = member_id
    # print(where)
    return where
def getWhere_praise(request):
    where = dict()
    member_id=request.POST.get('member_id','')
    # member_id=Member.objects.filter(member_name=member_name).first().member_id
    article_id = request.POST.get('article_id', '')
    # article_id=Article.objects.filter(article_title=article_title).first().article_id

    if article_id:
        where['article_id'] = article_id
    if member_id:
        where['member_id'] = member_id
    # print(where)
    return where

def getWhere_menu(request):
    where = dict()
    menu_name=request.POST.get('menu_name','')
    menu_path = request.POST.get('menu_path', '')
    # menu_pid_id = request.POST.get('menu_pid_id', '')
    # menu_pid_i => 0
    # print(menu_pid_id,"dd")

    if menu_name:
        where['menu_name__icontains'] = menu_name
    if menu_path:
        where['menu_path__icontains'] = menu_path
    # if menu_pid_id:
    #     where['menu_pid_id__lt'] = menu_pid_id


    return where
def getWhere_permission(request):
    where = dict()
    permission_name=request.POST.get('permission_name','')
    permission_path = request.POST.get('permission_path', '')
    # menu_pid_id = request.POST.get('menu_pid_id', '')
    # menu_pid_i => 0
    print(permission_name,permission_path)

    if permission_name:
        where['permission_name__icontains'] = permission_name
    if permission_path:
        where['menu_path__icontains'] = permission_path
    # if menu_pid_id:
    #     where['menu_pid_id__lt'] = menu_pid_id


    return where
def getWhere_role(request):
    where = dict()
    role_name=request.POST.get('role_name','')
    role_access = request.POST.get('role_access', '')
    if role_name:
        where['role_name__icontains']=role_name
    if role_access:
        where['role_access__icontains'] = role_access
    return where

def recent_seven_days():# 通过for 循环得到天数，如果想得到两周的时间，只需要把8改成15就可以了。
    import datetime
    d = datetime.datetime.now()#2019-6-28 9:25:43.843164
    lists = []
    for i in range(1,8):#i:1-7
        oneday = datetime.timedelta(days=i) #1 day, 0:00:00     2 days, 0:00:00 ... 7 days, 0:00:00
        day = d - oneday#2019-06-27 11:32:10.186535  2019-06-26 11:32:10.186535 ... 2019-06-21 11:32:10.186535
        date_to = datetime.datetime(day.year, day.month, day.day)#2019-06-27 00:00:00   2019-06-26 00:00:00  ...  2019-06-21 00:00:00
        lists.append(str(date_to)[0:10])#2019-06-27  2019-06-26  ... 2019-06-21
    return lists


def if_sess1(request):
    try:
        sess1 = request.session.get("member_id")
        if sess1:
            return None
        else:
            return redirect("/login/")
    except Exception as e:
        return redirect("/login/")


def if_sess2(request):
    try:
        sess1 = request.session.get("user_name")
        if sess1:
            return None
        else:
            return redirect("/back/login/login/")
    except Exception as e:
        return redirect("/back/login/login/")


