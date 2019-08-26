from django.shortcuts import render,HttpResponse,redirect
from app01.models import Article
from app01.models import mesboard
from app01.views.prelogin import *
from app01.my_forms import *
from django.contrib.auth.hashers import make_password, check_password
from app01.utils import validCode,sendMsg,function
from app01.utils import sendMsg #引入自定义的验证码
from app01.utils import function #引入自定义的验证码
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import time
from django.db.models import F,Q
from bs4 import BeautifulSoup



# Create your views here.
def  login(request):
    try:
        res = {'status': None, 'info': None}
        if request.method == "POST":
            valid_code = request.POST.get("validimg1")
            valid_code_str = request.session.get("valid_code_str")
            # print(1111)
            print(valid_code,valid_code_str)

            if valid_code.upper() == valid_code_str.upper():
                # print(valid_code)
                username = request.POST.get("lname")
                pwd = request.POST.get("pword")
                isLogin = Member.objects.filter(member_name=username).first()

                request.session['member_name'] = isLogin.member_name
                request.session['member_id'] = isLogin.member_id
                # print(isLogin.member_id)

                res2 = check_password(pwd,isLogin.member_pwd)


                if (isLogin and  res2):
                    res['status'] = 1
                    res['info'] = '登录成功'
                    return redirect("/")
                else:
                    res['status'] = 0
                    res['info'] = '登录失败'
                    return redirect("/login/")
    except Exception as e:

        return render(request, "login/login.html", locals())

    return render(request, "login/login.html", locals())

# @if_sess1
def  index1(request):
    import datetime
    atical_obj = Article.objects.all()
    art_obj_praise = Article.objects.all().order_by('article_praise_num')[:4]
    article_is_recommend_list=Article.objects.filter(article_is_recommend="1")[:3]
    now = datetime.datetime.now()
    rec = now -datetime.timedelta(days=10)

    member_name = request.session.get('member_name')
    now_id = request.session.get('member_id')


    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    article_new_list=Article.objects.filter(article_addtime__range=(rec,now)).order_by("article_clicknum")
    paginator = Paginator(article_new_list, 3)
    # print(paginator.num_pages)  # 总页数
    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1,paginator.num_pages)

    try:
        article_new_list = paginator.page(currentPage)
    except PageNotAnInteger:
        article_new_list = paginator.page(1)
    except EmptyPage:
        article_new_list = paginator.page(paginator.num_pages)

    # print(pageRange)
    return render(request, "login/index1.html", locals())
def main_part(request):
    articles_list = Article.objects.all().order_by("article_clicknum")

    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(articles_list, 6)

    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)

    try:
        articles_list = paginator.page(currentPage)
    except PageNotAnInteger:
        articles_list = paginator.page(1)
    except EmptyPage:
        articles_list = paginator.page(paginator.num_pages)

    return render(request, "login/main_part.html", locals())

def modif(request,id):
    member_obj = Member.objects.all()
    article_obj = Article.objects.filter(pk=id).first()
    article_content=article_obj.article_content
    # article_addtime=article_obj.article_addtime
    # member_name = article_obj.member.member_name
    article_title = article_obj.article_title
    article_img = article_obj.article_img
    # article_clicknum = article_obj.article_clicknum
    # article_is_recommend = article_obj.article_is_recommend
    # print(article_clicknum,article_is_recommend)
    #当点击提交按钮的时候才执行：
    if request.method == 'POST':
        title = request.POST.get("article_title")
        content = request.POST.get("article_content")
        article_img = request.POST.get("article_img")
        # member = request.POST.get("member_name")
        # article_addtime = request.POST.get("article_addtime")
        print(content,title,article_img)
        # member_id = int(member_obj.filter(member_name=member).first().member_id)
        # print(member_id,member)
        # 防止xss攻击,过滤script标签
        soup = BeautifulSoup(content, "html.parser")  # 通过字符串创建BeautifulSoup对象，即将字符串转为对象，然后调用对象里的相关方法
        # print(
        #     soup.find_all())  # [<img alt="" src="/media/add_article_img/hand.png"/>, <script charset="utf-8" src="/static/blog/kindeditor/kindeditor-all.js"></script>,<img src="/media/add_article_img/thumb_50_img1.jpg" alt="" />]
        for tag in soup.find_all():

            print(tag.name)  # img   script
            if tag.name == "script":
                tag.decompose()
        desc = soup.text[0:150] + "..."
        Article.objects.filter(pk=id).update(article_title=title,article_img=article_img,article_content=str(soup))
        # Book.objects.filter(pk=id).update(title=title, price=price, publishDate=publishDate, publish_id=publish_id)
        return HttpResponse("修改成功")


    return render(request,'login/modif.html',locals())


