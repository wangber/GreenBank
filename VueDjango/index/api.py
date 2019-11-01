from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from index.duanju_get import juzi_api
from .models import Yuyue,MyUser,History,Token
from rest_framework.views import APIView
from django.http import JsonResponse
from apitest.utils.auth import Authentication,Authentication_vo
from apitest.utils.permission import Mypermission

##这是index应用中的接口文件
class MyUserjson(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['open_id','nickname','location','all_touru','level','user_img',]

class Yuyuejson(serializers.ModelSerializer):
     class Meta:
          model = Yuyue
          fields = ['location','yuyuetime',]


def md5(user):
    import time
    import hashlib
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()

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
          user_img = request.POST.get("user_img")
          print(open_id)
          print(nickname)
          print(user_img)
          MyUser.objects.update_or_create(open_id=open_id,defaults={"nickname":nickname,"user_img":user_img})
          return Response("用户信息写入了数据库")
     except Exception as e:
          print(e)
          return Response("写入失败")

#认证
class AuthView(APIView):
    def post(self,request,*args,**kwargs):
        ret = {"code":1000,"msg":"认证完成"}
        try:
            user = request._request.POST.get("open_id")
            print("用户的open_id："+user)
            obj = MyUser.objects.filter(open_id=user).first()
            if not obj:
                ret["code"] = 1001
                ret["msg"] = "用户不存在"
            #为登录用户创建token
            token = md5(user)
            Token.objects.update_or_create(open_id=user,defaults={"token":token})
            ret['token'] = token
            #从数据库中获取用户返回用户类型
            ret['user_type'] = obj.user_type
            ret['all_touru'] = obj.all_touru
            ret['level'] = obj.level

        except Exception as e:
            print(e)
            ret['code'] = 1002
            ret['msg'] = "请求异常"
        return JsonResponse(ret)
#生成二维码的函数
def to_code(name,token,num):
     from MyQR import myqr
     import base64
     words = str(token)+str(num)
     words = "['"+str(token)+"','"+str(num)+"']" #构造可转化字符串
     dir_name = "D:\\webcre\\Tryrtry\\VueDjango\\index\\QR-code\\"
     name = name+".jpg"
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
        name = request.user.open_id
        token = request._request.GET.get("token")
        num = request._request.GET.get("num")
        if num =='' or num==0:
             return Response("数量输入有误")
     
        qr = to_code(name,token,num)
        ret = {'code':1000,'msg':"二维码获取动作完成"}
        try:
            ret['user'] = MyUserjson(request.user).data 
            ret['auth'] = str(request.auth) 
            ret['QR'] = qr
        except Exception as e:
             print(e)
             pass
        return JsonResponse(ret)    
from ast import literal_eval    
#后端接收用户的扫码后发出的请求
class Readcode(APIView):
     # authentication_classes = [Authentication,]
     #从请求中获取二维码生成者的token和投入数量
     def post(self,request,*args,**kwargs):
          info = request._request.POST.get("info")
          token = request._request.POST.get("token")
          #找扫码的人
          scaner_token_obj = Token.objects.get(token=token)
          scaner = MyUser.objects.filter(open_id = scaner_token_obj.open_id).first()
          print(token)
          print(info)
          info_list=literal_eval(info)
          cre_token = info_list[0]
          num = info_list[1]
          #查看该二维码是否有效
          
          try:
               cre_token_obj = Token.objects.get(token=cre_token) #找创建二维码的人
               codecreaster = MyUser.objects.filter(open_id = cre_token_obj.open_id).first()
               if (codecreaster.user_type ==2 ):
                    print("二维码有效")
                    #投入数量写入数据库
                    scaner.all_touru = scaner.all_touru+int(num)
                    #创建一个投入历史并写入
                    temp_his = History()
                    temp_his.user_id = scaner.open_id
                    temp_his.count = num
                    temp_his.save()
                    scaner.save()
                    print("数据已经写入")
                    return JsonResponse({
                         "info":True,
                         'num':num
                    })
               else:
                    return Response("二维码无效，重试一下吧")
          except Exception as e:
               print(e)
               return Response("出错了-_-")
     

#排行榜获取
class Paihang(APIView):
     def get(self,request,*args,**kwargs):
          #从数据库中读取投入量前50的用户
          ret = {}
          ret_user = {}
          alluser = MyUser.objects.all().order_by('-all_touru')[:50]
          print(type(alluser))
          j=0
          for i in alluser:
               ret_user[j] = MyUserjson(i).data
               j=j+1
          #找出最新的更新时间
          ret['alluser'] = ret_user
          new_time = History.objects.last()
          ret["time"] = str(new_time.date).split(" ")[0]
          return JsonResponse(ret)
#查看预约
import datetime
class Seeyuyue(APIView):
     def get(self,request,*args,**kwargs):
          ret = {}
          new = Yuyue.objects.last()
          last_time = new.yuyuetime
          old_time =  last_time-datetime.timedelta(days=15)
          print(old_time)
          print(last_time)
          ret_list = {}
          yuyue_result = Yuyue.objects.filter(yuyuetime__range = (old_time,last_time))
          for i in range(len(yuyue_result)):
               ret_list[i] = Yuyuejson(yuyue_result[i]).data
               ret_list[i]['yuyuetime'] = Yuyuejson(yuyue_result[i]).data['yuyuetime'].split('T')[0]
          ret["ret_list"] = ret_list
          ret["last_time"] = last_time.strftime('%Y-%m-%d')
          ret["old_time"] = old_time.strftime('%Y-%m-%d')
          return Response(ret)
  
     
