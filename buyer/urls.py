from django.urls import path, include
from buyer.views import *

urlpatterns = [
    path('index_buyer/', index_buyer, name="index_buyer"),
    path('home/', home, name="home"),
    path('buy_car/', buy_car, name="buy_car"),
    path('thing/<int:thing_id>/', thing, name="thing"),
    path('comment_add', comment_add, name="comment_add"),
    path('comment_delete', comment_delete, name="comment_delete"),
    path('buy_car_add', buy_car_add, name="buy_car_add"),
    path('order_add/<int:thing_id>/<int:num>/', order_add, name="order_add"),
    path('buy_car_delete', buy_car_delete, name="buy_car_delete"),
    path('order_success/', order_success, name="order_success"),
]