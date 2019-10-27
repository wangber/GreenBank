#基于token的认证
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from index.models import MyUser,History,Token
from rest_framework import serializers,exceptions
from rest_framework import serializers

class Authentication(BasicAuthentication):
    def authenticate(self,request):
        token = request._request.GET.get("token")
        token_obj = Token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        user = MyUser.objects.filter(open_id = token_obj.open_id).first()
        #在drf内部会将两个字段赋值给request，以供后续操作使用
        return (user,token_obj)
        #认证失败给浏览器返回的响应头
    def authenticate_header(self,request):
        pass

class Authentication_vo(BasicAuthentication):
    def authenticate(self,request):
        token = request._request.GET.get("token")
        token_obj = Token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        else:
            if token_obj.user_type !=2:
                raise exceptions.AuthenticationFailed("用户认证失败,权限不足")
                user = MyUser.objects.filter(open_id = token_obj.open_id).first()
        #在drf内部会将两个字段赋值给request，以供后续操作使用
        return (user,token_obj)
        
        #认证失败给浏览器返回的响应头
    def authenticate_header(self,request):
        pass
