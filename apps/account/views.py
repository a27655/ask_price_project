# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.account.models import User
from apps.account.forms import SetPasswordForm


class UserActiveSuccessView(TemplateView):
    template_name = 'user_active_success.html'

    def get(self, request, *args, **kwargs):
        active_code = kwargs.get('code')
        try:
            user = User.objects.get(activate_code=active_code)
        except:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            user.is_active = True
            user.save()
            return render(request, self.template_name, locals())



# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)