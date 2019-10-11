from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from index.duanju_get import juzi_api
from .models import Yuyue,MyUser,History,Token
from rest_framework.views import APIView
from django.http import JsonResponse
from apitest.utils.auth import Authentication 
from apitest.utils.permission import Mypermission

##这是index应用中的接口文件
class MyUserjson(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['open_id','nickname','location','all_touru','level',]
#测试接口
@api_view(['GET'])
def indexData(request):
     print('OK')
     return Response('OK')

@api_view(['GET'])
def get_onejuzi(request):
     try:            
          order = int(request.GET.get('type_order',1))
          print(order)
     except:
          sen = '抱歉这个句子貌似失踪了1'

     try:
          if order>=1 and order <=4:
               print('请求中...')
               sen = juzi_api(order)
          else:
               sen = '抱歉这个句子貌似失踪了2'
     except Exception as e:
          sen = '抱歉这个句子貌似失踪了error：3'+str(e)
     return Response(sen)

#接收预约的接口
@api_view(['POST'])
def yuyue(request):
     try:
          location_yuyue = request.POST.get('location')
          print(location_yuyue)
          Yuyue.objects.update_or_create(location=location_yuyue)
          return Response("预约成功")
     except Exception as e:
          print(e)
          return Response("预约失败")
     
#用户登录时更新数据库
@api_view(['POST'])
def login_up(request):
     try:
          #先为用户创建一个投入量为0的历史
          open_id = request.POST.get("user_openid")
          nickname = request.POST.get("user_nickname")
          print(open_id)
          print(nickname)
          History.objects.update_or_create(user_id=open_id,defaults={"count":0})
          MyUser.objects.update_or_create(open_id=open_id,defaults={"nickname":nickname})
          return Response("用户信息写入了数据库")
     except Exception as e:
          print(e)
          return Response("写入失败")

#认证
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
#生成二维码的函数
def to_code(token,num):
     from MyQR import myqr
     import base64
     words = str(token)+str(num)
     words = "['"+str(token)+"','"+str(num)+"']" #构造可转化字符串
     dir_name = "D:\\webcre\\Tryrtry\\VueDjango\\index\\QR-code\\"
     name = "myqr.png"
     version, level, qr_name = myqr.run(
                                        words,
                                        version=1,
                                        level="H",
                                        colorized=True,
                                        contrast=1.0,
                                        brightness=1.0,
                                        save_name= name,
                                        save_dir = dir_name
     )
     f = open(dir_name+name,"rb")
     base64_data = base64.b64encode(f.read())
     # print("图片是base64编码：")
     # print((str(base64_data))[1:])
     return (str(base64_data))[2:-1]
     
#一个生成二维码的视图
CODE = {"code":"这是一个二维码"}
 #用于生成二维码的视图
class CreateCode(APIView):
    #只有管理员可以使用该视图
    permission_classes = [Mypermission,]
    authentication_classes = [Authentication,]
    def get(self,request,*args,**kwargs):
        # request.user
        # request.auth
        token = request._request.GET.get("token")
        num = 50 #前端获取
        qr = to_code(token,num)
        ret = {'code':1000,'msg':None}
        try:
            ret['user'] = MyUserjson(request.user).data 
            ret['auth'] = str(request.auth)
            ret['QR'] = qr
        except Exception as e:
             print(e)
             pass
        return JsonResponse(ret)    
     
#后端接收用户的扫码后发出的请求
class Readcode(APIView):
     authentication_classes = [Authentication,]
     #从请求中获取二维码生成者的token和投入数量
     def post(self,request,*args,**kwargs):
          pass
     
