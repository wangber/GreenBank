from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from index.models import MyUser,History

class MyUserjson(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['open_id','nickname','location','all_touru','level',]
#在这里编写一些接口
#获取用户的信息
@api_view(['GET'])
def get_user(request):
    all_user = MyUser.objects.all()
    return Response(all_user)

# Create your views here.
