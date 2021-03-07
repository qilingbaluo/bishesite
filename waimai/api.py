from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # django的分页器
from waimai.models import yonghuUser
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import requests
import datetime
import base64
import json


hostUrl = 'http://127.0.0.1:9000/'

# 登录


@api_view(['POST'])
def yonghu_login(request):
    username = request.POST['username']
    password = request.POST['password']
    shenfen = request.POST['shenfen']
# 登录逻辑
    user = User.objects.filter(username=username)
    shenfen = yonghuUser.objects.filter(shenfen=shenfen, belong=user[0])
    if user:
        if shenfen:
            checkPwd = check_password(password, user[0].password)
            if checkPwd:
                userinfo = yonghuUser.objects.get_or_create(belong=user[0])
                userinfo = yonghuUser.objects.get(belong=user[0])
                token = Token.objects.get_or_create(user=user[0])
                token = Token.objects.get(user=user[0])
            else:
                return Response('pwderr')
    else:
        return Response('none')

    userinfo_data = {
        'token': token.key,
        'shenfen': userinfo.shenfen,
        'useradress': userinfo.useradress
    }
    return Response(userinfo_data)

# 注册


@api_view(['POST'])
def yonghu_register(request):
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    useradress = request.POST['useradress']
# 注册逻辑
    user = User.objects.filter(username=username)
    if user:
        return Response('repeat')
    else:
        new_password = make_password(password, username)
        newUser = User(username=username, password=new_password)
        newUser.save()

    token = Token.objects.get_or_create(user=newUser)
    token = Token.objects.get(user=newUser)
    userinfo = yonghuUser.objects.get_or_create(
        belong=newUser, useradress=useradress, shenfen='1')
    userinfo = yonghuUser.objects.get(
        belong=newUser, useradress=useradress, shenfen='1')

    userinfo_data = {
        'token': token.key,
        'shenfen': userinfo.shenfen,
        'useradress': userinfo.useradress
    }
    return Response(userinfo_data)

# 自动登录


@api_view(['POST'])
def yonghu_autologin(request):
    token = request.POST['token']
    user_token = Token.objects.get(key=token)
    if user_token:
        userinfo = yonghuUser.objects.get(belong=user_token.user)
        userinfo_data = {
            'token': token,
            'shenfen': userinfo.shenfen,
            'useradress': userinfo.useradress
        }
        return Response(userinfo_data)
    else:
        return Response('tokentimeout')

# 登出


@api_view(['POST'])
def yonghu_logout(request):
    token = request.POST['token']
    user_token = Token.objects.get(key=token)
    user_token.delete()
    return Response('logout')
