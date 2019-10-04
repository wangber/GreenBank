from django.db import models


#创建用户投入历史记录表
class History(models.Model):
    user_id = models.CharField(max_length=100,unique=True,verbose_name="用户id")
    count = models.IntegerField(verbose_name="投入量")
    date = models.DateTimeField(verbose_name="投入日期",auto_now_add=True)
    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name="用户投入历史记录表"
        verbose_name_plural="用户投入历史记录表"

#创建一个用户模型
class MyUser(models.Model):
    
    open_id = models.CharField(max_length=100,unique=True,verbose_name="用户id")
    nickname = models.CharField(max_length=30,verbose_name="用户昵称",default="未知昵称")
    location = models.CharField(max_length=30,default="宿舍信息尚未填写",verbose_name="宿舍楼栋与宿舍号")
    all_touru = models.IntegerField(verbose_name='所有投入',default=0)
    level = models.CharField(max_length=20,verbose_name="环保等级",default="热心环保")
    history = models.ForeignKey(History,related_name="user_touru",on_delete=models.CASCADE)
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

# Create your models here.
