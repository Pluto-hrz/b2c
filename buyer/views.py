from django.shortcuts import render, redirect
from django.urls import reverse
# 调用models类
from user.models import User, Order, Buy, Sell, Tag, Comment
# 调用内置登录状态判断
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    login = 0
    if request.user:
        username = request.user.username
        et = User.objects.filter(username=username)
        if et:
            u = User.objects.get(username=username)
            if u.character == 1:
                login = 1
            elif u.character == 0:
                login = 2
            else:
                login = 0
    things = Sell.objects.all()
    if request.method == "POST":
        search = request.POST.get('search')
        things = things.filter(introduce__contains=search).all()
    return render(request, 'home.html', locals())


@login_required
def index_buyer(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 1:
        return redirect(reverse("seller:index_seller"))
    else:
        things = Sell.objects.order_by('-create_time')[:5]
        orders = Order.objects.filter(buyer_name=username)
    return render(request, 'index_buyer.html', locals())



def thing(request, thing_id):
    login = 0
    if request.user:
        username = request.user.username
        et = User.objects.filter(username=username)
        if et:
            u = User.objects.get(username=username)
            if u.character == 1:
                login = 1
            elif u.character == 0:
                login = 2
            else:
                login = 0
    thing = Sell.objects.get(id=thing_id)
    thing_comment = thing.comment_set.all()
    tags = thing.tag_set.all()
    return render(request, 'thing.html', locals())


@login_required
def comment_add(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        thing_id = request.POST.get('thing_id')
        user = request.POST.get('user')
        c = Comment()
        c.comment = comment
        c.user = user
        c.thing_id = thing_id
        c.save()
    return render(request, 'comment_add.html', locals())


@login_required
def comment_delete(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        thing_id = request.POST.get('thing_id')
        comment_delete = Comment.objects.filter(comment=comment).first()
        comment_delete.delete()
    return render(request, 'comment_delete.html', locals())


@login_required
def buy_car(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 1:
        return redirect(reverse("seller:index_seller"))
    else:
        buys = u.buy_set.all()
        for b in buys:
            thing_id = b.thing_id
            t = Sell.objects.get(id=thing_id)
            b.name = t.name
            b.photo = t.photo
            b.introduce = t.introduce
            b.price = t.price
            b.spare = t.spare
            b.xiaoliang = t.xiaoliang
            b.save()
    return render(request, 'buy_car.html', locals())


@login_required
def buy_car_add(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 1:
        return redirect(reverse("seller:index_seller"))
    else:
        thing_id = request.POST.get('thing_id')
        num = request.POST.get('num')
        t = Sell.objects.get(id=thing_id)
        ex = Buy.objects.filter(thing_id=thing_id)
        if not ex:
            b = Buy()
            b.thing_id = thing_id
            b.name = t.name
            b.photo = t.photo
            b.introduce = t.introduce
            b.price = t.price
            b.spare = t.spare
            b.xiaoliang = t.xiaoliang
            b.num = int(num)
            b.buyer = u
            b.save()
        else:
            b = Buy.objects.get(thing_id=thing_id)
            if b.num > 0:
                b.num = b.num + int(num)
            b.name = t.name
            b.photo = t.photo
            b.introduce = t.introduce
            b.price = t.price
            b.spare = t.spare
            b.xiaoliang = t.xiaoliang
            b.save()
    return render(request, 'buy_car_add.html', locals())


@login_required
def buy_car_delete(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 1:
        return redirect(reverse("seller:index_seller"))
    else:
        thing_id = request.POST.get('thing_id')
        buy = Buy.objects.get(thing_id=thing_id)
        buy.delete()
    return render(request, 'buy_car_delete.html', locals())


@login_required
def order_add(request, thing_id, num):
    username = request.user.username
    t = Sell.objects.get(id=thing_id)
    u = User.objects.get(username=username)
    tags = t.tag_set.all()
    result = ''
    if u.character == 1:
        return redirect(reverse("seller:index_seller"))
    else:
        if request.method == 'GET':
            num = request.POST.get('num')if request.POST.get('num') else num
        ex = Sell.objects.filter(id=thing_id)
        if request.method == 'POST':
            if not ex:
                result = '该商品不存在'
            elif u.money < t.price * float(request.POST.get('num')):
                result = '您的余额不足，请及时充值！'
            elif int(request.POST.get('num')) > t.spare:
                result = '库存不足，请少买点！'
            elif t.state == 0:
                result = '该商品已经下架！'
            elif t.seller.is_active == 0:
                result = '商家账户已被冻结！'
            else:
                order = Order()
                order.state = '订单待处理'
                order.num = request.POST.get('num')
                order.buyer_name = username
                order.seller_name = t.seller.username
                order.thing_name = t.name
                order.thing_photo = t.photo
                order.mobile = u.mobile
                order.address = u.address
                order.one_price = t.price
                order.thing_id = t.id
                order.all_price = float(t.price) * float(request.POST.get('num'))
                order.save()
                t.spare = t.spare - int(request.POST.get('num'))
                t.xiaoliang = t.xiaoliang + int(request.POST.get('num'))
                t.save()
                u.money = u.money - t.price * float(request.POST.get('num'))
                u.save()
                exit = Buy.objects.filter(thing_id=thing_id)
                if exit:
                    buy = Buy.objects.get(thing_id=thing_id)
                    buy.delete()
                return render(request, 'order_success.html', locals())
    return render(request, 'order_add.html', locals())


@login_required
def order_success(request):
    username = request.user.username
    u = User.objects.get(username=username)
    if u.character == 1:
        return redirect(reverse("seller:index_seller"))
    else:
        pass
    return render(request, 'buy_car_delete.html', locals())



