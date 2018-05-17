# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _


class SetPasswordForm(forms.Form):
    """
    重置密码form
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            if ' ' in password1:
                raise forms.ValidationError(
                    '密码不能包含空格，请重新填写',
                    code='password_mismatch',
                )
            if len(password1) < 6:
                raise forms.ValidationError(
                    '密码不能小于六位，请重新填写',
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user