def enroll(request):
    res = {'status': None, 'info': None}
    if request.method == "POST":
        form = UserForm(request.POST)  # 引用my_forms函数里的userform 钩子校验函数 进行钩子校验
        import json
        # print(form.is_valid())
        if not form.is_valid():  # is_valid 有值为假  没有值时为真
            # print(form.is_valid())

            res['status'] = 0
            res['info'] = form.errors
            return HttpResponse(json.dumps(res))
        valid_code = request.POST.get("validimg")
        validcode3 = request.POST.get("validcode")
        valid_code_str = request.session.get("valid_code_str")
        validcode = request.session['validcode']
        # print(validcode)


        # form = UserForm(request.POST)#引用my_forms函数里的userform 钩子校验函数 进行钩子校验
        # import json
        # print(form.is_valid())
        # if  not form.is_valid():#is_valid 有值为假  没有值时为真
        #     print(form.is_valid())
        #
        #     res['status'] = 0
        #     res['info'] = form.errors
        #     return HttpResponse(json.dumps(res))
        if validcode3:
            if validcode==validcode3:

                member_name = request.POST.get("member_name")
                member_nickname = request.POST.get("member_nickname")
                member_pwd = make_password(request.POST.get("member_pwd"))
                member_email = request.POST.get("member_email")
                member_tel = request.POST.get("member_tel")
                member_obj = Member.objects.create(member_name=member_name, member_nickname=member_nickname,
                                                   member_pwd=member_pwd, member_email=member_email,
                                                   member_tel=member_tel)

                if member_obj:
                    res['status'] = 1
                    res['info'] = '登录成功'
                else:
                    res['status'] = 2
                    res['info'] = '登录失败'
                import json
                response_new = HttpResponse(json.dumps(res))

                request.session['member_id'] = member_obj.member_id
                request.session['member_name'] = member_obj.member_name
                return response_new

            else:
                    res['status'] = 0
                    res['info'] = '短信验证码不正确'
                    return HttpResponse(json.dumps(res))  # 把这个结果告诉给前台，ajax
        else:
            res['status'] = 0
            res['info'] = '短信验证码不存在'
            return HttpResponse(json.dumps(res))  # 把这个结果告诉给前台，ajax

    return render(request, "login/enroll.html", locals())

def loginTel(request):
    res = {'status': None, 'info': None}
    if request.method == "POST":
        valid_code = request.POST.get("validimg")
        valid_code_str = request.session.get("valid_code_str")
        tel = request.POST.get('member_tel')
        # print(tel)
        if valid_code.upper() == valid_code_str.upper():
            import json
            #点击发送短信执行以下程序
            if request.POST.get('sendSms')=='1':
                range_num =function.range_num(4);#5454
                request.session['validcode'] =range_num
                result = sendMsg.request2(tel,range_num,"GET")
                if result=='ok':
                    res['status']=1
                    # res['info']='发送成功%s'%range_num
                    res['info'] = '发送成功'
                    return HttpResponse(json.dumps(res))#把这个结果告诉给前台，ajax
                else:
                    res['status']=0
                    res['info']='发送失败'
                    return HttpResponse(json.dumps(res))#把这个结果告诉给前台，ajax
    return render(request,'login/enroll.html', locals())



def get_valid_code_img(request):
    img_data = validCode.get_valid_code_img(request)
    return HttpResponse(img_data)

@if_sess1
def search(request):
    # like '%python%' 含有python 不区分大小写
    # book_list =Book.objects.filter(title__icontains='python')
    # book_list=Book.objects.filter(price=11).values('title').distinct()
    # res = Book.objects.filter(~Q(price=82) & Q(publish_id=2))
    if request.method == "POST":
        keyboard = request.POST.get("keyboard")
        if keyboard:
            art_obj=Article.objects.filter(Q(article_content__icontains=keyboard) &
                                           Q(article_title__icontains=keyboard)).distinct()
        else:
            art_obj=""

    return render(request, "login/search.html", locals())


# @if_sess1
def diary(request):
    member_name = request.session.get("member_name")
    atical_obj = Article.objects.all()

    return render(request, "login/diary.html", locals())
def diary_part(request):
    articles_list = Article.objects.all()



    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(articles_list, 7)

    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)

    try:
        articles_list = paginator.page(currentPage)
    except PageNotAnInteger:
        articles_list = paginator.page(1)
    except EmptyPage:
        articles_list = paginator.page(paginator.num_pages)


    return render(request, "login/diary_part.html", locals())



