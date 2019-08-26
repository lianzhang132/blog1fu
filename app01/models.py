from django.db import models

# Create your models here.
class Article(models.Model):
    article_id= models.AutoField(primary_key=True)
    article_title=models.CharField(max_length=255,default="null")
    article_description=models.CharField(max_length=255,default="null")
    article_addtime=models.DateField()
    article_clicknum=models.IntegerField(default=0)
    article_content=models.TextField()
    article_img=models.CharField(max_length=9999,default="null")
    member=models.ForeignKey(to="Member",on_delete=models.CASCADE)# member_id
    article_praise_num=models.IntegerField(default="0")
    article_is_recommend=models.IntegerField(default="0")# '0：不推荐    1：推荐',


    # praise = models.ManyToManyField(to="Member")
    def __str__(self):
        return (self.article_title)
class Comment(models.Model):
    comment_id=models.AutoField(primary_key=True)
    member=models.ForeignKey(to="Member",to_field="member_id",on_delete=models.CASCADE)# member_id
    article=models.ForeignKey(to="Article",to_field="article_id",on_delete=models.CASCADE)# article_id
    comment_content=models.CharField(max_length=255,default="")
    comment_addtime=models.DateField()
    def __str__(self):
        return (self.comment_content)
class Member(models.Model):
    member_id=models.AutoField(primary_key=True)
    member_name=models.CharField(max_length=255,default="null")
    member_tel=models.CharField(max_length=11,default="null")
    member_email=models.EmailField()
    member_nickname=models.CharField(max_length=60,default="null")
    member_pwd=models.CharField(max_length=999,default="null")
    def __str__(self):
        return (self.member_name)

    # praise = models.ManyToManyField(to="Article")

class Praise(models.Model):
    praise_id=models.AutoField(primary_key=True)
    member_id=models.ForeignKey(to="Member",to_field="member_id",on_delete=models.CASCADE)# article_id
    article_id=models.ForeignKey(to="Article",to_field="article_id",on_delete=models.CASCADE)# article_id
    praise_addtime = models.DateField(default=None)


class Click(models.Model):
    praise_id=models.AutoField(primary_key=True)
    member=models.ForeignKey(to="Member",to_field="member_id",on_delete=models.CASCADE)# article_id
    article=models.ForeignKey(to="Article",to_field="article_id",on_delete=models.CASCADE)# article_id
    click_addtime = models.DateField(default=None)

class Web(models.Model):
    web_id=models.AutoField(primary_key=True)
    web_name=models.CharField(max_length=255,default="null")
    web_content=models.TextField()
    def __str__(self):
        return (self.web_name)
class mesboard(models.Model):
    mesboard_id=models.AutoField(primary_key=True)
    mesboard_name=models.CharField(max_length=255,default="null")
    mesboard_img=models.CharField(max_length=999,default="null")
    mesboard_content=models.TextField()
    mesboard_addtime = models.DateField()
    def __str__(self):
        return (self.mesboard_name)