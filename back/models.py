from django.db import models


class Users(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=255,default="null")
    user_birthday=models.DateTimeField()
    user_work=models.CharField(max_length=255,default="null")
    user_pwd = models.CharField(max_length=999, default="null")
    user_tel=models.CharField(max_length=11,default="null")
    user_is_recommend=models.IntegerField(default="0")# '0：未审核    1：审核通过',
    user_adders=models.CharField(max_length=150,default="null")

    def __str__(self):
        return (self.user_name)
class Role(models.Model):
    role_id=models.AutoField(primary_key=True)
    role_name=models.CharField(max_length=255,null=True, blank=True,)
    role_access=models.CharField(max_length=255,null=True, blank=True,)
    roleuser=models.ManyToManyField(to="Users")

    def __str__(self):
        return (self.role_name)

class Menu(models.Model):
    menu_id=models.AutoField(primary_key=True)
    menu_name=models.CharField(max_length=255,null=True, blank=True,)
    menu_path=models.CharField(max_length=255,null=True, blank=True,)
    menu_pid=models.ForeignKey(verbose_name='关联的权限', to='Menu', null=True, blank=True, related_name='parents',
                            help_text='父id', on_delete=models.CASCADE)

    def __str__(self):
        return (self.menu_name)
class Permission(models.Model):
    permission_id=models.AutoField(primary_key=True)
    permission_name=models.CharField(max_length=255,null=True, blank=True,)
    permission_path=models.CharField(max_length=255,null=True, blank=True,)
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True, blank=True, help_text='null表示不是菜单;非null表示是二级菜单',on_delete=models.CASCADE)
    permission_pid=models.ForeignKey(verbose_name='关联的权限', to='Permission', null=True, blank=True, related_name='parents',
                            help_text='父id', on_delete=models.CASCADE)

    def __str__(self):
        return (self.permission_name)
