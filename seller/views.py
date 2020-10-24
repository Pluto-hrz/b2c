from django.shortcuts import render, redirect
from django.urls import reverse
import re
# 用于图片转换
import base64
# 调用models类
from user.models import User, Order, Buy, Sell, Tag, Comment
# 调用内置登录状态判断
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index_seller(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        things = u.sell_set.all()
        orders = Order.objects.filter(seller_name=username)
    return render(request, 'index_seller.html', locals())


@login_required
def things_output(request):
    result = ''
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        if request.method == 'POST':
            user_id = request.user.id
            name = request.POST.get('name')
            introduce = request.POST.get('introduce')
            price = request.POST.get('price')
            spare = request.POST.get('spare')
            photo = request.FILES.get('photo').file.read() if request.FILES.get('photo') else None
            state = True if request.POST.get('character') else False
            xiaoliang = 0
            pr = re.findall(r'^[0-9]+\.[0-9]{2}$', price)
            sp = re.findall(r'^[1-9][0-9]*$', spare)
            ex1 = Sell.objects.filter(name=name)
            ex2 = Sell.objects.filter(introduce=introduce)
            ex3 = Sell.objects.filter(photo=photo)
            if not (pr and pr[0] == price):
                result = '商品价格格式不正确'
                return render(request, 'things_output.html', locals())
            elif not (sp and sp[0] == spare):
                result = '商品库存格式不正确'
                return render(request, 'things_output.html', locals())
            elif photo == None:
                result = '商品图片不能为空'
                return render(request, 'things_output.html', locals())
            elif ex1 or ex2 or ex3:
                result = '商品信息已存在'
                return render(request, 'things_output.html', locals())
            else:
                t = Sell()
                t.seller_id = u.id
                t.name = name
                t.introduce = introduce
                t.price = price
                t.spare = spare
                t.photo = base64.b64encode(photo).decode('utf8')
                t.state = state
                t.xiaoliang = xiaoliang
                t.save()
                result = '商品发布成功'
    return render(request, 'things_output.html', locals())


@login_required
def tags_add(request, thing_id):
    result = ''
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        if request.method == 'POST':
            user_id = request.user.id
            tag = request.POST.get('tag')
            ex = Sell.objects.filter(seller=user_id)
            if ex:
                if tag == '':
                    result = '标签不能为空'
                else:
                    t = Tag()
                    t.thing_id = thing_id
                    t.tag = tag
                    t.save()
                    result = '标签添加成功'
    return render(request, 'tags_add.html', locals())


@login_required
def comment_answer(request):
    result = ''
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    if request.method == 'POST':
        user_id = request.user.id
        answer = request.POST.get('answer')
        thing_id = request.POST.get('thing_id')
        comment = request.POST.get('comment')
        if not answer:
            c = Comment.objects.get(comment=comment)
            c.answer = answer
            c.save()
    return render(request, 'comment_answer.html', locals())


@login_required
def things_manage(request):
    result = ''
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        things = u.sell_set.all()
    return render(request, 'things_manage.html', locals())


@login_required
def things_shangjia(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        if request.method == 'POST':
            id = request.POST.get('id')
            ex = Sell.objects.filter(id=id).first()
            if ex:
                ex.state = 1
                ex.save()
    return render(request, 'things_shangjia.html', locals())


@login_required
def things_xiajia(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        if request.method == 'POST':
            id = request.POST.get('id')
            ex = Sell.objects.filter(id=id).first()
            if ex:
                ex.state = 0
                ex.save()
    return render(request, 'things_xiajia.html', locals())


@login_required
def things_delete(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        if request.method == 'POST':
            id = request.POST.get('id')
            ex = Sell.objects.filter(id=id).first()
            if ex:
                ex.delete()
    return render(request, 'things_delete.html', locals())


@login_required
def things_correct(request, thing_id):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        if request.method == 'GET':
            th = Order.objects.filter(thing_id=thing_id).all()
            for i in th:
                if i.state == '订单待处理':
                    return redirect(reverse("seller:things_manage"))
                else:
                    pass
            os = Order.objects.filter(seller_name=u.username).all()
            for o in os:
                if o.state == 0:
                    return redirect(reverse("seller:things_manage"))
            if request.method == 'POST':
                name = request.POST.get('name')
                introduce = request.POST.get('introduce')
                price = request.POST.get('price')
                spare = request.POST.get('spare')
                photo = request.FILES.get('photo').file.read() if request.FILES.get('photo') else None
                pr = re.findall(r'^[0-9]+\.[0-9]{2}$', price)
                sp = re.findall(r'^[1-9][0-9]*$', spare)
                ex1 = Sell.objects.filter(name=name)
                ex2 = Sell.objects.filter(introduce=introduce)
                ex3 = Sell.objects.filter(photo=photo)
                if not (pr and pr[0] == price):
                    result = '商品价格格式不正确'
                    return render(request, 'things_output.html', locals())
                elif not (sp and sp[0] == spare):
                    result = '商品库存格式不正确'
                    return render(request, 'things_output.html', locals())
                elif ex1 or ex2 or ex3:
                    result = '商品信息已存在'
                    return render(request, 'things_output.html', locals())
                else:
                    t = Sell.objects.filter(id=thing_id).first()
                    t.name = name
                    t.introduce = introduce
                    t.price = price
                    t.spare = spare
                    if photo != None:
                        t.photo = base64.b64encode(photo).decode('utf8')
                    t.save()
                    result = '商品修改成功'
    return render(request, 'things_correct.html', locals())


@login_required
def order_request(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 0:
        return redirect(reverse("buyer:index_buyer"))
    else:
        if request.method == 'POST':
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            buyer_name = order.buyer_name
            buyer = User.objects.get(username=buyer_name)
            money = order.all_price
            seller_name = order.seller_name
            seller = User.objects.get(username=seller_name)
            seller.money = seller.money + money
            order.state = '交易成功'
            buyer.save()
            seller.save()
            order.save()
    return render(request, 'order_request.html', locals())


@login_required
def order_unsuccess(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        num = order.num
        thing_name = order.thing_name
        thing = Sell.objects.get(name=thing_name)
        thing.spare = thing.spare + num
        thing.xiaoliang = thing.xiaoliang - num
        buyer_name = order.buyer_name
        buyer = User.objects.get(username=buyer_name)
        money = order.all_price
        buyer.money = buyer.money + money
        order.state = '交易失败'
        buyer.save()
        thing.save()
        order.save()
    return render(request, 'order_unsuccess.html', locals())







