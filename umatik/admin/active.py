#-*- coding:utf-8 -*-
# __author__ = 'Evren Esat Ozkan'
from django.contrib import admin
from admin_tabs.helpers import TabbedPageConfig, Config
from django.utils.translation import ugettext_lazy as _
from modmin import Modmin, LanguagesInline, TransConfig
from umatik.models import *


class ExhibitorPageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        details = Config(fields=["company", "logo", "phone", "email", "profile", "node", 'qrcode'])
        files = Config(inline="ExhibitorFilesInline")
        super = Config(fields=["app"])
        translations = Config(inline="ExhibitorTranslationInline")

    class ColsConfig:
        details = Config(fieldsets=["details"], css_classes=["col1"])
        files = Config(fieldsets=["files"], css_classes=["col1"])
        translations = Config(fieldsets=["translations"])
        super = Config(fieldsets=["super"])

    class TabsConfig:
        main_tab = Config(name="Details", cols=["details"])
        files_tab = Config(name="Documents", cols=["files"])
        translations_tab = Config(name="Translations", cols=["translations"])
        super_tab = Config(name="Super", cols=["super"])


class ExhibitorTranslationInline(LanguagesInline):
    model = ExhibitorTranslation


#
#class ExhibitorFilesInlineFormset(djfm.BaseInlineFormSet):
#    pass
#

class ExhibitorFilesInline(admin.TabularInline):
    model = ExhibitorFiles
    extra = 2
    exclude = ['app']

#    formset = ExhibitorFilesInlineFormset


class ExhibitorFilesAdmin(Modmin):
    pass


class ExhibitorAdmin(Modmin):
    page_config_class = ExhibitorPageConfig
    #    fields = ("app", 'company', "profile", 'logo','phone','node',"email")
    inlines = [ExhibitorFilesInline, ExhibitorTranslationInline]
    readonly_fields = ['qrcode']


class SponsorTypeAdmin(Modmin):
    list_display = ['title', 'app', 'sort']
    list_editable = ['sort']


class SponsorAdmin(Modmin):
    app_limited_fk = ['type']


class ContentAdmin(Modmin):
    app_limited_fk = ['lang']


class DelegateTranslationInline(LanguagesInline):
    model = DelegateTranslation


class DelegateConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=['firstname', 'lastname', 'company', 'position', 'photo', 'profile'])
        translations = Config(inline="DelegateTranslationInline")


class DelegateAdmin(Modmin):
    list_display = ['firstname', 'lastname']
    page_config_class = DelegateConfig
    inlines = [DelegateTranslationInline, ]


class SpeakerTranslationInline(LanguagesInline):
    model = SpeakerTranslation


class SpeakerConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=["firstname", "lastname", "company", "position", "profile", "photo"])
        translations = Config(inline="SpeakerTranslationInline")


class SpeakerAdmin(Modmin):
    page_config_class = SpeakerConfig
    inlines = [SpeakerTranslationInline, ]



class EventPageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        info = Config(fields=["title", ("date", "start", "end"), "description", "image", "location", "node"])
        speakers = Config(fields=["speakers"])
        super = Config(fields=["app"])

    class ColsConfig:
        info = Config(fieldsets=["info"], css_classes=["col1"])
        speakers = Config(fieldsets=["speakers"], css_classes=["col1"])
        super = Config(fieldsets=["super"])

    class TabsConfig:
        main_tab = Config(name="Event", cols=["info"])
        speakers_tab = Config(name="Speakers", cols=["speakers"])
        super_tab = Config(name="Super", cols=["super"])


class EventAdmin(Modmin):
    page_config_class = EventPageConfig
    fields = ("app", 'title', ('date', 'start', 'end'), "description", "speakers", 'image', 'location', 'node')
    filter_horizontal = ('speakers',)
