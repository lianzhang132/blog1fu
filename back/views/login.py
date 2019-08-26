from django.shortcuts import render,HttpResponse,redirect
from back.models import Users
from django.contrib.auth.hashers import make_password, check_password
from app01.utils import validCode,sendMsg,function

def  login(request):
    try:
        res = {'status': None, 'info': None}
        if request.method == "POST":
            valid_code = request.POST.get("validimg1")
            valid_code_str = request.session.get("valid_code_str")
            # print(1111)
            # print(valid_code,valid_code_str)

            if valid_code.upper() == valid_code_str.upper():
                # print(valid_code)
                username = request.POST.get("lname")
                pwd = request.POST.get("pword")
                isLogin = Users.objects.filter(user_name=username).first()

                res2 = check_password(pwd,isLogin.user_pwd)


                if (isLogin and  res2):
                    res['status'] = 1
                    res['info'] = '登录成功'
                    request.session['user_name'] = isLogin.user_name
                    request.session['user_id'] = isLogin.user_id
                    return redirect("/back/index/index/")
                else:
                    res['status'] = 0
                    res['info'] = '登录失败'
                    return redirect("/back/login/login/")
    except Exception as e:
        return redirect("/back/login/login/")

    return render(request, "login/login1.html", locals())

def logout(request):
    try :


        del request.session["user_name"]#删除session
        # request.session.flush()#删除所有session
        return redirect("/back/login/login/")
    except Exception as e :
        return redirect("/back/login/login/")


def get_valid_code_img(request):
    img_data = validCode.get_valid_code_img(request)
    return HttpResponse(img_data)