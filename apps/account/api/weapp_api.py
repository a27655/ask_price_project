# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.mail_utils import send_activate_email, SendMailToResetPwd
from apps.account.serializers.weapp_serializers import SellerUserLoginSerializer, SellerUserRegisterSerializer, \
    UserResetPasswordSendMailSerializer, UserActiveSendMailSerializer


class WeappSellerLoginToken(APIView):
    permission_classes = ()
    serializer_class = SellerUserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        微信小程序销售登录

        ---
        serializer: SellerUserLoginSerializer
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data = {'is_active': False, 'token': {}}
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            data = {'is_active': True, 'token': token.key}
        return Response(data=data, status=status.HTTP_200_OK)


class WeappSellerRegister(APIView):
    permission_classes = ()
    serializer_class = SellerUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        微信小程序注册

        ---
        serializer: SellerUserRegisterSerializer
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_activate_email(request, user.email, user.activate_code)
        token, created = Token.objects.get_or_create(user=user)
        return Response(status=status.HTTP_201_CREATED)


class UserResetPasswordAPI(APIView):
    permission_classes = ()
    serializer_class = UserResetPasswordSendMailSerializer

    def post(self, request, *args, **kwargs):
        """
        重置密码，发送邮件方式

        ---
        serializer: UserResetPasswordSendMailSerializer
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        SendMailToResetPwd().reset_pwd(user, request=request)
        return Response(status=status.HTTP_200_OK)


class UserSendActiveEmail(APIView):
    permission_classes = ()
    serializer_class = UserActiveSendMailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        send_activate_email(request, user.email, user.activate_code)
        return Response(status=status.HTTP_200_OK)