def diary_info(request,id):

    atical_obj = Article.objects.all()

    return render(request, "login/diary.html", locals())

@if_sess1
def about(request):
    member_name = request.session.get("member_name")
    return render(request, "login/about.html",locals())

@if_sess1
def gbook(request):
    mes_obj = mesboard.objects.all()
    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(mes_obj, 7)

    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)

    try:
        mes_obj = paginator.page(currentPage)
    except PageNotAnInteger:
        mes_obj = paginator.page(1)
    except EmptyPage:
        mes_obj = paginator.page(paginator.num_pages)
    if request.method == "POST":

        mesboard_name = request.POST.get("mesboard_name")
        mesboard_img= request.POST.get("mycall")
        mesboard_content = request.POST.get("content")
        mesboard_addtime = time.strftime( "%Y-%m-%d", time.localtime())
        mesboard_obj = mesboard.objects.create(mesboard_name=mesboard_name, mesboard_img=mesboard_img,
                                           mesboard_content=mesboard_content, mesboard_addtime=mesboard_addtime)

    return render(request, "login/gbook.html",locals())
@if_sess1
def study(request):
    import datetime
    now = datetime.datetime.now()  #获取现在的时间
    start = datetime.date(2018, 7, 12)#开始时间
    atical_obj = Article.objects.filter(article_addtime__range=(start,now))

    currentPage = int(request.GET.get('page', 1))  # 获取当前在第几页
    paginator = Paginator(atical_obj, 6)

    if paginator.num_pages > 11:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages + 1)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = range(1, paginator.num_pages + 1)

    try:
        atical_obj = paginator.page(currentPage)
    except PageNotAnInteger:
        atical_obj = paginator.page(1)
    except EmptyPage:
        atical_obj = paginator.page(paginator.num_pages)

    return render(request, "login/study.html",locals())

def study1(request):
    import datetime
    now = datetime.datetime.now()  #获取现在的时间
    start = datetime.date(2018, 7, 12)#开始时间
    atical_obj = Article.objects.filter(article_addtime__range=(start,now),article_is_recommend=1)

    return render(request, "login/study.html",locals())

def study2(request):
    import datetime
    now = datetime.datetime.now()  #获取现在的时间
    start = datetime.date(2018, 7, 12)#开始时间
    atical_obj = Article.objects.filter(article_addtime__range=(start,now),article_is_recommend=0)

    return render(request, "login/study2.html",locals())


@if_sess1
def share(request):
    article_praise_num = Article.objects.filter(article_praise_num__gt=1)
    return render(request, "login/share.html",locals())


def share1(request):
    article_praise_num = Article.objects.filter(article_praise_num__gt=1,article_is_recommend=1)[:10]
    return render(request, "login/share1.html",locals())

def share2(request):
    article_praise_num = Article.objects.filter(article_praise_num__gt=1,article_is_recommend=0)[:10]
    return render(request, "login/share2.html",locals())


def text(request):
    artical_obj=Article.objects.all()

    return render(request,"text{}.html".format(artical_obj.arttical_id))


#退出
def logout(request):
    try:


        del request.session["member_name"]#删除session
    except Exception as e:
        return redirect("/login/")
    return redirect("/login/")
@if_sess1
def findPwd(request):
    from django.core.mail import send_mail
    from blog1 import settings
    try:
        if request.method=='POST':
            member_name=request.POST.get('member_name')
            #根据member_name查找member表拿到member_email-98000@qq.com
            # member_email=Member.objects.filter(member_name=member_name).first().value("member_email")记住这样写是错的
            member_email=Member.objects.filter(member_name=member_name).first().member_email
            # 生成一个6位的随机数密码 123456
            range_num = function.range_num(6)
            #把密码加密，把member表根据member_name把member_pwd进行修改最新的密码
            member_pwd = make_password(range_num)
            print(member_name)
            Member.objects.filter(member_name=member_name).update(member_pwd=member_pwd)
            #发送邮件，把新密码发送给98000@qq.com
            # send_mail(
            #     '董鹏亚在找回密码',
            #     '您的密码已经被找回，新密码为123456',
            #     settings.EMAIL_HOST_USER,
            #     ['1072502827@qq.com']
            # )


            import threading
            t=threading.Thread(target=send_mail,args=(
                '%s在找回密码,'%(member_name),
                '您的密码已经被找回，新密码为%s'%(range_num),
                settings.EMAIL_HOST_USER,
                [member_email]
            ))
            t.start()
            return render(request, 'login/findPwd.html')
    except Exception as e:
        return render(request,'login/findPwd.html')
    return render(request, 'login/findPwd.html')