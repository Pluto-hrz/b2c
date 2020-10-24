from django.urls import path, include
from user.views import *

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register, name="register"),
    path('xie_yi/', xie_yi, name="xie_yi"),
    path('money/', money, name="money"),
    path('forget_password/', forget_password, name="forget_password"),
    path('correct_password/', correct_password, name="correct_password"),
    path('forget_correct_password/<int:user_id>/', forget_correct_password, name="forget_correct_password"),
    path('user_correct/', user_correct, name="user_correct"),
]