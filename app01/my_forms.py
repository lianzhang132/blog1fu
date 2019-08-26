from django import forms  #自动验证 # forms组件
from django.forms import widgets#自动生成input 框的插件
from django.core.exceptions import ValidationError

from app01.models import Member
class UserForm(forms.Form):
    wid_01 = widgets.TextInput(attrs={"class": "form-control"})#<input type='text' class="form-control">class 里是bootstrp的类约束样式
    wid_02 = widgets.PasswordInput(attrs={"class": "form-control"})#<input type='password' class="form-control">
    #前两条语句通过html中的类名 与html中的信息 相关联 起到验证作用  报错提示名字在 主页面 js语句中有定义详情可见 enroll页面203行

    member_email = forms.EmailField(label="邮箱", widget=wid_01, error_messages={"required": "该字段必填", "invalid": "格式不正确"})
    member_tel = forms.CharField(max_length=11, widget=wid_01, label="电话号码", )
    member_name=forms.CharField(max_length=6,min_length=2,label="用户名",widget=wid_01,error_messages={"required":"该字段必填"})
    member_pwd=forms.CharField(max_length=21,min_length=8,label="密码",widget=wid_02,error_messages={"required":"该字段必填"})
    r_pwd=forms.CharField(max_length=21,min_length=8,label="确认密码",widget=wid_02,error_messages={"required":"该字段必填"})
    validimg=forms.CharField(max_length=6,min_length=1,label="验证码",widget=wid_01,error_messages={"required":"该字段必填"})
    validcode=forms.CharField(max_length=6,min_length=1,label="短信验证码",widget=wid_01,error_messages={"required":"该字段必填"})
#前面对应html页面中的 name值 调用时先后验证 后面是验证条件以及报错信息
    # 局部钩子
    def clean_username(self):
        val = self.cleaned_data.get("member_name")#获取用户名的值
        res = Member.objects.filter(member_name=val)
        print(res)
        if not res:
            return val
        else:
            raise ValidationError("用户名已存在!")
    # 全局钩子
    def clean(self):
        pwd=self.cleaned_data.get("member_pwd")
        r_pwd=self.cleaned_data.get("r_pwd")
        if pwd and r_pwd:
            if pwd==r_pwd:
                # print(self.cleaned_data)
                return self.cleaned_data#这是一个干净的数据 正确的
            else:
                raise ValidationError('两次密码不一致!')
        else:
            return self.cleaned_data
