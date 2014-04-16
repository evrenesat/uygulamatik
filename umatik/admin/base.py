#-*- coding:utf-8 -*-
# __author__ = 'Evren Esat Ozkan'
from django.contrib import admin
from admin_tabs.helpers import TabbedPageConfig, Config
from django.utils.translation import ugettext_lazy as _
from modmin import Modmin, LanguagesInline, TransConfig
from treeadmin.admin import TreeAdmin as TreeADMIN
from umatik.models import *


class ContentConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=["parent", "main", "title", "summary", "detail", "image",
                                  "active", "publish_date", "sort"])
        translations = Config(inline="ContentTranslationInline")


class ContentTranslationInline(LanguagesInline):
    model = ContentTranslation


class ContentAdmin(TreeADMIN):
    page_config_class = ContentConfig
    # raw_id_fields = ['icon']
    app_limited_fk = ['parent', ]
    inlines = [ContentTranslationInline, ]
    list_display = ['title', 'main', 'active', 'sort']
    list_editable = ['active']

    def save_model(self, request, obj, form, change):
        super(ContentAdmin, self).save_model(request, obj, form, change)
        obj.make_main()

class PhotoAdmin(Modmin):
    pass


class NewsTranslationInline(LanguagesInline):
    model = NewsTranslation


class NewsConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=["title", "summary", "detail", "image", "publish_date", "sort"])
        translations = Config(inline="NewsTranslationInline")


class NewsAdmin(Modmin):
    list_display = ['title', 'sort']
    list_editable = ['sort']
    page_config_class = NewsConfig
    inlines = [NewsTranslationInline, ]


class PageTranslationInline(LanguagesInline):
    model = PageTranslation


class PageConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=["title", "summary", "detail", "image", "sort"])
        translations = Config(inline="PageTranslationInline")


class PageAdmin(Modmin):
    page_config_class = PageConfig
    inlines = [PageTranslationInline, ]
    list_display = ['title', 'app', 'sort']
    list_editable = ['sort']


class ElogAdmin(admin.ModelAdmin):
    pass


class VersionAdmin(admin.ModelAdmin):
    pass


class FeedbackAdmin(Modmin):
    has_place = True
    raw_id_fields = ('place', 'customer')
    list_filter = ['type']
    list_display = ['type', 'date']
    super_list_filter = ['place', 'forhost', 'archived', 'called']
    readonly_fields = ['content_type']
    place_exclude = ['place', 'content_type']
    place_readonly = ['customer']
    date_hierarchy = 'date'


class ProfileAdmin(admin.ModelAdmin):
    pass

from qurl.models import QRcode
class QRcodeAdmin(admin.ModelAdmin):
    pass
