#-*- coding:utf-8 -*-
from django.contrib import admin
from django.http import Http404
from umatik.models import *
from admin_tabs.helpers import TabbedModelAdmin, TabbedPageConfig, Config


class TransConfig(TabbedPageConfig):
    class SuperFieldsConfig:
        super = Config(fields=["app"])

    class ColsConfig:
        details = Config(fieldsets=["details"])
        translations = Config(fieldsets=["translations"])
        super = Config(fieldsets=["super"])

    class TabsConfig:
        main_tab = Config(name="Content", cols=["details"])
        translations_tab = Config(name="Translations", cols=["translations"])
        super_tab = Config(name="Super", cols=["super"])

class LanguagesInline(admin.StackedInline):
    def get_formset(self, request, obj=None, **kwargs):
        langs = AppLang.objects.filter(app_id=request.session['appid'])
        lang_num = langs.count()
        for lang in langs:
            if lang.main:
                lang_num -= 1
        self.extra = lang_num
        self.max_num = lang_num
        return super(LanguagesInline, self).get_formset(request, obj, **kwargs)


    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(LanguagesInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'lang':
            field.queryset = field.queryset.filter(app_id=request.session['appid'], main=False)
        return field


class Modmin(TabbedModelAdmin):
    super_list_filter = ()
    super_list_display = ()
    place_exclude = None
    place_readonly = None
    has_place = False
    save_on_top = True
    list_only = False
    app_limited_fk = []
    list_field_for_module = [] #('module_codename','field_name')
#    tabbed = False
    def __init__(self, model, admin_site):
        self._list_filter = self.list_filter
        self._list_display = self.list_display
        self._readonly_fields = self.readonly_fields
        super(Modmin, self).__init__(model, admin_site)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            # if self.place_exclude:
            #     obj.place_id = request.session['placeid']
            obj.app_id = request.session['appid']
        obj.save()

    def has_module(self, request, module_name):
        return ModuleSelection.objects.filter(app_id=request.session['appid'], active=True, module__codename=module_name).count()

    def change_view(self, request, extra_context=None):
        if not request.user.is_superuser and self.list_only:
            raise Http404
#        if self.tabbed:
#            change_form_template = 'tabbed_change_form.html'
#         if self.place_exclude:
#             if not request.user.is_superuser:
#                 self.exclude = self.place_exclude + (self.exclude or [])
#             else:
#                 self.exclude = None
        if not request.user.is_superuser:
            self.exclude = (self.exclude or []) + ['app']

        if self.place_readonly:
            if not request.user.is_superuser:
                self.readonly_fields = list(self._readonly_fields) + list(self.place_readonly)
            else:
                self.readonly_fields = self._readonly_fields

        return super(Modmin, self).change_view(request, extra_context)


    def add_view(self, request, form_url='', extra_context=None):

        # if self.place_exclude:
        #
        #     if not request.user.is_superuser:
        #         self.exclude = self.place_exclude + (self.exclude or [])
        #     else:
        #         self.exclude = None

        if not request.user.is_superuser:
            self.exclude = (self.exclude or []) + ['app']

        if self.place_readonly:
            if not request.user.is_superuser:
                self.readonly_fields = list(self._readonly_fields) + list(self.place_readonly)
            else:
                self.readonly_fields = self._readonly_fields

        return super(Modmin, self).add_view(request, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
#        if self.list_field_for_module:
        for module, field_name in self.list_field_for_module:
            if self.has_module(request, module):
                if field_name not in self.list_display:
                    self.list_display.append(field_name)
            elif field_name in self.list_display:
                self.list_display.remove(field_name)

        if self.super_list_filter:
            if not request.user.is_superuser:
                self.list_filter = self._list_filter
            else:
                self.list_filter = list(self._list_filter) + list(self.super_list_filter)
        if self.super_list_display:
            if not request.user.is_superuser:
                self.list_display = self._list_display
            else:
                self.list_display = list(self._list_display) + list(self.super_list_display)
        return super(Modmin, self).changelist_view(request, extra_context)



    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not self.app_limited_fk:
            return super(Modmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        field = super(Modmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if not request.user.is_superuser and db_field.name in self.app_limited_fk:
            field.queryset = field.queryset.filter(app_id=request.session['appid'])
        return field

    def queryset(self, request):
        qs = super(Modmin, self).queryset(request)
        if not request.user.is_superuser:

            appid = request.session['appid']
            placeid = request.session.get('placeid')
            qs = qs.filter(app=appid)
            if  self.has_place and placeid:
                qs = qs.filter(place=placeid)
        return qs
#
#    class Media:
#        css = {
#            "all": ("/media/css/jquery-ui-1.8.22.custom.css", "/media/css/tabs.css")
#        }
#        js = ("/media/js/jquery-ui-1.8.22.custom.min.js",)  # Note: was modified to use django.jQuery and not jQuery
