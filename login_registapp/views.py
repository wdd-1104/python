import random,string
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from login_registapp.captcha.image import ImageCaptcha
from homeapp.models import User
import hashlib

# 验证码
def getcaptcha(request):
    # 图片验证的对象
    image = ImageCaptcha()
    # 验证码随机组成   可控制长短   是一个列表
    codes = random.sample(string.ascii_letters+string.digits,4)
    # 把列表变成字符串
    codes = "".join(codes)
    # session记录验证码  注册时验证
    request.session["codes"] = codes
    # 图片上生成验证码
    date = image.generate(codes)
    return HttpResponse(date,"image/png")

# 登录页面
def login(request):
    uname = request.COOKIES.get("uname")
    upwd = request.COOKIES.get("upwd")
    a = User.objects.filter(e_mail=uname, password=upwd)
    if a:
        request.session["login"] = "ok"
        return redirect(reverse('homeapp:home')+'?e_mail='+uname)
    # 页面号码   存储
    page = request.GET.get('page')
    request.session['page'] = page
    return render(request,"login.html",{'page':page})

# 登录逻辑
def loginlogic(request):
    uname = request.POST.get('uname')
    upwd = request.POST.get('upwd')
    rem = request.POST.get('rem')
    # 对密码进行加密
    h1 = hashlib.sha256()
    h1.update(upwd.encode())
    pwd1 = h1.hexdigest()
    # 获取盐
    try:
        salt = User.objects.get(e_mail=uname).column_8
        pwd1 = pwd1 + salt
    except:
        pass
    a = User.objects.filter(e_mail=uname,password=pwd1)
    if a:
        page = request.session.get('page')
        request.session['uname'] = a[0].e_mail
        ren = HttpResponse('ok1')
        if page == '2':
            ren = HttpResponse('ok2')
        elif page == '3':
            ren = HttpResponse('ok3')
        # 购物车时
        elif page == '4':
            ren = HttpResponse('ok4')
        elif page == '5':
            ren = HttpResponse('ok5')
        if rem == 'true':
            ren.set_cookie("uname", uname, max_age=3600 * 24 * 2)
            ren.set_cookie("upwd", upwd, max_age=3600 * 24)
        user = User.objects.get(e_mail=uname)
        user.user_status="1"
        user.save()
        request.session['login'] = 'ok'
        return ren
    return HttpResponse("用户名或密码错误")

# 登陆判断验证码
def chackcaptcha1(request):
    number = request.POST.get("uyzm")
    code = request.session.get("codes")
    if number.lower() == code.lower():
        return HttpResponse("ok")
    else:
        return HttpResponse("0")

# 注册页面
def regist(request):
    page = request.GET.get('page')
    request.session['page'] = page
    return render(request,"register.html")

# 注册页面逻辑处理
def registlogic(request):
    uname = request.POST.get('uname')
    upwd = request.POST.get('upwd')
    # 对密码进行加密
    h1 = hashlib.sha256()
    h1.update(upwd.encode())
    pwd1 = h1.hexdigest()
    # 加盐加密
    s = '123134642561@#$%$#^%*&#$%TGSDFHDTYKZXFGADSFG'
    y = random.sample(s,5)
    y = ''.join(y)
    pwd1 = pwd1 + y
    User.objects.create(e_mail=uname,password=pwd1,user_status=1,column_8=y)  # 添加对象
    request.session['login'] = 'ok'
    a = User.objects.filter(e_mail=uname)[0]
    return HttpResponse(a.e_mail)


#  注册判断验证码
def chackcaptcha(request):
    number = request.POST.get("number")
    code = request.session.get("codes")
    if number.lower() == code.lower():
        return HttpResponse("1")
    return HttpResponse("0")

# 判断名字
def chackname(request):
    name = request.POST.get("name")
    a = User.objects.filter(e_mail=name)
    if a:
        return HttpResponse("0")
    return HttpResponse("1")


def registok(request):
    e_mail = request.GET.get("e_mail")
    request.session['uname'] =e_mail
    return render(request,'register ok.html',{'e_mail':e_mail})

# 退出
def quit(request):
    username = request.session.get('uname')
    u= User.objects.filter(e_mail=username)[0]
    u.user_status="0"
    u.save()
    request.session['login'] = 'no'
    del request.session['uname']
    request.session.clear()
    return HttpResponse("no")

# 处理跳转
def username(request):
    # request.session['uname'] = username
    page = request.session.get('page')
    ren = HttpResponse('ok1')
    if page == '2':
        ren = HttpResponse('ok2')
    elif page == '3':
        ren = HttpResponse('ok3')
    elif page == '4':
        ren = HttpResponse('ok4')
    elif page == '5':
        ren = HttpResponse('ok5')
    return ren
