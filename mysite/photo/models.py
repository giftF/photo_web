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
    photo_url = models.CharField(max_length=255,null=True)
    channel = models.IntegerField()
    is_show = models.IntegerField()

# 照片表
class photos(models.Model):
    title = models.CharField(max_length=50,null=False)
    text = models.CharField(max_length=50,null=True)
    photo_url = models.CharField(max_length=255,null=True)
    mini_url = models.CharField(max_length=255,null=True)
    catalog_id = models.IntegerField(null=False, default=1)
    is_show = models.IntegerField()

# 渠道表
class channel(models.Model):
    name = models.CharField(max_length=10, null=False)
    channel = models.IntegerField()
    is_show = models.IntegerField()

# 小程序数据库
# 用户表
class mini_nuser(models.Model):
    # user_id = models.AutoField()  # 用户id
    openid = models.CharField(max_length=30, null=False)  # 微信唯一标识 管理员openid为登录后台的user_name
    gender = models.IntegerField(null=True)  # 性别 男：1   女：2   未知：0
    city = models.CharField(max_length=20, null=True)  # 城市
    model = models.CharField(max_length=30, null=True)  # 手机型号
    type = models.IntegerField(null=True)  # 用户类型 普通用户：1  管理员：0
    passwd = models.CharField(max_length=32)  # 密码，普通用户为空，用作管理员登录后台
    token = models.CharField(max_length=32, null=True)  # 管理员使用

# 诗词表
class mini_poetry(models.Model):
    # id = models.AutoField()  # 文章id
    title = models.TextField(null=False)  # 诗词标题
    author = models.TextField(null=False)  # 作者
    body = models.TextField(null=False)  # 正文
    dubbing = models.CharField(max_length=50, null=True)  # 朗读配音1
    dubbing_user = models.CharField(max_length=30, null=True)  # 提供人
    dubbing_1 = models.CharField(max_length=50, null=True)  # 朗读配音2
    dubbing_2 = models.CharField(max_length=50, null=True)  # 朗读配音3
    edit = models.IntegerField()  # 上传人员id
    created_time = models.CharField(max_length=20, null=False)  # 创建时间，字符串形式存放时间戳

# 阅读历史
class mini_history(models.Model):
    # id = models.AutoField()  # 阅读记录id
    user_id = models.IntegerField()  # 用户id
    poetry_id = models.IntegerField()  # 诗词id
















































