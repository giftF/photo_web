from django.shortcuts import render
from django.http import HttpResponse
from photo import models
import time
import os
from django.db.models import Q
from PIL import Image
import hashlib
import uuid
import json
import random

'''
code = {
    1 : 缺少openid
}
'''

def damo(request):
    a = {'id': 1}
    x = models.mini_poetry.objects.values().filter(**a)
    resp = {'a': 1, 'b': 2}
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

# 验证用户信息
def the_openid(reqest):
    openid = reqest.META.get("HTTP_OPENID")
    if not openid:
        resp = {'text': '没有openid', 'code': 1}
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
    return openid

# 储存用户信息
def mini_setuser(request):
    re_openid = the_openid(request)
    if type(re_openid) != str:
        return re_openid
    kws = request.POST.copy()
    try:
        kws['gender'] = int(kws['gender'])
    except:
        kws['gender'] = 0
    sql_body = models.mini_nuser.objects.values().filter(openid=re_openid)
    if sql_body:
        models.mini_nuser.objects.create(**kws.dict())
        resp = {'text': '操作成功:修改', 'code': 200}
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
    else:
        kws['openid'] = re_openid
        models.mini_nuser.objects.create(**kws.dict())
    resp = {'text': '操作成功:新增', 'code': 200}
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

# 获取用户user_id
def get_userid(request):
    re_openid = the_openid(request)
    try:
        user_id = models.mini_nuser.objects.values('id').filter(openid=re_openid)[0]['id']
    except:
        user_id = models.mini_nuser.objects.create(openid=re_openid).id
    return user_id

# 随机查看文章
def mini_read(request):
    user_id = get_userid(request)
    try:
        prey = models.mini_history.objects.values('id').filter(user_id=user_id).order_by('-id')[0]['id']
    except:
        prey = 0
    last = models.mini_poetry.objects.count() - 1
    index = random.randint(0, last)
    texts = models.mini_poetry.objects.values().all()[index]
    models.mini_history.objects.create(user_id=user_id, poetry_id=texts['id'])
    resp = {'text': texts, 'prey': prey, 'next': 0, 'code': 1, 'msg': None}
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

# 搜索文章
def mini_search(request):
    user_id = get_userid(request)
    handle = request.POST['handle']
    # 按关键字搜索
    if handle == 'search':
        text = request.POST['search']
        t = ''
        for i in text:
            t += '%s|' % i
        search = t[:-1]
        try:
            prey = models.mini_history.objects.values('poetry_id').filter(user_id=user_id).order_by('-id')[0][
                'poetry_id']
        except:
            prey = 0
        last = models.mini_poetry.objects.filter(
            Q(title__contains=search) | Q(body__contains=search) | Q(author__contains=search)).count() - 1
        if last >= 0:
            index = random.randint(0, last)
            texts = models.mini_poetry.objects.values().filter(
                Q(title__contains=search) | Q(body__contains=search) | Q(author__contains=search))[index]
            models.mini_history.objects.create(user_id=user_id, poetry_id=texts['id'])
            resp = {'text': texts, 'prey': prey, 'code': 1, 'next': 0, 'msg': None}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
        else:
            try:
                prey = models.mini_history.objects.values('id').filter(user_id=user_id).order_by('-id')[0]['id']
            except:
                prey = 0
            last = models.mini_poetry.objects.count() - 1
            index = random.randint(0, last)
            texts = models.mini_poetry.objects.values().all()[index]
            models.mini_history.objects.create(user_id=user_id, poetry_id=texts['id'])
            resp = {'text': texts, 'prey': prey, 'code': 1, 'next': 0, 'msg': '没有匹配的内容'}
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
    # 查看上一首
    elif handle == 'prey':
        prey_old = request.POST['prey']
        try:
            prey = models.mini_history.objects.values('id').filter(Q(user_id=user_id) & Q(id__lt=prey_old)).order_by('-id')[0][
                'id']
        except:
            prey = 0
        try:
            next = models.mini_history.objects.values('id').filter(Q(user_id=user_id) & Q(id__gt=prey_old)).order_by('id')[0]['id']
        except:
            next = 0
        poetry_id = models.mini_history.objects.values('poetry_id').filter(id=prey_old)[0]['poetry_id']
        texts = models.mini_poetry.objects.values().filter(id=poetry_id)[0]
        resp = {'text': texts, 'prey': prey, 'next': next, 'code': 1, 'msg': None}
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
    # 查看下一首
    elif handle == 'next':
        next_old = request.POST['next']
        try:
            prey = models.mini_history.objects.values('id').filter(Q(user_id=user_id) & Q(id__lt=next_old)).order_by('-id')[0][
                'id']
        except:
            prey = 0
        try:
            next = models.mini_history.objects.values('id').filter(Q(user_id=user_id) & Q(id__gt=next_old)).order_by('id')[0]['id']
        except:
            next = 0
        poetry_id = models.mini_history.objects.values('poetry_id').filter(id=next_old)[0]['poetry_id']
        texts = models.mini_poetry.objects.values().filter(id=poetry_id)[0]
        resp = {'text': texts, 'prey': prey, 'next': next, 'code': 1, 'msg': None}
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
    # 随机查看
    else:
        return mini_read(request)