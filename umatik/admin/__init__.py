#-*- coding:utf-8 -*-

from django.contrib import admin
from django.db.models import Q
from umatik.models import *
from utils.admin import admin_register
from modmin import Modmin
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _


from application import *
from map import *
from active import *
from kafe import *
from base import *
from avm import *

@receiver(user_logged_in)
def login_settings(sender, **kwargs):
    r = kwargs['request']
    u = kwargs['user']
    r.session['uid'] = u.id

#    profile = u.profile
#    if profile:
#        profile = profile[0]
#        r.session['appid'] = profile.app_id
#        r.session['placeid'] = profile.place_id


user_logged_in.connect(login_settings)
admin_register(admin, namespace=globals())


class CustomUserAdmin(UserAdmin):
    """superuser olmayan kullanicinin kisiel bilgilerini degistirmesi"""

    def get_fieldsets(self, request, obj=None):
        """ kisisel bilgi ekraninda izinlere ait bilgilerin gosterilmemesi """
        if not request.user.is_superuser:
            self.fieldsets = (
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
            )
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def response_post_save_change(self, request, obj):
        """ superuser olmayan kullanici bilgilerini kaydettikten sonra gene ayni ekranda kalmasi """
        opts = self.model._meta
        if self.has_change_permission(request, None):
            if request.user.is_superuser:
                post_url = reverse('admin:%s_%s_changelist' %
                                   (opts.app_label, opts.module_name), current_app=self.admin_site.name)
            else:
                post_url = request.path
        else:
            post_url = reverse('admin:index',
                               current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
