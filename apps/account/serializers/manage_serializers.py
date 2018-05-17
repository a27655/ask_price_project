# -*- coding: utf-8 -*-
from rest_framework import serializers

from apps.account.models import User


class ManagerLoginSerializer(serializers.Serializer):
    """运维登录serializer"""
    username = serializers.CharField(label='用户名', help_text='用户名')
    password = serializers.CharField(label="密码", style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            try:
                user = User.objects.get(username=username, user_type=User.OPERATION_USER)
                valid = user.check_password(password)
                if not valid:
                    raise serializers.ValidationError('输入密码错误。')
            except User.DoesNotExist:
                raise serializers.ValidationError("用户尚未注册。")
            if user:
                if not user.is_active:
                    msg = '账号未激活，可联系相关管理人员'
                    raise serializers.ValidationError(msg)
                if not user.is_staff:
                    msg = '该账户已被禁用，可联系相关管理人员'
                    raise serializers.ValidationError(msg)
        else:
            msg = '请输入用户名和密码'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class UserManageListSerializer(serializers.HyperlinkedModelSerializer):
    staff_change_url = serializers.HyperlinkedIdentityField(label='更改职员状态接口', help_text='更改职员状态接口',
                                                            view_name='manager-users-staff-change')

    class Meta:
        model = User
        fields = ('id','email', 'is_staff', 'staff_change_url')