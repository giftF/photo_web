from django.shortcuts import render
from django.http import HttpResponse
from photo import models
import time
import os
from django.db.models import Q
from PIL import Image


# 用于判断浏览用户ip是否有效
def validate_ip(request):
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
    now = str(time.time()).split('.')[0]
    update_time = models.time_limits.objects.values().filter(~Q(channel='9999'), ip="%s"%ip)
    if not len(update_time):
        return False
    elif int(now) - int(update_time[0]['update_time']) > 300:
        return False
    else:
        models.time_limits.objects.filter(ip='%s'%ip).update(update_time='%s'%now)
        return True


# Create your views here.
# 进入首页
def hello(request):
    if not validate_ip(request):
        return render(request, 'login.html')
    photo_catalog = models.catalog.objects.values().filter(is_show=1)
    return render(request, 'show_catalog.html', {'photo_catalog': photo_catalog})

# 查看用户验证口令
def validate(request):
    t = str(time.time()).split('.')[0]
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
    try:
        the_answer = request.POST['answer']
    except:
        if not validate_ip(request):
            return render(request, 'login.html', {'text': '口令过期'})
        photo_catalog = models.catalog.objects.values().filter(is_show=1)
        return render(request, 'show_catalog.html', {'photo_catalog': photo_catalog})
    isanswer = models.answers.objects.values().filter(answer="%s"%the_answer)
    if len(isanswer):
        channel = isanswer[0]['channel']
        if not models.time_limits.objects.filter(ip='%s'%ip).update(update_time='%s'%t,channel='%s'%channel):
            models.time_limits.objects.create(ip='%s'%ip,update_time='%s'%t,channel='%s'%channel)
        photo_catalog = models.catalog.objects.values().filter(is_show=1)
        return render(request, 'show_catalog.html', {'photo_catalog': photo_catalog})
    return render(request, 'login.html', {'text':'口令错误!'})

# 查看照片
def show_photo(request):
    if not validate_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    catalog_id = request.GET['catalog_id']
    photos = models.photos.objects.values().filter(catalog_id=catalog_id,is_show=1)
    return render(request, 'show_photo.html', {'photos':photos})

# 用户判断编辑用户ip是否有效
def validate_root_ip(request):
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
    now = str(time.time()).split('.')[0]
    update_time = models.time_limits.objects.values().filter(channel='9999', ip="%s"%ip)
    if not len(update_time):
        return False
    elif int(now) - int(update_time[0]['update_time']) > 300:
        return False
    else:
        models.time_limits.objects.filter(ip='%s'%ip).update(update_time='%s'%now)
        return True

# 编辑用户验证口令
def add_validate(request):
    if validate_root_ip(request):
        photo_catalog = models.catalog.objects.values().filter(is_show=1)
        return render(request, 'edit_catalog.html', {'photo_catalog': photo_catalog})
    t = str(time.time()).split('.')[0]
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
    try:
        the_answer = request.POST['answer']
    except:
        return render(request, 'add_catalog_validate.html')
    txt = open('answer.csv','r')
    answer = txt.read()
    answer = answer.replace('\n', '').replace('\t', '')
    if the_answer == answer:
        if not models.time_limits.objects.filter(ip='%s' % ip).update(update_time='%s' % t, channel='9999'):
            models.time_limits.objects.create(ip='%s' % ip, update_time='%s' % t, channel='9999')
        photo_catalog = models.catalog.objects.values().filter(is_show=1)
        return render(request, 'edit_catalog.html', {'photo_catalog':photo_catalog})
    return render(request, 'add_catalog_validate.html', {'text': '口令错误!'})

# 跳转创建相册页面
def found(request):
    if not validate_root_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    return render(request, 'add_catalog.html')

