# -*- coding: utf-8 -*-

from django.core import validators
from rest_framework import serializers

from apps.account.models import User


class SellerUserLoginSerializer(serializers.Serializer):
    """小程序用户登录serializer"""
    email = serializers.EmailField(label='邮箱', help_text='邮箱')
    password = serializers.CharField(label="密码", style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
                valid = user.check_password(password)
                if not valid:
                    raise serializers.ValidationError('输入密码错误。')
            except User.DoesNotExist:
                raise serializers.ValidationError("邮箱尚未注册。")
            if user:
                if not user.is_staff:
                    msg = '该账户已被禁用，可联系相关管理人员'
                    raise serializers.ValidationError(msg)
        else:
            msg = '请输入邮箱和密码'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class SellerUserRegisterSerializer(serializers.Serializer):
    """小程序用户注册serializer"""
    email = serializers.EmailField(label='邮箱', help_text='邮箱')
    password = serializers.CharField(label="密码", style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        if email and password:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError('此邮箱已经注册')
            # 验证密码不能为中文
            validator_instance = validators.RegexValidator(r'^[\w.@+-]+$', '密码只能为@.+-_,英文,数字', 'invalid')
            validator_instance(password)
        else:
            msg = '请输入邮箱和密码'
            raise serializers.ValidationError(msg)
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.seller_objects.create(email, password)
        return user


class UserResetPasswordSendMailSerializer(serializers.Serializer):
    """重置密码发送邮件serializer"""
    email = serializers.EmailField(label='邮箱', help_text='邮箱')

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('此邮箱尚未注册')
        else:
            if not user.is_active:
                raise serializers.ValidationError('此账户未激活')
        attrs['user'] = user
        return attrs


class UserActiveSendMailSerializer(serializers.Serializer):
    """账户激活发送邮件serializer"""
    email = serializers.EmailField(label='邮箱', help_text='邮箱')

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('此邮箱尚未注册')
        else:
            if user.is_active:
                raise serializers.ValidationError('此账户已激活，请前往登录')
        attrs['user'] = user
        return attrs