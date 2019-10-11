#权限控制
from rest_framework.permissions import BasePermission
#志愿者权限
class Mypermission(BasePermission):
    message = "这个功能需要是志愿者才能使用哦"
    def has_permission(self,request,view):
        if request.user.user_type !=2:
            return False
        return True
