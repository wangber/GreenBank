from django.db import models


#创建用户投入历史记录表
class History(models.Model):
    user_id = models.CharField(max_length=100,verbose_name="用户id")
    count = models.IntegerField(verbose_name="投入量")
    date = models.DateTimeField(verbose_name="投入日期",auto_now_add=True)
    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name="用户投入历史记录表"
        verbose_name_plural="用户投入历史记录表"

#创建一个用户模型
class MyUser(models.Model):
    
    open_id = models.CharField(max_length=100,unique=True,verbose_name="用户open_id")
    nickname = models.CharField(max_length=30,verbose_name="用户昵称",default="未知昵称")
    location = models.CharField(max_length=30,default="宿舍信息尚未填写",verbose_name="宿舍楼栋与宿舍号")
    all_touru = models.IntegerField(verbose_name='所有投入',default=0)
    level = models.CharField(max_length=20,verbose_name="环保等级",default="热心环保")
    user_img = models.TextField(max_length=200,verbose_name="用户头像",default="https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2781007512,3931003336&fm=26&gp=0.jpg")
    user_type_choices =(
        (1,"普通用户"),
        (2,"志愿者"),
        (3,"管理员")
    )
    user_type = models.IntegerField(choices=user_type_choices,default=1)
    def __str__(self):
        return self.nickname
        pass

    class Meta:
        managed = True
        verbose_name =  "用户"
        verbose_name_plural =  "用户"

class Token(models.Model):
    open_id = models.CharField(max_length=100,unique=True,verbose_name="用户id")
    token = models.CharField(max_length=100,verbose_name="登录token") 


#预约表
class Yuyue(models.Model):
    location = models.CharField(max_length=30,verbose_name="预约地址")
    yuyuetime = models.DateTimeField(auto_now=True,verbose_name="预约时间")
    def __str__(self):
        return self.location
    class Meta:
        ordering = ['yuyuetime']
        verbose_name_plural = "预约情况"

# Create your models here.
