from django.urls import path, include
from seller.views import *

urlpatterns = [
    path('index_seller/', index_seller, name="index_seller"),
    path('things_manage/', things_manage, name="things_manage"),
    path('things_output/', things_output, name="things_output"),
    path('tags_add/<int:thing_id>/', tags_add, name="tags_add"),
    path('comment_answer/', comment_answer, name="comment_answer"),
    path('things_shangjia/', things_shangjia, name="things_shangjia"),
    path('things_xiajia/', things_xiajia, name="things_xiajia"),
    path('things_delete/', things_delete, name="things_delete"),
    path('things_correct/<int:thing_id>/', things_correct, name="things_correct"),
    path('order_request/', order_request, name="order_request"),
    path('order_unsuccess/', order_unsuccess, name="order_unsuccess"),

]