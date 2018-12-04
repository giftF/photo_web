from django.shortcuts import render
from django.http import HttpResponse
from photo import models
import time
import os
from django.db.models import Q
from PIL import Image
import hashlib
import uuid
from xpinyin import Pinyin

# 生成token或其他32位随机字符串
def create_md5():    #通过MD5的方式创建
    m=hashlib.md5()
    m.update(bytes(str(time.time()),encoding='utf-8'))
    return m.hexdigest()

# 密码加密
def md5_passwd(passwd):
    md = hashlib.md5()  # 构造一个md5
    md.update(passwd.encode())
    return md.hexdigest()  # 加密后的字符串

# 验证登录
def is_login(request):
    try:
        token = request.session['token']
    except:
        return render(request, 'mini/mini_login.html', {'text': '请登录!'})
    if models.mini_nuser.objects.filter(token=token):
        return token
    else:
        return render(request, 'mini/mini_login.html', {'text': 'token失效，请重新登录'})

# 后台登录页面
def mini_index(request):
    is_login(request)
    return render(request, 'mini/mini_index.html')

# 后台登录
def mini_login(request):
    try:
        user_name = request.POST['login']
        password = request.POST['password']
        md5_password = md5_passwd(password)
    except:
        return render(request, 'mini/mini_login.html', {'text': '账号货密码错误'})
    if models.mini_nuser.objects.values().filter(openid=user_name, passwd=md5_password):
        token = create_md5()
        models.mini_nuser.objects.filter(openid=user_name).update(token=token)
        request.session['token'] = token
        return render(request, 'mini/mini_index.html')
    else:
        return render(request, 'mini/mini_login.html', {'text': '账号货密码错误'})

# 查询接口
def mini_find(request):
    is_login(request)
    try:
        text = request.POST['search']
        t = ''
        for i in text:
            t += '%s|'%i
        text = t[:-1]
        lists = models.mini_poetry.objects.values('id', 'title', 'author').filter(
            Q(title__contains=text) | Q(body__contains=text) | Q(author__contains=text))
    except:
        lists = models.mini_poetry.objects.values('id', 'title', 'author').all()
    return render(request, 'mini/mini_index.html', {'bodys': lists})

# 跳转新增页面
def mini_add_page(request):
    is_login(request)
    return render(request, 'mini/mini_add.html')

# 新增
def mini_add(request):
    token = is_login(request)
    if type(token) != str:
        return token
    title = request.POST['title']
    author = request.POST['author']
    body = request.POST['body']
    dubbing = request.FILES.get("dubbing", None)
    dubbing_user = request.POST['dubbing_user']
    dubbing_1 = request.FILES.get("dubbing_1", None)
    dubbing_2 = request.FILES.get("dubbing_2", None)
    if dubbing:
        url = '/photo/static/tapes/' + str(time.time()).split('.')[0] + dubbing.name
        destination = open(os.path.join("./photo/static/tapes", str(time.time()).split('.')[0] + dubbing.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in dubbing.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        dubbing = url
    if dubbing_1:
        url = '/photo/static/tapes/' + str(time.time()).split('.')[0] + dubbing_1.name
        destination = open(os.path.join("./photo/static/tapes", str(time.time()).split('.')[0] + dubbing_1.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in dubbing_1.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        dubbing_1 = url
    if dubbing_2:
        url = '/photo/static/tapes/' + str(time.time()).split('.')[0] + dubbing_2.name
        destination = open(os.path.join("./photo/static/tapes", str(time.time()).split('.')[0] + dubbing_2.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in dubbing_2.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        dubbing_2 = url
    if request.POST['id'] == '':
        edit = models.mini_nuser.objects.values('id').filter(token=token)[0]['id']
        p = Pinyin()
        title_py = p.get_pinyin(title, '|', tone_marks='marks') + '\n'
        for i in title:
            title_py += '%s|'%i
        title = title_py[:-1]
        author_py = p.get_pinyin(author, '|', tone_marks='marks') + '\n'
        for i in author:
            author_py += '%s|'%i
        author = author_py[:-1]
        body_list = body.split('\r\n')
        bodys = ''
        for i in body_list:
            body_py = p.get_pinyin(i, '|', tone_marks='marks') + '\n'
            for j in i:
                body_py += '%s|'%j
            bodys += '%s\n'%body_py[:-1]
        body = bodys[:-1]
        try:
            models.mini_poetry.objects.create(title=title, author=author, body=body, dubbing=dubbing, dubbing_user=dubbing_user, dubbing_1=dubbing_1, dubbing_2=dubbing_2, edit=edit, created_time=str(time.time()).split('.')[0])
        except:
            return render(request, 'mini/mini_add.html', {'text': '新增失败'})
    elif dubbing is not None:
        models.mini_poetry.objects.filter(id=request.POST['id']).update(title=title, author=author, body=body, dubbing=dubbing, dubbing_user=dubbing_user)
    else:
        models.mini_poetry.objects.filter(id=request.POST['id']).update(title=title, author=author, body=body)
    return mini_find(request)

# 跳转编辑页面
def mini_edit_page(request):
    is_login(request)
    text = models.mini_poetry.objects.values().filter(id=request.GET['id'])[0]
    return render(request, 'mini/mini_add.html', {'text': text})

# 删除
def mini_delete(request):
    is_login(request)
    models.mini_poetry.objects.filter(id=request.GET['id']).delete()
    return mini_find(request)