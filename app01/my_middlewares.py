from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
from back.models import Users
from back.models import Permission
from back.models import Menu
from back.models import Role
from blog1 import settings


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.session.get('user_id'):
            # 判读当前登录用户，是否拥有访问此路径的权限
            user_id = request.session.get("user_id")#得到管理员id
            user_obj = Users.objects.filter(user_id=user_id).first()
            role_list = user_obj.role_set.all()# 用户所属的角色
            # role_list = user_obj# 用户所属的角色
            # role_objs = models.Role.objects.filter(userinfo=user_id).all()
            # 例如http://127.0.0.1:8000/back/index/index/ 这个不是菜单，应该放行
            permission_obj = Permission.objects.filter(permission_path=request.path).first()  # 当前访问的权限id

            if permission_obj:
                permission_list = []
                for role in role_list:
                    permission_list.extend(role.role_access.split(","))

                if str(permission_obj.permission_name) not in permission_list:
                    return HttpResponse("您无权限 请联系管理员开通")
                else:
                    return None






