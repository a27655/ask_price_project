# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse



def send_activate_email(request, email, activate_code):
    """注册账户激活发送邮件"""
    # current_site = get_current_site(request)
    activate_url = reverse('user_activate', kwargs={'code':activate_code}, request=request)
    subject, form_email, to = '报价系统激活', 'a_handsome_man@163.com', email
    text_content = '报价系统新注册用户激活'
    html_content = '<html><body><h3>激活链接</h3><a href="%s" target="_blank">%s</a><br/><span>\
    若未跳转，将地址复制于浏览器地址栏</span></body></html>' % (activate_url, activate_url)
    msg = EmailMultiAlternatives(subject, text_content, form_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


class SendMailToResetPwd(object):
    """账户重置密码发送邮件"""
    def send_email(self, subject_template_name, email_template_name,
                   context, from_email, to_email, html_email_template_name=None):
            """
            Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
            """
            subject = loader.render_to_string(subject_template_name, context)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            body = loader.render_to_string(email_template_name, context)

            email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
            if html_email_template_name is not None:
                html_email = loader.render_to_string(html_email_template_name, context)
                email_message.attach_alternative(html_email, 'text/html')

            email_message.send()

    def reset_pwd(self, user, domain_override=None,
                  subject_template_name='registration/password_reset_subject.txt',
                  email_template_name='registration/password_reset_email.html',
                  use_https=False, token_generator=default_token_generator,
                  from_email=None, request=None, html_email_template_name=None):
            """
            Generates a one-use only link for resetting password and sends to the
            user.
            """
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            self.send_email(subject_template_name, email_template_name,
                            context, from_email, user.email,
                            html_email_template_name=html_email_template_name)