from django.db import models

# Create your models here.

# 登录记录表
class time_limits(models.Model):
    ip = models.CharField(max_length=20,null=False)
    update_time = models.BigIntegerField()
    channel = models.IntegerField()

# 答案记录表
class answers(models.Model):
    answer = models.CharField(max_length=20,null=False)
    channel = models.IntegerField()

# 相册目录表
class catalog(models.Model):
    title = models.CharField(max_length=10,null=False)
    photo_url = models.ImageField(upload_to='static/images', max_length=255)
    channel = models.IntegerField()
    is_show = models.IntegerField()

# 照片表
class photos(models.Model):
    title = models.CharField(max_length=50,null=False)
    text = models.CharField(max_length=50,null=True)
    photo_url = models.ImageField(upload_to='static/images', max_length=255)
    mini_url = models.CharField(max_length=255,null=True)
    catalog_id = models.IntegerField(null=False, default=1)
    is_show = models.IntegerField()

# 渠道表
class channel(models.Model):
    name = models.CharField(max_length=10,null=False)
    channel = models.IntegerField()
    is_show = models.IntegerField()