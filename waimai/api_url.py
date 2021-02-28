from django.urls import path
from waimai import api

urlpatterns = [
# 用户管理
    # 登录
    path('yonghu-login/',api.yonghu_login),
    # 注册
    path('yonghu-register/',api.yonghu_register)
]