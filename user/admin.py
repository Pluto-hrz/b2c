from . import models as us
from django.contrib import admin


class CharacterFilter(admin.SimpleListFilter):
    title = "用户身份"
    parameter_name = "character"

    def lookups(self, request, model_admin):
        return (
            ("buy", "买家"),
            ("sell", "商家"),
        )

    def queryset(self, request, queryset):
        if self.value() == "buy":
            return queryset.filter(character=0)
        elif self.value() == "sell":
            return queryset.filter(character=1)


class StateFilter(admin.SimpleListFilter):
    title = "商品状态"
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return (
            ("up", "上架"),
            ("down", "下架"),
        )

    def queryset(self, request, queryset):
        if self.value() == "up":
            return queryset.filter(state=1)
        elif self.value() == "down":
            return queryset.filter(state=0)


class OrderFilter(admin.SimpleListFilter):
    title = "订单状态"
    parameter_name = "state"

    def lookups(self, request, model_admin):
        return (
            ("1", "订单待处理"),
            ("2", "交易成功"),
            ("3", "交易失败"),
        )

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(state="订单待处理")
        elif self.value() == "2":
            return queryset.filter(state="交易成功")
        elif self.value() == "3":
            return queryset.filter(state="交易失败")


class AdminLogin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ['username', '用户状态', 'character', 'create_time']
    # 搜索框，按照元组内指定字段搜索
    search_fields = ('username', )
    # 按时间过滤
    date_hierarchy = 'create_time'
    # 定义动作列表
    actions = ["publish_status", "withdraw_status"]
    # 每页显示多少条
    list_per_page = 20
    # 过滤器
    list_filter = (CharacterFilter,)

    # 禁止登陆动作函数 参数固定
    def publish_status(self, request, queryset):
        queryset.update(is_active=False)
    # 指定动作显示名称
    publish_status.short_description = '冻结用户'

    def withdraw_status(self, request, queryset):
        queryset.update(is_active=True)
    withdraw_status.short_description = '解除冻结'


class MyTags(admin.ModelAdmin):
    list_display = ['tag', 'thing']
    search_fields = ('tag', )
    list_filter = ['thing', 'tag']


class Things(admin.ModelAdmin):
    list_display = ['name', 'price', 'spare', 'xiaoliang', 'state', 'create_time']
    search_fields = ('name', )
    date_hierarchy = 'create_time'
    actions = ["publish_status", "withdraw_status"]
    list_filter = (StateFilter,)

    def publish_status(self, request, queryset):
        queryset.update(state=False)
    publish_status.short_description = '下架商品'

    def withdraw_status(self, request, queryset):
        queryset.update(state=True)
    withdraw_status.short_description = '上架商品'


class Order(admin.ModelAdmin):
    list_display = ['thing_name', 'buyer_name', 'seller_name', 'state', 'all_price', 'create_time']
    search_fields = ('thing_name', )
    date_hierarchy = 'create_time'
    actions = ["publish_status", "withdraw_status"]
    list_filter = (OrderFilter,)

    def publish_status(self, request, queryset):
        queryset.update(state='交易成功')
    publish_status.short_description = '确认交易'

    def withdraw_status(self, request, queryset):
        queryset.update(state='交易失败')
    withdraw_status.short_description = '取消交易'


class Comment(admin.ModelAdmin):
    list_display = ['thing', 'comment', 'user', 'answer', 'create_time']
    search_fields = ('thing', )
    date_hierarchy = 'create_time'
    list_filter = ['thing']


# 注册   第一个参数为数据库模型， 第二为自己写的类
admin.site.register(us.User, AdminLogin)
admin.site.register(us.Tag, MyTags)
admin.site.register(us.Sell, Things)
admin.site.register(us.Order, Order)
admin.site.register(us.Comment, Comment)
