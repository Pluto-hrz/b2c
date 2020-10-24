from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    user = (
        (False, '买家'),
        (True, '商家'),
    )
    character = models.BooleanField(default=False, choices=user, verbose_name='用户身份')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    money = models.FloatField(default=0, verbose_name='账户余额')
    address = models.CharField(max_length=50, verbose_name='地址', default='')
    mobile = models.CharField(max_length=11, verbose_name='手机', default='')
    image = models.TextField(verbose_name='头像')


    def 用户状态(self):
        if self.is_active:
            return '正常'
        return '冻结'

    def __str__(self):
        return self.username


class Order(models.Model):
    seller_name = models.CharField(max_length=30, null=False, verbose_name='商家名称')
    buyer_name = models.CharField(max_length=30, null=False, verbose_name='买家名称')
    thing_name = models.CharField(max_length=30, null=False, verbose_name='商品名称')
    thing_photo = models.TextField(null=True, verbose_name='商品图片')
    mobile = models.CharField(max_length=30, null=False, verbose_name='手机')
    address = models.TextField(null=False, verbose_name='地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    state = models.CharField(max_length=30, verbose_name='订单状态', null=True)
    num = models.PositiveIntegerField(null=False, verbose_name='商品数量')
    one_price = models.FloatField(null=False, verbose_name='商品单价')
    all_price = models.FloatField(null=False, verbose_name='订单总价')
    thing_id = models.CharField(max_length=30, verbose_name='商品id', null=True)

    def __str__(self):
        return self.thing_name

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class Buy(models.Model):
    buyer = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL)
    thing_id = models.CharField(max_length=30, null=True, verbose_name='商品')
    num = models.PositiveIntegerField(null=False, verbose_name='数量')
    name = models.CharField(max_length=50, verbose_name='商品名称', null=False, unique=True)
    photo = models.TextField(verbose_name='商品图片')
    introduce = models.TextField(verbose_name='商品简介')
    price = models.FloatField(null=False, verbose_name='商品价格')
    spare = models.PositiveIntegerField(null=False, verbose_name='商品库存')
    xiaoliang = models.PositiveIntegerField(null=False, verbose_name='商品销量')

    def __str__(self):
        return self.name


class Sell(models.Model):
    st = (
        (False, '下架'),
        (True, '上架'),
    )

    seller = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, verbose_name='商品名称', null=False, unique=True)
    photo = models.TextField(verbose_name='商品图片')
    introduce = models.TextField(verbose_name='商品简介')
    price = models.FloatField(null=False, verbose_name='商品价格')
    spare = models.PositiveIntegerField(null=False, verbose_name='商品库存')
    state = models.BooleanField(verbose_name='商品状态', default='', choices=st)
    xiaoliang = models.PositiveIntegerField(null=False, verbose_name='商品销量')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ='商品'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    thing = models.ForeignKey('Sell', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='商品名称')
    tag = models.CharField(max_length=30, null=False, verbose_name='标签名称')

    class Meta:
        verbose_name ='标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Comment(models.Model):
    comment = models.TextField(null=False, verbose_name='评论内容')
    user = models.CharField(max_length=100, verbose_name='评论用户')
    answer = models.TextField(null=True, verbose_name='回复内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    thing = models.ForeignKey('Sell', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name ='评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment


