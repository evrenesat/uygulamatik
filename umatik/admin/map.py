#-*- coding:utf-8 -*-
# __author__ = 'Evren Esat Ozkan'
from django.contrib import admin
from admin_tabs.helpers import TabbedPageConfig, Config
from django.utils.translation import ugettext_lazy as _
from modmin import Modmin
from umatik.models import *


class NodePageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        node = Config(fields=["app", "type", "name", "map", "x", "y"])
        matrix = Config(inline="MatrixInline")

    class ColsConfig:
        node = Config(fieldsets=["node"], css_classes=["col1"])
        matrix = Config(fieldsets=["matrix"], css_classes=["matrix"])

    class TabsConfig:
        main_tab = Config(name="Node", cols=["node"])
        matrix_tab = Config(name="Matrix", cols=["matrix"])


class MatrixInline(admin.TabularInline):
    model = Node.nbhds.through
    extra = 2
    fk_name = 'node1'
    raw_id_fields = ('node1', 'node2')


class MatrixAdmin(admin.ModelAdmin):
    list_display = ['app', 'node1', 'node2', 'distance']


class NodeAdmin(Modmin):
    page_config_class = NodePageConfig
    list_display = ['name', 'type', 'x', 'y']
    list_filter = ["map", ]
    search_fields = ['name']
    #    list_editable = ['x', 'y', 'type',]
    inlines = [MatrixInline]


class MapAdmin(Modmin):
#    pass
    #list_field_for_module = (('Nvs','edit_nodes') ,)
    list_display = ["name", 'order', 'edit_nodes']
    list_editable = ['order']
