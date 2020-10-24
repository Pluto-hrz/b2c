from django.shortcuts import render, redirect
from django.urls import reverse
# 内置user的登录注销以及判断登录
from django.contrib.auth import login as log_in
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
# 用于密码加密解密
from django.contrib.auth.hashers import make_password, check_password
# 引入form表单和model类
from b2c.forms import UserForm
from user.models import User, Order, Buy, Sell, Tag
# 用于发送邮件
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
# 用于图片转换
import base64
# 用于正则表达式
import re


# Create your views here.

def login(request):
    result = ''
    myform = UserForm()
    if request.method == "POST":
        myform = UserForm(request.POST)
        if myform.is_valid():
            user = User.objects.filter(username=request.POST.get('username')).first()
            log_in(request, user)
            if user.character == 0:
                return redirect(reverse("buyer:index_buyer"))
            else:
                return redirect(reverse("seller:index_seller"))
        else:
            result = myform.errors.get('__all__').data[0].message if myform.errors.get('__all__') \
                else myform.errors.get('captcha').data[0].message
    else:
        result = ''
    return render(request, 'login.html', locals())


def register(request):
    result = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        image = request.FILES.get('image').file.read() if request.FILES.get('image') else None
        character = True if request.POST.get('character') else False
        money = 0.88
        un = re.findall(r"^[a-z0-9_]{6,16}$", username)
        pd = re.findall(r"^[a-z0-9_.]{6,16}$", password)
        em = re.findall(r"^[a-z0-9]+[@][a-z0-9]+\.com|cn$", email)
        mb = re.findall(r"^1\d{10}$", mobile)
        exist_user = User.objects.filter(username=username)
        if exist_user:
            result = '用户名已存在'
            return render(request, 'register.html', locals())
        elif not(un and un[0] == username):
            result = '用户名格式不正确'
            return render(request, 'register.html', locals())
        elif not(pd and pd[0] == password):
            result = '密码格式不正确'
            return render(request, 'register.html', locals())
        elif not(em and em[0] == email):
            result = '邮箱格式不正确'
            return render(request, 'register.html', locals())
        elif not(mb and mb[0] == mobile):
            result = '手机号格式不正确'
            return render(request, 'register.html', locals())
        elif image == None:
            result = '请上传头像'
            return render(request, 'register.html', locals())
        else:
            u = User()
            u.username = username
            u.password = make_password(password)
            u.email = email
            u.address = address
            u.mobile = mobile
            u.image = base64.b64encode(image).decode('utf8')
            u.character = character
            u.money = money
            u.save()
            result = '注册成功'
            return render(request, 'register.html', locals())
    myform = UserForm()
    return render(request, 'register.html', locals())


def xie_yi(request):
    # 本文件借鉴自淘宝，严禁外用
    return render(request, 'xie_yi.html', locals())


@login_required
def logout(request):
    log_out(request)
    return render(request, 'logout.html', locals())


@login_required
def correct_password(request):
    user = request.user
    result = ''
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')
        if user.check_password(old_password):
            if not new_password:
                result = '新密码不能为空'
            elif new_password != repeat_password:
                result = '两次密码不一致'
            else:
                pd = re.findall(r"^[a-z0-9_.]{6,16}$", new_password)
                if not(pd and pd[0] == new_password):
                    result = '新密码格式不正确'
                else:
                    user.set_password(new_password)
                    user.save()
                    return redirect(reverse("buyer:home"))
        else:
            result = '原密码输入错误'
    return render(request, 'correct_password.html', locals())


def forget_password(request):
    result = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        exit_user = User.objects.filter(username=username)
        if exit_user:
            u = User.objects.get(username=username)
            my_sender = '1559492576@qq.com'  # 发件人邮箱账号
            my_pass = 'meppaiqclftvjgfb'  # 发件人邮箱密码
            my_user = u.email  # 收件人邮箱账号，我这边发送给自己

            def mail():
                ret = True
                try:
                    text = '您的密码找回链接为' + 'http://127.0.0.1:8000/user/forget_correct_password/' + str(u.id) + '/'
                    msg = MIMEText(text, 'plain', 'utf-8')
                    msg['From'] = formataddr(["From购物网", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                    msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                    msg['Subject'] = "忘记密码找回"  # 邮件的主题，也可以说是标题

                    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
                    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                    server.quit()
                except Exception:
                    ret = False
                return ret
            ret = mail()
            if ret:
                result = '邮件发送成功'
                u.is_active = 0
            else:
                result = '邮件发送失败'
        else:
            result = '用户名不存在'
    return render(request, 'forget_password.html', locals())


def forget_correct_password(request, user_id):
    result = ''
    user = User.objects.get(id=user_id)
    if user.is_active == 1:
        return render(request, 'forget_password.html', locals())
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')
        if not new_password:
            result = '新密码不能为空'
        elif new_password != repeat_password:
            result = '两次密码不一致'
        else:
            pd = re.findall(r"^[a-z0-9_.]{6,16}$", new_password)
            if not (pd and pd[0] == new_password):
                result = '新密码格式不正确'
            else:
                user.set_password(new_password)
                user.is_active = 1
                user.save()
                return redirect("/user/login/")
    return render(request, 'forget_correct_password.html', locals())


@login_required
def money(request):
    result = ''
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 1:
        return redirect(reverse("seller:index_seller"))
    else:
        if request.method == 'POST':
            add_money = request.POST.get('add')
            u.money = float(u.money) + float(add_money)
            u.save()
            result = '充值成功'
    return render(request, 'money.html', locals())


@login_required
def user_correct(request):
    result = ''
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        image = request.FILES.get('image').file.read() if request.FILES.get('image') else None
        un = re.findall(r"^[a-z0-9_]{6,16}$", username)
        em = re.findall(r"^[a-z0-9]+[@][a-z0-9]+\.com|cn$", email)
        mb = re.findall(r"^1\d{10}$", mobile)
        if username != name and User.objects.filter(username=name):
            result = '用户名已存在'
            return render(request, 'user_correct.html', locals())
        elif not (un and un[0] == username):
            result = '用户名格式不正确'
            return render(request, 'user_correct.html', locals())
        elif not (em and em[0] == email):
            result = '邮箱格式不正确'
            return render(request, 'user_correct.html', locals())
        elif not (mb and mb[0] == mobile):
            result = '手机号格式不正确'
            return render(request, 'user_correct.html', locals())
        else:
            user.username = name
            user.email = email
            user.address = address
            user.mobile = mobile
            if image != None:
                user.image = base64.b64encode(image).decode('utf8')
            user.save()
            result = '修改成功'
            return render(request, 'user_correct.html', locals())
    return render(request, 'user_correct.html', locals())











