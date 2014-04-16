#-*- coding:utf-8 -*-
# __author__ = 'Evren Esat Ozkan'
from django.contrib import admin
from admin_tabs.helpers import TabbedPageConfig, Config
from django.utils.translation import ugettext_lazy as _
from modmin import Modmin, LanguagesInline, TransConfig
from umatik.models import *


class MenuItemTranslationInline(LanguagesInline):
    model = MenuItemTranslation


class MenuItemConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=['name', 'price', 'cut_price', 'category', 'showcase', 'sort', 'image', 'description', 'prepare_time'])
        translations = Config(inline="MenuItemTranslationInline")


class MenuItemAdmin(Modmin):
    list_display = ['name', 'price', 'cut_price', 'category', 'showcase', 'sort']
    list_editable = ['price', 'cut_price', 'showcase', 'sort']
    list_filter = ['category']
    page_config_class = MenuItemConfig
    inlines = [MenuItemTranslationInline, ]


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    exclude = ('sort',)
    extra = 0


class MenuCategoryTranslationInline(LanguagesInline):
    model = MenuCategoryTranslation


class MenuCategoryConfig(TabbedPageConfig):
    class FieldsetsConfig:
        details = Config(fields=['name', 'sort', 'image'])
        translations = Config(inline="MenuCategoryTranslationInline")
        items = Config(inline="MenuItemInline")
        super = Config(fields=["app"])

    class ColsConfig:
        details = Config(fieldsets=["details"], css_classes=["col1"])
        items = Config(fieldsets=["items"], css_classes=["col1"])
        translations = Config(fieldsets=["translations"])
        super = Config(fieldsets=["super"])

    class TabsConfig:
        main_tab = Config(name="Details", cols=["details"])
        items_tab = Config(name="Items", cols=["items"])
        translations_tab = Config(name="Translations", cols=["translations"])
        super_tab = Config(name="Super", cols=["super"])




class MenuCategoryAdmin(Modmin):
    list_display = ['name', 'sort']
    list_editable = ['sort']
    page_config_class = MenuCategoryConfig
    inlines = [MenuItemInline, MenuCategoryTranslationInline]
