#-*- coding:utf8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label=_('E-Posta'), widget=forms.TextInput({'placeholder':_('E-Posta')}))
    password = forms.CharField(label=_('Sifre'), widget=forms.PasswordInput({'placeholder':_('Sifre')}))
    password2 = forms.CharField(label=_('Sifre (Tekrar)'), widget=forms.PasswordInput({'placeholder':_('Sifre (Tekrar)')}))

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError(_('Sifre alanlari birbirinin aynisi olmali.'))
        return self.cleaned_data

    def clean_email(self):
        users = User.objects.filter(email=self.cleaned_data['email'])
        if users.count():
            raise forms.ValidationError(_('Bu e-posta adresi zaten kullanilmakta.'))
        return self.cleaned_data['email']


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('Email'), widget=forms.TextInput({'placeholder':_('Email')}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput({'placeholder':_('Password')}))



class PasswordChangeForm(forms.Form):
    password = forms.CharField(label=_('Current Password'),
                widget=forms.PasswordInput({'placeholder':_('Current Password')}))
    new_password = forms.CharField(label=_('New Password'),
                    widget=forms.PasswordInput({'placeholder':_('New Password')}))
    new_password2 = forms.CharField(label=_('New Password (Again)'),
        widget=forms.PasswordInput({'placeholder':_('New Password (Again)')}))


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PasswordChangeForm, self).__init__(*args, **kwargs)


    def clean(self):
        if self.cleaned_data.get('new_password') != self.cleaned_data.get('new_password2'):
            raise forms.ValidationError(_('New password fields do not match.'))
        return self.cleaned_data


    def clean_password(self):
        user = User.objects.get(pk=self.request.user.id)
        if not user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError(_('Please enter your current password correctly.'))
        return self.cleaned_data['password']



class InfoChangeForm(forms.Form):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput({'placeholder':_('Name')}))
    surname = forms.CharField(label=_('Surname'), widget=forms.TextInput({'placeholder':_('Surname')}))
    email = forms.EmailField(label=_('E-Mail'), widget=forms.TextInput({'placeholder':_('E-Mail')}))
