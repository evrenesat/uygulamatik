# -*- coding: utf-8 -*-
from django.contrib import admin
from admin_tabs.helpers import Config

from at_shop_order.models import OrderHead, LocalOrderItem, OrderTable, OrderTableTranslation
from umatik.admin import Modmin
from umatik.admin.modmin import LanguagesInline, TransConfig

__author__ = 'ozgur'
__creation_date__ = '11.03.2013' '15:43'

#from home.models import Menu, ToDoList,Favorites,FavoritesGroup, Docs, DownloadList

class OrderTableTranslationInline(LanguagesInline):
    model = OrderTableTranslation


class OrderTableConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=["name", 'explanation', 'sort', 'qrcode'])
        translations = Config(inline="OrderTableTranslationInline")


class OrderTableAdmin(Modmin):
    list_display = ('name', 'sort')
    list_editable = ('sort',)
    readonly_fields = ['qrcode']
    # change_template = 'admin/at_shop_order/ordertable/change_form.html'
    page_config_class = OrderTableConfig
    inlines = [OrderTableTranslationInline]

class LocalOrderItemInline(admin.TabularInline):
    model = LocalOrderItem
    raw_id_fields = ['product']


class OrderHeadAdmin(Modmin):
    list_display = ('order_table', 'status')
    list_filter = ('status',)

    inlines = [LocalOrderItemInline]


admin.site.register(OrderHead, OrderHeadAdmin)
admin.site.register(OrderTable, OrderTableAdmin)
admin.site.register(LocalOrderItem)



