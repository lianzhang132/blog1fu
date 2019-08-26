from django.shortcuts import render,HttpResponse,redirect

def if_sess1(function):
    def wer(request):
        try:
            if request.session['member_name']:
                # print(request.session['member_name'])
                return function(request)
        except Exception as e :
            # print("sess1")
            return redirect("/login/")
    return wer



def if_sess2(function):
    def wer(request):
        try:
            if request.session['user_name']:
                return function(request)
        except Exception as e :
            return redirect("/back/login/login/")
    return wer
