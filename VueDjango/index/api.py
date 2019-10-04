from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from index.duanju_get import juzi_api

##这是index应用中的接口文件


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



     
     