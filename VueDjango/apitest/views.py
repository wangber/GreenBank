from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework import serializers,exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from index.models import MyUser,History,Token
from rest_framework.authentication import BasicAuthentication
from .utils.auth import Authentication
from .utils.permission import Mypermission

class MyUserjson(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['open_id','nickname','location','all_touru','level',]
def md5(user):
    import time
    import hashlib
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()

#在这里编写一些接口
#认证接口
class AuthView(APIView):
    def post(self,request,*args,**kwargs):
        ret = {"code":1000,"msg":None}
        try:
            user = request._request.POST.get("open_id")
            print("用户的open_id："+user)
            obj = MyUser.objects.filter(open_id=user).first()
            print(obj)
            if not obj:
                ret["code"] = 1001
                ret["msg"] = "用户不存在"
            #为登录用户创建token
            token = md5(user)
            Token.objects.update_or_create(open_id=user,defaults={"token":token})
            
            ret['token'] = token
        except Exception as e:
            print(e)
            ret['code'] = 1002
            ret['msg'] = "请求异常"
        return JsonResponse(ret)

CODE = {"code":"这是一个二维码"}
class CreateCode(APIView):

    #只有管理员可以使用该视图
    permission_classes = [Mypermission,]
    #用于生成二维码的视图
    authentication_classes = [Authentication,]
    def get(self,request,*args,**kwargs):
        # request.user
        # request.auth
        ret = {'code':1000,'msg':None,'data':None}
        try:
            ret['data'] = CODE
            ret['user'] = MyUserjson(request.user).data 
            ret['auth'] = str(request.auth)
        except Exception as e:
            pass
        return JsonResponse(ret)    

     
#获取用户的信息

# Create your views here.
