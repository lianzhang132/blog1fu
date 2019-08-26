from django.shortcuts import render,HttpResponse,redirect
from app01.utils import function
from app01.models import Article
from app01.models import Click
from app01.models import Praise
def click(request):
    from django.db.models import Sum
    recent_seven_days = function.recent_seven_days()
    list_week_day = recent_seven_days[::-1]  # 进行倒序
    clicknum_list=[]
    praise_num_list=[]
    for v in list_week_day:
        # res=Article.objects.filter(article_addtime__icontains=v).aggregate(clicknum=Sum('article_clicknum'),praise_num=Sum('article_praise_num'))
        # v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id'))
        clicknum =Click.objects.filter(click_addtime__icontains=v).count()
        praise_num =Praise.objects.filter(praise_addtime__icontains=v).count()

        # clicknum=res['clicknum']          if (res['clicknum'] is not None) else 0 #如果res【clicknum】 不为空 则赋值给前面 否则 赋值0
        # praise_num = res['praise_num']         if (res['praise_num'] is not None) else 0

        print(v, praise_num, clicknum)

        # clicknum = res['clicknum']
        # if clicknum==None:
        #     clicknum=0
        clicknum_list.append(clicknum)

        # praise_num = res['praise_num']
        # if praise_num==None:
        #     praise_num=0
        praise_num_list.append(praise_num)

    # data=[{
    #     'name': '点击量',
    #     'data': clicknum_list
    # }, {
    #     'name': '点赞量',
    #     'data': praise_num_list
    # }]

    # num= [ '20190624', '20190625', '20190626', '20190627', '20190628', '20190629', '20190630']
    return render(request,'statistics/click.html',locals())