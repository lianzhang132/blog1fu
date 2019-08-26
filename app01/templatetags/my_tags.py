from django import template
from app01.models import Article
register=template.Library()

@register.simple_tag
def multi_tag(x,y):
    return x*y


@register.inclusion_tag('login/rightpart.html')
def rightArticle():
    art_obj_praise = Article.objects.all().order_by('article_praise_num')[:4]
    article_is_recommend_list = Article.objects.filter(article_is_recommend="1")[:3]
    return {'art_obj_praise':art_obj_praise,'article_is_recommend_list':article_is_recommend_list}