# 创建相册
def found_result(request):
    if not validate_root_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    try:
        title = request.POST['title']
        channel = request.POST['channel']
        photo = request.FILES['img']
        HS = request.POST['HS']
    except:
        photo_catalog = models.catalog.objects.values().filter(is_show=1)
        return render(request, 'edit_catalog.html', {'photo_catalog': photo_catalog})
    print(str(photo).split('.')[1].upper())
    if str(photo).split('.')[1].upper() not in ['JPG','JPEG','PNG']:
        return render(request, 'add_catalog.html', {'text':'只能上传jpg\jpeg\png格式的图片'})
    l = str(photo).split('.')
    l_url = l[0] + str(time.time()).split('.')[0] +  '.' + l[1]
    photo = Image.open(photo)
    if HS == '2':
        photo = photo.rotate(270)
    photo.save('./photo/static/images/%s'%l_url)
    if models.catalog.objects.create(title=title,photo_url=l_url,channel=channel,is_show=1):
        photo_catalog = models.catalog.objects.values().filter(is_show=1)
        return render(request, 'edit_catalog.html', {'photo_catalog': photo_catalog})
    return render(request, 'add_catalog.html', {'text':'创建失败'})

# 删除相册
def delete_catalog(request):
    if not validate_root_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    catalog_id = request.GET['catalog_id']
    models.catalog.objects.filter(id=catalog_id).update(is_show=0)
    photo_catalog = models.catalog.objects.values().filter(is_show=1)
    return render(request, 'edit_catalog.html', {'photo_catalog': photo_catalog})

# 跳转编辑相册页面
def to_edit_catalog(request):
    if not validate_root_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    catalog_id = request.GET['catalog_id']
    photo_list = models.photos.objects.values().filter(is_show=1,catalog_id=catalog_id)
    return render(request, 'edit_photo.html', {'photos': photo_list,'catalog_id':catalog_id})

# 跳转添加照片页面
def to_add_photo(request):
    if not validate_root_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    try:
        catalog_id = request.GET['catalog_id']
    except:
        photo_catalog = models.catalog.objects.values().filter(is_show=1)
        return render(request, 'edit_catalog.html', {'photo_catalog': photo_catalog})
    return render(request, 'add_photo.html',{'catalog_id':catalog_id})

# 添加照片
def add_photo(request):
    if not validate_root_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    try:
        title = request.POST['title']
        text = request.POST['the_text']
        catalog_id = request.POST['catalog_id']
        photo = request.FILES['img']
        HS = request.POST['HS']
    except:
        photo_catalog = models.catalog.objects.values().filter(is_show=1)
        return render(request, 'edit_catalog.html', {'photo_catalog': photo_catalog})
    if str(photo).split('.')[1].upper() not in ['JPG','JPEG','PNG']:
        return render(request, 'add_photo.html', {'catalog_id': catalog_id, 'text':'只能上传jpg\jpeg\png格式的图片'})
    l = str(photo).split('.')
    l_url = l[0] + str(time.time()).split('.')[0] + '.' + l[1]
    photo = Image.open(photo)
    if HS == '2':
        photo = photo.rotate(270)
    photo.save('./photo/static/images/%s' % l_url)

    image = Image.open('./photo/static/images/%s' % l_url)
    image = image.resize((35, 35), Image.ANTIALIAS)
    name = str(photo).split('.')[0]
    n = '35%s'%l_url
    image.save('./photo/static/images/%s' % n, 'JPEG', quality=90)
    if models.photos.objects.create(title=title,catalog_id=catalog_id,is_show=1,photo_url=l_url,mini_url=n,text=text):
        photo_list = models.photos.objects.values().filter(is_show=1, catalog_id=catalog_id)
        return render(request, 'edit_photo.html', {'photos': photo_list, 'catalog_id': catalog_id})
    return render(request, 'add_photo.html', {'catalog_id': catalog_id})

# 删除照片
def delete_photo(request):
    if not validate_root_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    id = request.GET['id']
    catalog_id = request.GET['catalog_id']
    models.photos.objects.filter(id=id).update(is_show=0)
    photo_list = models.photos.objects.values().filter(is_show=1, catalog_id=catalog_id)
    return render(request, 'edit_photo.html', {'photos': photo_list, 'catalog_id': catalog_id})

# 返回目录
def return_catalog(request):
    if not validate_ip(request):
        return render(request, 'login.html', {'text':'口令过期'})
    photo_catalog = models.catalog.objects.values().filter(is_show=1)
    return render(request, 'show_catalog.html', {'photo_catalog': photo_catalog})

# 游客注销
def logout(request):
    if not validate_ip(request):
        return render(request, 'login.html')
    try:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    except:
        ip = request.META['REMOTE_ADDR']
    models.time_limits.objects.filter(ip=ip).update(update_time=0)
    return render(request, 'login.html')

