#-*- coding:utf-8 -*-
from itertools import groupby
import json
from operator import itemgetter
from os.path import basename
import re
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template import Template, Context
from django.utils.safestring import mark_safe
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _, activate
from django.utils.translation import ugettext
import hashlib
from django.db.models import F, signals, Sum
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from qurl.models import QRcode
from umatik import countries
from utils.cache import kes
import unicodedata
from countries import COUNTRIES, LANGUAGES
from django.core.files.storage import FileSystemStorage
from utils.thumbnailer import customThumbnailer
from utils.cssmin import cssmin
from uuid import uuid4
from django.utils.translation import ugettext_lazy as _, activate
import threading
from ckeditor.fields import RichTextField

_thread_locals = threading.local()
#FIXME: app_id viewda tanimlaniyor, -mumkunse apiye ozel- middlewarede tanimlanmali
_thread_locals.api_lang = ''
_thread_locals.app_id = 0


def regroupEvents(events_dict):
    """
    @param list. events_dict: Events.objects.values() sozlugu girer
    @return: sorted tuple, 'date' alanina gore gruplanip, 'start' alanina gore siralanmis
    """
    key = itemgetter('date')
    return [(date.strftime("%d/%m/%Y"), sorted(list(datevents), key=itemgetter('start')))
            for date, datevents in
            groupby(sorted(events_dict, key=key), key=key)]


def imgcleanlist(img_list):
    ilist = []
    for i in img_list:
        if type(i) is tuple:
            ilist.extend(list(i))
        else:
            ilist.append(i)
    return map(imgclean, filter(bool, ilist))


class AppManager(models.Manager):
    """o anki api cagrisi sirasinda etkin app'a ait nesneleri dondurur
    _thread_locals.app_id `views.get_all_records` altinda tanimlanir
    """

    def get_query_set(self):
        return super(AppManager, self).get_query_set().filter(app_id=_thread_locals.app_id)


class TModel(models.Model):
    #
    # def __init__(self, *args, **kwargs):
    #     self.source.related_name = 'translations'
    #     super(TModel, self).__init__(*args, **kwargs)

    lang = models.ForeignKey('AppLang', verbose_name=_('Language'))
    app = models.ForeignKey('Application', editable=False)

    class Meta:
        abstract = True
        unique_together = (('lang', 'source'),)

    def save(self, *args, **kwargs):
        if not self.id:
            self.app = self.source.app
        super(TModel, self).save(*args, **kwargs)


class UModel(models.Model):
    def __init__(self, *args, **kwargs):
        super(UModel, self).__init__(*args, **kwargs)
        self.Trns = self._Trns(self)

    objects = models.Manager()
    abjects = AppManager()

    @classmethod
    def _get_fields(cls, base, trans):
        """
        gerekiyorsa cevrilebilir alanlarin basina translations__ ekler
        _thread_locals.api_lang `views.get_all_records` altinda tanimlaniyor
        values ya da values_list tarafindan kullanilacak alan listesi dondurur

        @param cls:
        @param base: list, cevrilmeyecek alanlar
        @param trans: list, translations modelinde tanimlanmis alanlar
        @return: list
        """
        base.extend(trans)  # cevirilerin bos olmasi ihtimalian karsi default degerleri her sekilde almak istiyoruz.
        if _thread_locals.api_lang:  # _thread_locals.api_lang `views.get_all_records` altinda tanimlaniyor
            trans = map(lambda t: "translations__%s" % t, trans)
        base.extend(trans)
        return base

    @classmethod
    def _get_values(cls, base_fields, trans_fields, get_qs=False):
        """etkin app'a ozel object.values kisayolu

        @param get_qs: bool, false liste yerine queryset dondur
        @param base_fields: list, cevrilmeyecek alanlar
        @param trans_fields: list, translations modelinden tanimlanmis alanlar
        @return: list of dict
        """
        fields = cls._get_fields(base_fields, trans_fields)
        result_list = cls.abjects.values(*fields)
        if get_qs:
            return result_list
        elif not _thread_locals.api_lang:
            return list(result_list)
        else:
            result_set = []
            for result in result_list:
                for trnsfld in trans_fields:
                    trans_field_name = "translations__%s" % trnsfld
                    if result[trans_field_name]:
                        result[trnsfld] = result[trans_field_name]
                    del result[trans_field_name]
                result_set.append(result)
            return result_set

    class Meta:
        abstract = True

    class _Trns:
        """
        UModel'lerin cevrilebilir ozelliklerine nesne yönelimli olarak erişimi kolaylaştıran proxy nesne
        (UModel)News.title ve (TModel)NewsTranslation.title var ise
        News.Trans.title nesnesi;
          - Eger api_lang degiskeni mevcut ise (yani istemci uygulamanin ana dili disinda desteklenen
         bir dili kullaniyorsa) ve o ozelligin o dil icin cevirisi girilmis ise NewTranslations.title'i dondurur.
          - Diger durumlarda News.title'i dondurur.
        """

        def __init__(self, owner):
            self.owner = owner

        def __getattr__(self, name):
            if _thread_locals.api_lang:
                obj = self.owner.translations.get(lang__code=_thread_locals.api_lang)
                return mark_safe(getattr(obj, name) or getattr(self.owner, name).replace('\r','').replace('\n','').replace('\t',''))
            else:
                return mark_safe(getattr(self.owner, name).replace('\r','').replace('\n','').replace('\t',''))


def imgclean(img_name):
    return re.sub(r'(.*)/(.*)', r'\2', img_name) if img_name else ''


class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """

    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)


class Module(models.Model):
    """Application modules"""

    name = models.CharField(_('Name'), max_length=50, help_text=_('Name of the module'))
    codename = models.CharField(_('Code name'), max_length=20, help_text=_('Code name of the module'))
    title = models.CharField(_('Menu title'), max_length=30, help_text=_('Menu\'s title that\'s visible to users'))
    active = models.BooleanField(_('Active'), default=True, help_text=_('Is module active?'))
    order = models.SmallIntegerField(_('Sort'), default=1,
                                     help_text=_('Order of the module (from left to right or from top to bottom)'))
    visible = models.BooleanField(_('Visible'), default=True, help_text=_('Module has an icon on app menu'))
    #    icon = models.ImageField(_("Icon"), upload_to="uploads", null=True, blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    def getPrimaryIcon(self):
        return self.related_icons.get(primary=True)

    def getIcon(self, app):
        icon = self.related_icons.filter(id__in=app.theme.iconset.icon_set.values_list('id', flat=True))
        return icon[0] if icon else self.getPrimaryIcon()

    def getTitle(self):
        #TODO: Multi-lang support
        return self.title

    def addToApp(self, app):
        self.moduleselection_set.get_or_create(app=app, defaults={
            'icon': self.getIcon(app), 'title': self.getTitle(), 'visible': self.visible, 'order': self.order})

    class Meta:
        ordering = ['order']

        #        get_latest_by = "timestamp"

        verbose_name = _('App Module')
        verbose_name_plural = _('App Modules')

    def __unicode__(self):
        return '%s' % (self.name,)


class ModuleSelection(models.Model):
    """Application modules"""
    module = models.ForeignKey(Module, help_text=_('Module to be used'))
    active = models.BooleanField(_('Active'), default=True, help_text=_('Is this module active?'))
    app = models.ForeignKey('Application', help_text=_('Application that the selected module is included'))
    icon = models.ForeignKey('Icon', null=True, blank=True, help_text=_('Icon for the selected module'))
    xtra = models.CharField(_('Extra data'), max_length=255)
    visible = models.BooleanField(_('Visible'), default=True, help_text=_('Module has an icon on app menu'))
    title = models.CharField(_('Visible name'), max_length=30, null=True, blank=True, default='',
                             help_text=_('Module\'s title that is visible to users'))
    order = models.SmallIntegerField(_('Sort'), default=1,
                                     help_text=_('Order of the module (from left to right or from top to bottom)'))
    customicon = models.ImageField(_("Custom icon"), upload_to="uploads", null=True, blank=True,
                                   help_text=_('Custom icon for the module'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['order']
        #        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')
        unique_together = ('module', 'app', 'xtra')

    def get_xtra(self):
        return json.loads(self.xtra) if self.xtra else {}

    def __unicode__(self):
        return '%s' % (self.module.name,)


class AppType(models.Model):
    """Application type"""

    name = models.CharField(_('Name'), max_length=50, help_text=_('Name of the generic application type'))
    codename = models.SlugField(_('Code name'), max_length=30, help_text=_('Code name of this application'))
    modules = models.ManyToManyField(Module, help_text=_('Modules which this application will have'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    icon = models.ImageField(_("Icon"), upload_to="uploads", null=True, blank=True,
                             help_text=_('Icon of the application'))
    iconb = models.ImageField(_("Big icon"), upload_to="uploads", null=True, blank=True,
                              help_text=_('A bigger icon for the application (is used in tablets or when necessary)'))

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.name,)


class Theme(models.Model):
    """Application modules"""

    iconset = models.ForeignKey('IconCategory', verbose_name=_('Icon set'))
    name = models.CharField(_('Name'), max_length=50, help_text=_('Name of this theme'))
    codename = models.CharField(_('Code name'), max_length=20, null=True, blank=True,
                                help_text=_('Code name of this theme'))
    # jmt = models.CharField(_('JM Theme'), max_length=2, default='a')
    transparent_background = models.CharField(_('Semi transparent BG'), max_length=25, default='rgba(0,0,0, 0.60)')
    transparent_background2 = models.CharField(_('Very transparent BG'), max_length=25, default='rgba(0,0,0, 0.30)')
    css = models.TextField(_('CSS'), null=True, blank=True)
    processed_css = models.TextField(_('Processed CSS'), null=True, blank=True, editable=False)
    web_processed_css = models.TextField(_('Processed CSS'), null=True, blank=True, editable=False)
    active = models.BooleanField(_('Active'), default=True)
    order = models.SmallIntegerField(_('Sort'), default=1)
    preview = models.ImageField(_("Preview"), upload_to="uploads", null=True, blank=True,
                                help_text=_('Preview of this theme'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['order']

        #        get_latest_by = "timestamp"

    #verbose_name = _('')
    #verbose_name_plural = _('')
    def process_css(self):
        mincss = cssmin(self.css, 500)
        for ti in self.themeimage_set.all():
            mincss = mincss.replace(ti.filename, basename(ti.image.file.name))
        self.processed_css = mincss.replace('images/', '')
        self.web_processed_css = mincss.replace('images/', settings.APPSERVERURL + "media/uploads/")

    def get_image_list(self):
        return map(lambda a: a.replace('uplaads/', ''), self.themeimage_set.values_list('image', flat=True))

    def save(self, *args, **kwargs):
        self.process_css()
        super(Theme, self).save(*args, **kwargs)

    def __unicode__(self):
        return mark_safe(
            "<span style='text-align:center;'>%s<br><img src='/media/%s' width='100' /></span>" % (
                self.name, self.preview))


def save_filename(instance, filename):
    instance.filename = filename
    fp = filename.split('.')
    return 'uploads/%s_%s.%s' % (fp[0], str(uuid4()).split('-')[0], fp[-1])


class ThemeImage(models.Model):
    """theme specific images"""

    theme = models.ForeignKey(Theme, help_text=_('The theme which the image is added'))
    image = models.ImageField(_("File"), upload_to=save_filename, help_text=_('Image to upload'))
    filename = models.CharField(_('Image name'), max_length=50, null=True, blank=True,
                                help_text=_('Name of image file'))

    def save(self, *args, **kwargs):
        super(ThemeImage, self).save(*args, **kwargs)
        self.theme.save()

    class Meta:
        verbose_name = _(u"Theme image")
        verbose_name_plural = _(u"Theme images")

    def __unicode__(self):
        return '%s' % (self.filename,)


class IconCategory(models.Model):
    """ Holds system-wide icon categories """
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True, help_text=_('Name of the icon category'))
    sort = models.SmallIntegerField(_('Sort'), default=1, null=True, blank=True, help_text=_('Order of the category'))

    class Meta:
        ordering = ["sort"]
        verbose_name = _("Icon set")
        verbose_name_plural = _("Icon sets")

    def __unicode__(self):
        return self.name


class Icon(models.Model):
    """Application modules"""

    # theme = models.ManyToManyField(Theme, null=True, blank=True, help_text=_('The themes that will use this icon'))
    category = models.ForeignKey(IconCategory, verbose_name=_('Theme'), null=True, blank=False, help_text=_('Iconset of this icon'))
    module = models.ForeignKey(Module, verbose_name=_('Category'), null=True, blank=True, related_name='related_icons',
                               help_text=_('Module which this icon will belong to'))
    keywords = models.CharField(_('Keywords'), max_length=50, null=True, blank=True,
                                help_text=_('Keywords for this icon'))
    primary = models.BooleanField(_('Primary icon'), default=False, help_text=_('Preferred icon for the module'))
    image = models.ImageField(_("File"), upload_to="uploads", null=True, blank=True)
    hdimage = models.ImageField(_("HD File"), upload_to="uploads", null=True, blank=True,
                                help_text=_('High definition version of the icon'))
    active = models.BooleanField(_('Active'), default=True, help_text=_('Is icon active?'))

    def getFileName(self):
        return imgclean(self.image.file.name)

    class Meta:
        pass
        # unique_together = ('module', 'primary')

        #        get_latest_by = "timestamp"
        verbose_name = _('Icon')
        verbose_name_plural = _('Icons')

    #    def __unicode__(self):
    #        return '%s > %s' % (self.theme.name, self.image.file.name.split('/')[-1].split('.')[0])

    def __unicode__(self):
        return mark_safe("<img src='/media/%s' width='50' />" % self.image)

    __unicode__.allow_tags = True

    def ikon(self):
        return mark_safe("<img src='/media/%s' width='50' />" % self.image)

    ikon.allow_tags = True


HEADER_TYPES = (
    ('icon', _("Icon")),
    ('banner', _("Banner")),
    ('text', _("Text")),
    ('space', _("Empty space")),
    ('none', _("None")),

)


class ApplicationStatus(models.Model):
    """ApplicationStatus"""

    title = models.CharField(_('Title'), max_length=40, help_text=_('Title of the application status'))
    default = models.BooleanField(_('Default state'), default=False,
                                  help_text=_("If checked, this will be the default state of the application"))
    description = RichTextField(_('Description'), max_length=140, help_text=_('Description of this status'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    @classmethod
    def get_default(cls):
        defs = cls.objects.filter(default=True)
        return defs[0] if defs else None

    def __unicode__(self):
        return '%s' % (self.title,)


class Application(models.Model):
    """Base application settings"""

    status = models.ForeignKey(ApplicationStatus, null=True, blank=True, help_text=_('Status of the application'))
    type = models.ForeignKey(AppType, help_text=_('Type of the application'))
    theme = models.ForeignKey(Theme, verbose_name=_('Base theme'),
                              help_text=_('The theme to be used in the application'))
    # jmt = models.CharField(_('JM Theme'), max_length=2, default='a')
    css = RichTextField(_('CSS'), null=True, blank=True, help_text=_('Css for the application'))
    name_short = models.CharField(_('Short name'), max_length=40, help_text=_('Short name of the application'))
    subdomain = models.SlugField(_('Subdomain '), max_length=25, blank=True,
                                 help_text=_('uygulamatik.com subdomain for your web app. Min 6, max 25 character'))
    name_long = models.CharField(_('Long name'), max_length=70, null=True, blank=True,
                                 help_text=_('Full name of the application'))
    company = models.CharField(_('Company / Organisation'), max_length=100, null=True, blank=True,
                               help_text=_('Company of the application'))
    icon = models.ImageField(_("App icon"), upload_to="uploads", null=True, blank=True,
                             help_text=_('Icon of the application'))
    logo_small = models.ImageField(_("Logo (small)"), upload_to="uploads", null=True, blank=True,
                                   help_text=_('Small logo of the application'))
    logo_big = models.ImageField(_("Logo (big)"), upload_to="uploads", null=True, blank=True,
                                 help_text=_('Big logo of the application'))

    header_type = models.CharField(_('Header type'), choices=HEADER_TYPES, default="icon", max_length=10,
                                   help_text=_('How the header of the application will look like'))
    header_image = models.ImageField(_("Header banner"), upload_to="uploads", null=True, blank=True,
                                     help_text=_('A banner image for the header of the application'))
    splash_image = models.ImageField(_("Splash image"), upload_to="uploads", null=True, blank=True,
                                     help_text=_(
                                         'The image that will appear on the screen while the application is '
                                         'launching'))
    background_image = models.ImageField(_("Background image"), upload_to="uploads", null=True, blank=True,
                                         help_text=_('The image that will be the background of the main screen'))
    app_bg = models.BooleanField(_('In app background'), default=False,
                                 help_text=_("Use main screen's background image for whole app"))
    show_qrcode_button = models.BooleanField(_('Show QRCode button on main screen'), default=True)
    background_color = models.CharField(_('Background color'), max_length=14, null=True, blank=True,
                                        help_text=_('The color of the application background'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    default_language = models.CharField(_('Application language'), max_length=2, choices=LANGUAGES, default='tr')

    #iletisim ve adres bilgileri
    lat = models.FloatField(_('Latitude'), default=0.0, help_text=_('Latitude info of the application owner'))
    lon = models.FloatField(_('Longitude'), default=0.0, help_text=_('Longitude info of the application owner'))
    address = models.CharField(_('Address Line'), max_length=100, null=True, blank=True,
                               help_text=_('Address of the application owner company'))
    country = models.CharField(_('Country'), max_length=2, choices=COUNTRIES, null=True, blank=True,
                               help_text=_('Country of the application owner company'))
    street = models.CharField(_('Street'), max_length=60, null=True, blank=True,
                              help_text=_('Street where the application owner company is'))
    city = models.CharField(_('City'), max_length=40, null=True, blank=True,
                            help_text=_('City where the application owner company is'))
    phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True,
                             help_text=_('Phone number of the application owner (0XXX XXX XX XX)'))
    fax = models.CharField(_('Fax'), max_length=20, null=True, blank=True,
                           help_text=_('Fax number of the application owner company'))
    active = models.BooleanField(_('Active'), default=True, help_text=_('Is the application active?'))
    published = models.BooleanField(_('Publish App'), default=False, help_text=_('Is the application published?'))

    @classmethod
    def get_theme_images(cls, appid):
        return cls.objects.get(pk=appid).theme.get_image_list()

    def save(self, *args, **kwargs):
        if not self.id:
            self.status = ApplicationStatus.get_default()
        super(Application, self).save(*args, **kwargs)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')
        # permissions = (("is_an_app_admin", "Is an app admin"),)

    def __unicode__(self):
        return '%s' % (self.name_short)

    def updateTheme(self):
        for ms in self.moduleselection_set.all():
            icons = self.theme.iconset.icon_set.filter(module=ms.module)
            if icons:
                ms.icon = icons[0]
                ms.save()

    def createModuleSelections(self):
        for m in self.type.modules.filter(visible=True):
            m.addToApp(self)

#LANGUAGES = (
#    ('tr', u'Türkçe'), ('en', u'English'), ('de', u'German'), ('ru', u'Russia'), ('fr', u'French'), ('it', u'Italian'),)
BLOCK_STATUS = ((0, 'None'), (1, 'Incomplete'), (2, 'Complete'))

BLOCK_TYPES = ((1, 'HTML Box'), (2, 'Title'), (3, 'Text Box'))


class Block(models.Model):
    """Content blocks"""
    app = models.ForeignKey(Application, verbose_name=_('Application'), null=True, blank=True,
                            help_text=_('The application that holds this block data'))
    keyword = models.CharField(_('Source string'), max_length=255, help_text=_('Keywords of the block'))
    translation = models.CharField(_('Translation'), max_length=255, default='', blank=True)
    translated = models.BooleanField(_('Translated'), default=False)
    lang = models.CharField(_('Language'), max_length=5, help_text=_('Translation language'))
    # type = models.SmallIntegerField(_('Type'), choices=BLOCK_TYPES, default=0, help_text=_('Type of the block'))
    # status = models.SmallIntegerField(_('Status'), choices=BLOCK_STATUS, default=0, help_text=_('Status of the block'))

    def save(self, *args, **kwargs):
        self.translated = bool(self.translation.strip())
        super(Block, self).save(*args, **kwargs)
    #     self.create_translations()
    #
    # def create_translations(self):
    #     for k in self.app.applang_set.values_list('code', flat=True):
    #         cset = self.blocktranslation_set.filter(lang=k)
    #         if not cset:
    #             self.blocktranslation_set.create(lang=k)


    class Meta:
        verbose_name = _(u"Translation")
        verbose_name_plural = _(u"Translations")
        ordering = ['keyword']
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.keyword,)

#
# class BlockTranslation(models.Model):
#     """block content for each language"""
#     KES_PREFIX = 'CEVIR'
#     app = models.ForeignKey(Application, verbose_name=_('Application'), null=True, blank=True,
#                             help_text=_('The application that hold this block translation data'))
#     block = models.ForeignKey(Block, verbose_name=_('Original Block'), help_text=_('Block to translate'))
#     keyword = models.CharField(max_length=100, editable=False, help_text=_('Keywords of the block translation'))
#     lang = models.CharField(_('Language'), max_length=5, choices=LANGUAGES, help_text=_('Translation language'))
#     translation = RichTextField(_('Translation'), default='', blank=True, help_text=_('Translation of the block'))
#
#     class Meta:
#         ordering = ['lang']
#         #app_label = 'website'
#         verbose_name = _(u"Blok çevirisi")
#         verbose_name_plural = _(u"Blok çevirileri")
#
#     def __unicode__(self):
#         return '%s for %s' % (self.keyword, self.lang)
#
#     def save(self, *args, **kwargs):
#         self.keyword = slugify(self.block.keyword)
#         if self.block.type in [2, 3]:
#             self.translation = strip_tags(self.translation)
#         super(BlockTranslation, self).save(*args, **kwargs)
#         kes(self.KES_PREFIX, self.keyword, self.lang).s(self.translation)


class ProductCategoryTranslation(TModel):
    source = models.ForeignKey('ProductCategory', related_name='translations',
                               help_text=_('ProductCategory to translate'))
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True, help_text=_('Name of the category'))
    #translatable fields here


class ProductCategory(UModel):
    """ AVM wide store category"""
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that has this product category'))
    parent_category = models.ForeignKey("self", blank=True, null=True, verbose_name=_("Parent Category"),
                                        help_text=_('Parent category of this product category'))
    image = models.ImageField(_("Image"), upload_to="uploads", null=True, blank=True,
                              help_text=_('Image of the category'))
    order = models.SmallIntegerField(_('Sort'), default=100, help_text=_('Order of the category'))
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True, help_text=_('Name of the category'))
    pid = models.CharField(max_length=32, editable=False, null=True, blank=True)

    class Meta:
        db_table = "product_category"
        ordering = ["order"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ProductCategory, self).save(*args, **kwargs)
        if not self.pid:
            self.pid = hashlib.md5('pc_%s' % self.id).hexdigest()
            super(ProductCategory, self).save(*args, **kwargs)

    @classmethod
    def get_data(cls):
        # return dict([(d['id'], d)
        #              for d in cls._get_values(['id', 'parent_category', 'parent_category__pid', 'image', 'pid'], ['name'])]) or {'none': True}
        categories = cls._get_values(['id', 'parent_category', 'parent_category__pid', 'image', 'pid'], ['name'])
        for c in categories:
            c['product_category_id'] = c['id']
            c['id'] = c['pid']
            del c['pid']
            c['upper_category'] = c['parent_category__pid']
            del c['parent_category__pid']
        return categories or {'none': True}
        #     c['image'] = imgclean(c['image'])
        #     #            images.append(c['image'])


class StoreProductCategoryTranslation(TModel):
    source = models.ForeignKey('StoreProductCategory', related_name='translations',
                               help_text=_('StoreProductCategory to translate'))
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True, help_text=_('Name of the category'))


class StoreProductCategory(UModel):
    """ AVM wide product category"""
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that has this store product category'))
    place = models.ForeignKey('Place', null=True, blank=True, help_text=_('The store that has this product category'))
    order = models.SmallIntegerField(_('Sort'), default=100, help_text=_('Order of the category'))
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True, help_text=_('Name of the category'))
    pid = models.CharField(max_length=32, editable=False, null=True, blank=True)

    # THUMB_PREFIX = 'spc'
    # THUMB_FIELDS = ['logo']
    # THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (480, 480, 'l')]

    class Meta:
        db_table = "store_product_category"
        ordering = ["order"]
        verbose_name = _("Store category")
        verbose_name_plural = _("Store categories")

    def __unicode__(self):
    #        return "%s > %s" % (self.place, self.name)
        return self.name

    def save(self, *args, **kwargs):
        super(StoreProductCategory, self).save(*args, **kwargs)
        if not self.pid:
            self.pid = hashlib.md5('spc_%s' % self.id).hexdigest()
            super(StoreProductCategory, self).save(*args, **kwargs)

    @classmethod
    def get_data(cls):
        # return dict([(d['id'], d)
        #              for d in cls._get_values(['id', 'order', 'place', 'pid', 'place__pid'], ['name'])]) or {'none': True}

        store_categories = cls._get_values(['id', 'order', 'place', 'pid', 'place__pid'], ['name'])

        for c in store_categories:
            c['store_product_category_id'] = c['id']
            c['place_id'] = c['place']
            c['id'] = c['pid']
            c['place'] = c['place__pid']
            del c['place__pid']
            del c['pid']
        return store_categories or {'none': True}


PLACE_TEMPLATES = [
    ('place_details', 'Mobil Alışveriş'),
    ('place_details_aboutus', 'Hakkımızda'),
]


class PlaceTranslation(TModel):
    source = models.ForeignKey('Place', related_name='translations', help_text=_('Place to translate'))
    description = RichTextField(_("Description"), null=True, blank=True, default='',
                                help_text=_('Description of the application'))
    #translatable fields here


class Place(UModel):
    """
    magaza, stand, katilimci
    """

    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that holds this place data'))
    category = models.ForeignKey(ProductCategory, verbose_name=_("Category"), null=True, blank=True,
                                 help_text=_('Category of the place'))

    name = models.CharField(_("Name"), max_length=100, null=True, blank=True, default='',
                            help_text=_('Name of the place'))
    template = models.CharField(_("Mağaza şablonu"), max_length=100, choices=PLACE_TEMPLATES, default='place_details',
                                help_text=_('Template of the application'))
    description = RichTextField(_("Description"), null=True, blank=True, default='',
                                help_text=_('Description of the application'))
    authorized_person = models.CharField(_("Authorized Person"), max_length=50, null=True, blank=True, default='',
                                         help_text=_('Authorized person of the place'))
    address = models.CharField(_("Address"), max_length=100, null=True, blank=True, default='',
                               help_text=_('Address of the place'))
    phone = models.CharField(_("Phone"), max_length=10, null=True, blank=True, default='',
                             help_text=_('Phone number of the place (0XXX XXX XX XX)'))
    gsm = models.CharField(_("GSM"), max_length=10, blank=True, default='',
                           help_text=_('GSM number of the place (0XXX XXX XX XX)'))
    email = models.EmailField(_("Email"), null=True, blank=True, default='', help_text=_('E-mail address of the place'))
    logo = models.ImageField(_("Tepe logo"), upload_to="uploads", blank=True,
                             help_text=_('This logo will appear on the top of the page'))
    llogo = models.ImageField(_("Liste logo"), upload_to="uploads", blank=True, null=True,
                              help_text=_('This logo will appear on the listing page'))
    background = models.CharField(_("Background"), max_length=7, default="#ffffff", blank=True,
                                  help_text=_('Background color of the place page'))
    node = models.OneToOneField('Node', null=True, blank=True, help_text=_('The node which this place is on'))
    pid = models.CharField(max_length=32, editable=False)

    THUMB_FIELDS = ['logo', 'llogo']
    THUMB_PREFIX = 'pl'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (750, 750, 'lrg')]

    class Meta:
        db_table = "places"
        verbose_name = _("Place")
        verbose_name_plural = _("Places")

    def save(self, *args, **kwargs):
        super(Place, self).save(*args, **kwargs)
        if not self.pid:
            self.pid = hashlib.md5('st_%s' % self.id).hexdigest()
            super(Place, self).save(*args, **kwargs)

    @classmethod
    def get_data(cls):
        # return dict([(d['id'], d)
        #              for d in cls._get_values(['id', 'name',  'template',
        #                                        'category', 'category__pid', 'node',
        #                                        'node__map_id', 'authorized_person', 'address',
        #                                        'phone', 'gsm', 'email',
        #                                        'logo', 'background', 'pid', 'llogo'], ['description'])]) or {'none': True}
        places = cls._get_values(['id', 'name', 'template', 'category', 'category__pid', 'node',
                                  'node__map_id', 'authorized_person', 'address',
                                  'phone', 'gsm', 'email',
                                  'logo', 'background', 'pid', 'llogo'], ['description'])
        for s in places:
            s['place_id'] = s['id']
            s['id'] = s['pid']
            s['category_id'] = s['category']
            s['category'] = s['category__pid']
            del s['pid']
            s['logo'] = imgclean(s['logo'])
            s['llogo'] = imgclean(s['llogo'])
            # images.append(s['llogo'])
        return places or {'none': True}


NODE_TYPES = (
    (1, _("Store")),
    (10, _("Booth")),
    (12, _("Conferance Hall")),
    (20, _("Restaurant")),
    (30, _("WC")),
    (40, _("Junction")),
    (50, _("Gate")),
    (60, _("Parking Lot")),
)


class Node(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that holds this node\'s data'))
    map = models.ForeignKey("Map", help_text=_('The map where this node appears'))
    type = models.SmallIntegerField(_('Type'), choices=NODE_TYPES, help_text=_('Type of the node'))
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True, default='',
                            help_text=_('Name of the node'))
    #    logo = models.ImageField(_("T logo"), upload_to="uploads", null=True, blank=True)
    nbhds = models.ManyToManyField('self', verbose_name="Neighbourhood", symmetrical=False, through='Matrix',
                                   help_text=_('Neighbours of the node'))
    x = models.IntegerField('X Coordinate', default=0, help_text=_('X coordinate of the node on the map'))
    y = models.IntegerField('Y Coordinate', default=0, help_text=_('Y coordinate of the node on the map'))

    def __unicode__(self):
        return "%s %s #%s" % (self.name, self.get_type_display(), self.id)

    def get_node_matrix(self):
        return dict(self.nbhds.values_list('to__node2', 'to__distance'))


#    def get_nodes(self):
#        return {self.id : dict(self.nbhds.values_list('to__node2', 'to__distance'))}
#        self.nlist =  '"%s": [%s, "%s", %s, %s, %s]' % (self.id, dumps(dict(vlist)), self.name, self.x, self.y, self.map_id) if vlist  else ""
#        return self.vlist

#function AngleCalc(y,x){return Math.atan2(y,x) * 180/Math.PI}

class Map(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that holds this map data'))
    order = models.SmallIntegerField(_('Sort'), default=1, help_text=_('Order of the map'))
    offset = models.IntegerField(_('Target offset'), default=100, help_text=_('Target offset on the map'))
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True, default='',
                            help_text=_('Name of the map'))
    map = models.ImageField(_("Map file"), upload_to="uploads", null=True, blank=True, help_text=_('Image of the map'))
    qrcode = models.OneToOneField(QRcode, null=True, blank=True)

    QRTYPE = 'm'
    def __unicode__(self):
        return "%s #%s" % (self.name, self.id)

    def edit_nodes(self):
        return "<a href='/edit_nodes/%s/%s' class='edit_nodes'>%s</a>" % (
            self.app_id, self.id, ugettext("Node'lari Duzenle"))

    edit_nodes.allow_tags = True

    def save(self, *args, **kwargs):
        super(Map, self).save(*args, **kwargs)
        customThumbnailer(self.map, [(self.map.width / 2, self.map.height / 2, 's')])


class Matrix(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that holds this matrix data'))
    node1 = models.ForeignKey(Node, related_name='frm', help_text=_('The node where this matrix starts from'))
    node2 = models.ForeignKey(Node, related_name='to', help_text=_('The node where this matrix ends'))
    distance = models.PositiveIntegerField(_('Distance'), help_text=_('The distance between selected two nodes'))

    def save(self, *args, **kwargs):
        recurs = kwargs.pop('recurs', True)
        super(Matrix, self).save(*args, **kwargs)
        if recurs:
            mx, new = Matrix.objects.get_or_create(app_id=self.app_id, node1=self.node2, node2=self.node1,
                                                   defaults={'distance': self.distance})
            if not new:
                mx.distance = self.distance
                mx.save(recurs=False)


class Profile(models.Model):
    """user profile"""

    #    app = models.ForeignKey(Application, verbose_name=_('Application'))
    user = models.OneToOneField(User, unique=True, help_text=_('The user that is associated with this profile'))
    node = models.ForeignKey(Node, null=True, blank=True, help_text=_('The node that presents this profile on the map'))
    root = models.BooleanField(_('Is super user'), default=False, help_text=_('Is this profile\'s owner a superuser?'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    apps = models.ManyToManyField(Application, help_text=_('The applications which this profile is in'))

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        unique_together = ('user', 'node')
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.user,)

#
#    def save(self, *args, **kwargs):
#        super(Profile, self).save(*args, **kwargs)
#        kes(self.STOREID_CACHEKEY % self.user.username).delete()


#    STOREID_CACHEKEY = 'GSTRID%s'
#    #FIXME: cache key should be invalidated on Profile.save()
#    @classmethod
#    def _get_placeid_by_username(cls, username, cache):
#        """
#        @param cls: class instance
#        @param username: String
#        @param cache:kes object
#        @return:integer, currently logged in users Place id if exists, "0" othervise
#
#        gets the id from db and places in cache backend
#        """
#        l = cls.objects.filter(user__username=username).values_list('place', flat=True)
#        return cache.set(l[0]) if l else 0
#
#
#    @classmethod
#    def get_placeid_by_username(cls, username):
#        """
#        @param cls: class instance
#        @param username: String
#        @return:integer, currently logged in users Place id if exists, "0" othervise
#        Gets the id from cache backend or db
#        """
#        cache = kes(cls.STOREID_CACHEKEY % username)
#        return cache.get(cls._get_placeid_by_username(username, cache))


class Product(models.Model):
    """Ürün bilgilerini tutar"""
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that holds this product\'s info'))
    category = models.ForeignKey('ProductCategory', verbose_name=_("Category"), null=True, blank=True,
                                 help_text=_('Category of the product'))
    store_category = models.ForeignKey('StoreProductCategory', verbose_name=_("Store category"), null=True, blank=True,
                                       help_text=_('Store category of the product'))
    place = models.ForeignKey(Place, verbose_name=_("Store"), help_text=_('The store that sells the product'))
    name = models.CharField(_("Name"), max_length=100, help_text=_('Name of the product'))
    description = models.CharField(_("Description"), max_length=255, null=True, blank=True,
                                   help_text=_('Description of the product'))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, help_text=_('Price of the product'))
    cut_price = models.DecimalField(_("Cut Price"), max_digits=10, decimal_places=2, blank=True, null=True,
                                    help_text=_('Cut price of the product'))
    discount_rate = models.PositiveIntegerField(_("Discount Rate"), max_length=2, blank=True, null=True,
                                                help_text=_('Discount rate of the product'))
    image = models.ImageField(_("Image"), upload_to="uploads", null=True, blank=True,
                              help_text=_('Image of the product'))
    pid = models.CharField(max_length=32, editable=False)
    showcase = models.BooleanField(_('Showcase'), default=False,
                                   help_text=_('Is the product presented on the showcase?'))

    THUMB_PREFIX = 'pr'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (750, 750, 'lrg')]

    class Meta:
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if not self.pid:
            self.pid = hashlib.md5('pr_%s' % self.id).hexdigest()
            super(Product, self).save(*args, **kwargs)


CAMPAIGN_TYPES = (
    (1, "Normal"),
    (20, "Momentary"),
    (30, "Daily"),
    (50, "Game"),
)


class CampaignTranslation(TModel):
    source = models.ForeignKey('Campaign', related_name='translations', help_text=_('Campaign to translate'))
    description = RichTextField(_("Description"), help_text=_('Description of the campaign'))
    #translatable fields here


class Campaign(UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that holds this campaing\'s data'))
    type = models.SmallIntegerField(_('Type'), choices=CAMPAIGN_TYPES, default=1, help_text=_('Type of the campaign'))
    category = models.ForeignKey('ProductCategory', verbose_name=_("Category"), null=True, blank=True,
                                 help_text=_('Category of the campaign'))
    place = models.ForeignKey(Place, verbose_name=_("Store"), help_text=_('The store that has this campaign'))
    product = models.ForeignKey(Product, blank=True, null=True, verbose_name=_("Product"),
                                help_text=_('the product with the campaign'))
    name = models.CharField(_("Name"), max_length=100, help_text=_('Name of the campaign'))
    description = RichTextField(_("Description"), help_text=_('Description of the campaign'))
    start_date = models.DateTimeField(_("Start Date"), help_text=_('Start date of the campaign'))
    end_date = models.DateTimeField(_("End Date"), help_text=_('End date of the campaign'))
    #    momentary_campaign = models.BooleanField(_("Momentary Campaign"), default=False)
    no_text = models.BooleanField(_("Full image banner"), default=False,
                                  help_text=_('If checked, only the banner appears on the campaign\'s details page'))
    stock = models.PositiveIntegerField(_("Stock"), max_length=3, blank=True, null=True,
                                        help_text=_('Stock count which the campaign is limited with'))
    image = models.ImageField(_("Image"), upload_to="uploads", blank=True, null=True,
                              help_text=_('Image of the campaign'))
    thumb_image = models.ImageField(_("Thumbnail image"), upload_to="uploads", blank=True, null=True,
                                    help_text=_('Thumbnail image of the campaign'))
    special_background = models.ImageField(_("Special background"), upload_to="uploads", blank=True, null=True,
                                           help_text=_(
                                               'Special background image for the campaign, especially useful when there '
                                               'is no campaign description entered and full image banner checked'))
    pid = models.CharField(max_length=32, editable=False)

    THUMB_PREFIX = 'cm'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (750, 750, 'lrg')]

    class Meta:
        db_table = "campaigns"
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Campaign, self).save(*args, **kwargs)
        if not self.pid:
            self.pid = hashlib.md5('cm_%s' % self.id).hexdigest()
            super(Campaign, self).save(*args, **kwargs)

    @classmethod
    def get_data(cls):
        campaigns = cls._get_values(['id', 'place', 'category', 'product', 'name',
                                     'category__pid', 'no_text', 'start_date', 'end_date',
                                     'stock', 'type', 'image', 'thumb_image', 'special_background',
                                     'pid', 'place__pid', 'product__pid'], ['description'])
        for c in campaigns:
            c['campaign_id'] = c['id']
            c['id'] = c['pid']
            del c['pid']
            c['category_id'] = c['category']
            c['category'] = c['category__pid']
            c['place_id'] = c['place']
            c['product_id'] = c['product']
            c['place'] = c['place__pid']
            c['product'] = c['product__pid']
            del c['place__pid']
            del c['product__pid']
            c['image'] = imgclean(c['image'])
            c['thumb_image'] = imgclean(c['thumb_image'])
            c['special_background'] = imgclean(c['special_background'])
        return campaigns


class NewsTranslation(TModel):
    source = models.ForeignKey('News', related_name='translations', help_text=_('News to translate'))
    title = models.CharField(_('Title'), max_length=30, help_text=_('Title of the news'))
    summary = models.CharField(_('Summary'), max_length=80, null=True, blank=True, help_text=_('Summary of the news'))
    detail = RichTextField(_('Detail'), help_text=_('Details of the news'))


class News(UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that serves this news'))
    title = models.CharField(_('Title'), max_length=30, help_text=_('Title of the news'))
    summary = models.CharField(_('Summary'), max_length=80, null=True, blank=True, help_text=_('Summary of the news'))
    detail = RichTextField(_('Detail'), help_text=_('Details of the news'))
    image = models.ImageField(_('Image'), upload_to='uploads', blank=True, help_text=_('Image of the news'))
    publish_date = models.DateTimeField(_('Publish date'), default=now, help_text=_('Publish date of the news'))
    timestamp = models.DateTimeField(default=now, editable=False, blank=True)
    sort = models.SmallIntegerField(_('Sort'), default=0, help_text=_('Order of the news'))
    qrcode = models.OneToOneField(QRcode, null=True, blank=True)

    QRTYPE = 'n'
    THUMB_PREFIX = 'nw'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (750, 750, 'lrg')]

    @classmethod
    def get_data(cls):
        return dict([(d['id'], d)
                     for d in cls._get_values(['id', 'image', 'timestamp'], ['title', 'detail', 'summary'])]) or {
                   'none': True}

    class Meta:
        ordering = ['sort', 'timestamp']
        verbose_name = _('News Entry')
        verbose_name_plural = _('News Entries')

    def __unicode__(self):
        return self.title


class PageTranslation(TModel):
    source = models.ForeignKey('Page', related_name='translations', help_text=_('The page to translate'))
    title = models.CharField(_('Title'), max_length=30, help_text=_('Title of the page'))
    summary = models.CharField(_('Summary'), max_length=80, null=True, blank=True, help_text=_('Summary of the page'))
    detail = RichTextField(_('Detail'), help_text=_('Details of the page'))


class Page(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that hold this page\'s data'))
    title = models.CharField(_('Title'), max_length=30, help_text=_('Title of the page'))
    summary = models.CharField(_('Summary'), max_length=80, null=True, blank=True, help_text=_('Summary of the page'))
    detail = RichTextField(_('Detail'), help_text=_('Details of the page'))
    image = models.ImageField(_('Image'), upload_to='uploads', blank=True, help_text=_('Image of the page'))
    timestamp = models.DateTimeField(_('zamanpulu'), auto_now_add=True)
    sort = models.SmallIntegerField(_('Sort'), default=0, help_text=_('Order of the page'))
    qrcode = models.OneToOneField(QRcode, null=True, blank=True)

    QRTYPE = 'pg'
    THUMB_PREFIX = 'pg'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (750, 750, 'lrg')]

    class Meta:
        ordering = ['sort']
        verbose_name = _('Simple Page')
        verbose_name_plural = _('Simple pages')

    def __unicode__(self):
        return self.title


class AppLang(models.Model):
    """
    belgelendirme eksik !!!!!!!!
    """
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that has this language'))
    pul = models.DateTimeField(auto_now_add=True)
    main = models.BooleanField(_('Main language'), default=False, help_text=_('Main language of the application'))
    code = models.CharField(_(u"Language"), max_length=5, choices=countries.LANGUAGES,
                            help_text=_('Language to use in the application'))

    def __unicode__(self):
        return self.get_code_display()

    class Meta:
        verbose_name = _(u"Enabled language")
        verbose_name_plural = _(u"Enabled languages")
        unique_together = (("app", "code"),)


class Content(MPTTModel, UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that holds this content data'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children',
                            help_text=_('Parent content of this content'))
    title = models.CharField(_('Title'), max_length=30, help_text=_('Title of the content'))
    # menu_title = models.CharField(_("Menu title"), max_length=255, blank=True, null=True,
    #                               help_text=_('Menu title of the content'))
    summary = models.CharField(_('Summary'), max_length=80, null=True, blank=True,
                               help_text=_('Summary of the content'))
    detail = RichTextField(_('Detail'), help_text=_('Details of the content'))
    image = models.ImageField(_('Image'), upload_to='uploads', blank=True, null=True,
                              help_text=_('Image of the content'))
    # icon = models.ForeignKey('Icon', verbose_name=_('Icon'), null=True, blank=True, help_text=_('Icon of the content'))
    # custom_icon = models.ImageField(_('Custom icon'), upload_to='uploads', blank=True, null=True,
    #                                 help_text=_('Custom icon of the content'))
    main = models.BooleanField(_('Main Menu Item'), default=False,
                               help_text=_('Check this box if you want to use this item as a main menu entry.'))
    active = models.BooleanField(_("Publish"), default=True,
                                 help_text=_('Only published contents will be pushed to the app.'))
    publish_date = models.DateTimeField(_('Publish date'), default=now, help_text=_('When the content is published'))
    timestamp = models.DateTimeField(default=now, editable=False, blank=True)
    sort = models.SmallIntegerField(_('Sort'), default=0, help_text=_('Order of the content'))
    module_selection = models.ForeignKey(ModuleSelection, editable=False, null=True, blank=True)

    THUMB_PREFIX = 'cng'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (750, 750, 'lrg')]

    def make_main(self):
        if self.main:
            if not self.module_selection:
                module = Module.objects.filter(codename='Cms')[0]
                xtra = json.dumps({'oid': self.id})
                icon = Icon.objects.filter(keywords__startswith='placeholder')
                icon = icon[0] if icon else None
                self.module_selection = ModuleSelection.objects.create(module=module, app=self.app, icon=icon,
                                                                       title=self.title, xtra=xtra)
                self.save()
            else:
                self.module_selection.active = self.active
                self.module_selection.save()
        elif self.module_selection:
            ms = self.module_selection
            self.module_selection = None
            self.save()
            ms.delete()



    def get_icon(self):
        if self.custom_icon:
            return self.custom_icon.name
        elif self.icon:
            return self.icon.getFileName()
        else:
            return ''

    @classmethod
    def get_data(cls):
        data = dict([(d['id'], d)
                     for d in cls._get_values(['id', 'image', 'parent', 'publish_date', 'sort'],
                                              ['title', 'detail', 'summary'])])
        if data:
            for cid in data.keys():
                data[cid]['children'] = list(cls.abjects.filter(parent_id=cid).values_list('id', flat=True))
        else:
            data = {'none': True}

        return data
    #
    @classmethod
    def get_child_data(cls):
        tpl = Template("""
        {%load mptt_tags%}
        [{% recursetree nodes %}
        {
            "id": "{{ node.id }}",
            "children": [{{ children }}]
        },{% endrecursetree %}]
        """)
        return tpl.render(Context({'nodes': Content.abjects.all()})).replace(',]', ']')

    class Meta:
        ordering = ['sort']
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def __unicode__(self):
        return self.title


class ContentTranslation(TModel):
    source = models.ForeignKey(Content, related_name='translations', help_text=_('Content to translate'))
    title = models.CharField(_("Title"), max_length=255, help_text=_('Title of the content'))
    # menu_title = models.CharField(_("Menu title"), max_length=255, blank=True, null=True,
    #                               help_text=_('Menu title of the content'))
    summary = models.CharField(_('Summary'), max_length=80, null=True, blank=True,
                               help_text=_('Summary of the content'))
    detail = RichTextField(_('Detail'), help_text=_('Details of the content'))


    # class Meta(TModel.Meta):
    #     verbose_name = _('Page Translation')
    #     verbose_name_plural = _('Page Translations')
    #
    # def __unicode__(self):
    #     return self.title or self.source.title
    #
    #


#
#class Activity(models.Model):
#    app = models.ForeignKey(Application, verbose_name=_('Application'))
#    name = models.CharField(_('Name'), max_length=30)
#    description = RichTextField(_('Description'))
#    start_date = models.DateField(_('Start Date'))
#    end_date = models.DateField(_('End Date'))
#    image = models.ImageField(_('Image'), upload_to='uploads', blank=True)
#    pid = models.CharField(max_length=32, editable=False)
#
#    class Meta:
#        db_table = 'activities'
#        verbose_name = _('Activity')
#        verbose_name_plural = _('Activities')
#
#
#    @classmethod
#    def get_thumbs(cls, name):
#        name = re.sub(r'(.*)/(.*)', r'\2', name)
#        l = []
#        for x, y, z in ACTV_THUMB_SIZES:
#            l.append("%s_%s" % (z, name.replace('jpeg', 'jpg')))
#        return l
#
#


class Version(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'))
    current_version = models.DecimalField(_('Current Version'), decimal_places=2, max_digits=8, default='0.0')
    pid = models.CharField(max_length=32, editable=False)

    class Meta:
        db_table = "version"

    def __unicode__(self):
        return unicode(self.current_version)

    def save(self, *args, **kwargs):
        super(Version, self).save(*args, **kwargs)
        self.pid = hashlib.md5('vn_%s' % self.id).hexdigest()
        super(Version, self).save(*args, **kwargs)


class Customer(models.Model):
    """musteri kayitlari"""

    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that holds this customer record'))
    name = models.CharField(_('İsim'), max_length=100, help_text=_('Name of the customer'))
    mail = models.CharField(_('E-posta'), max_length=150, help_text=_('E-mail of the customer'))
    mobile = models.CharField(_('Telefon'), max_length=20,
                              help_text=_('Mobile phone number of the customer (0XXX XXX XX XX)'))
    address = models.CharField(_('Adres'), max_length=150, help_text=_('Address of the customer'))
    timestamp = models.DateTimeField(_('zamanpulu'), auto_now_add=True)

    class Meta:
    #        app_label = 'auth'
    #        db_table = 'place_customer'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __unicode__(self):
        return '%s [Tel: %s]' % (self.name, self.mobile)


FEEDBACK_TYPE = (
    (1, 'Teşekkür'),
    (2, 'Öneri'),
    (3, 'Şikayet'),
)
TYPECSSCLASS = {
    1: 'tesekkur',
    2: 'oneri',
    3: 'sikayet'
}


class Feedback(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that stores this feedback'))
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'), help_text=_('Sender of the feedback'))
    place = models.ForeignKey(Place, verbose_name=_('Store'), null=True, blank=True,
                              help_text=_('The store which the feedback is about'))
    type = models.SmallIntegerField(_('Tip'), choices=FEEDBACK_TYPE, help_text=_('Type of the feedback'))
    msg = RichTextField(_('Customer\'s Message'), max_length=30, help_text=_('Customer\'s ideas'))
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(editable=False, null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    date = models.DateTimeField(_('Tarih'), auto_now_add=True, help_text=_('The date when the feedback is sent'))
    forhost = models.BooleanField(_('General Feedback'), default=False, help_text=_('Is it a general feedback'))
    called = models.BooleanField(_('Called back?'), default=False, help_text=_('Called back the customer?'))
    archived = models.BooleanField(_('Archived?'), default=False, help_text=_('Archived the feedback?'))
    notes = RichTextField(_('Notes about the meeting'), null=True, blank=True,
                          help_text=_('Notes about the meeting with the customer'))

    class Meta:
    #        db_table = 'activities'
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

    def __unicode__(self):
        return unicode(self.date)

    def typecss(self):
        return TYPECSSCLASS[self.type]


CHART_TYPE = (
    (10, 'FastFood'),
    (20, 'Mobile Shopping'),

)

CART_STATUS = (
    (10, _('Received')),
    (20, _('Processing')),
    (30, _('Preparing')),
    (40, _('Ready')),
    (50, _('Shipped')),
    (60, _('Delivered')),
)


class BaseOrder(models.Model):
    """siparis"""

    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that has this order'))
    type = models.SmallIntegerField(_('Type'), choices=CHART_TYPE, default=10, help_text=_('Type of the order'))
    status = models.SmallIntegerField(_('Status'), choices=CART_STATUS, default=10, help_text=_('Status of the order'))
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'), help_text=_('Owner of the order'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    ptime = models.DateTimeField(_('Completion time'), null=True, blank=True,
                                 help_text=_('The date when the order is completed'))
    total_price = models.DecimalField(_('Total price'), decimal_places=2, max_digits=9, null=True, blank=True,
                                      help_text=_('Total price of the order'))

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __unicode__(self):
        return '%s' % (self.id,)

    def calculateTotal(self):
        self.total_price = self.orderitem_set.aggregate(Sum('line_total'))['line_total__sum']
        self.save()

    def createStoreOrders(self):
        storeorder_cache = {}
        for item in self.orderitem_set.all():
            if not storeorder_cache.get(item.place_id):
                storeorder_cache[item.place_id], new = item.place.storeorder_set.get_or_create(baseorder=self,
                                                                                               customer=self.customer)
            storeorder_cache[item.place_id].orderitem_set.add(item)
        for storeorder in storeorder_cache.values():
            storeorder.calculateTotal()

        self.save()


class StoreOrder(models.Model):
    """siparis"""

    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that has this store order'))
    ept = models.SmallIntegerField(_('Estimated preparation time'), help_text="(minutes)", null=True, blank=True)
    status = models.SmallIntegerField(_('Status'), choices=CART_STATUS, default=10, help_text=_('Status of the order'))
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'), help_text=_('Owner of the order'))
    baseorder = models.ForeignKey(BaseOrder, verbose_name=_('Base order'), help_text=_('Base order item'))
    place = models.ForeignKey(Place, verbose_name=_('Store'), help_text=_('The store that order is given from'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    ptime = models.DateTimeField(_('Preparation time'), null=True, blank=True,
                                 help_text=_('The date when the order is prepared'))
    total_price = models.DecimalField(_('Total price'), decimal_places=2, max_digits=9, null=True, blank=True,
                                      help_text=_('Total price of the order'))

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Store Order')
        verbose_name_plural = _('Store Orders')

    def __unicode__(self):
        return '%s' % (self.id,)

    def calculateTotal(self):
        self.total_price = self.orderitem_set.aggregate(Sum('line_total'))['line_total__sum']
        self.save()


class OrderItem(models.Model):
    """siparis"""

    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that has this order item'))
    storeorder = models.ForeignKey(StoreOrder, verbose_name=_('Chart'), null=True, blank=True,
                                   help_text=_('Chart of the order item'))
    baseorder = models.ForeignKey(BaseOrder, verbose_name=_('Chart'), help_text=_('Chart of the order item'))
    place = models.ForeignKey(Place, verbose_name=_('Store'), help_text=_('The store where this item is ordered from'))
    product = models.ForeignKey(Product, verbose_name=_('Product'), help_text=_('The product that is ordered'))
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=7, help_text=_('Price of the item'))
    qty = models.IntegerField(_('Quantity'), default=1, help_text=_('Quantity of the order item'))
    line_total = models.DecimalField(_('Line total'), decimal_places=2, max_digits=7,
                                     help_text=_('Line total of the order item'))

    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __unicode__(self):
        return '%s' % (self.id,)

    def save(self, *args, **kwargs):
    #        super(OrderItem, self).save(*args, **kwargs)
        if not self.line_total:
            self.price = self.product.cut_price or self.product.price
            self.line_total = self.price * self.qty
            self.place = self.product.place
        super(OrderItem, self).save(*args, **kwargs)


class Elog(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that this client error occurred'))
    msg = models.CharField(_('Name'), max_length=30, help_text=_('Name of the error'))
    date = models.DateTimeField(_('Date'), auto_now_add=True)

    class Meta:
    #        db_table = 'activities'
        verbose_name = _('Client Error')
        verbose_name_plural = _('Client Errors')

    def __unicode__(self):
        return self.date


class SpeakerTranslation(TModel):
    source = models.ForeignKey('Speaker', related_name='translations')
    profile = RichTextField(_('Profile'), null=True, blank=True, help_text=_('Profile of the speaker'))


class Speaker(UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that presents this speaker'))
    firstname = models.CharField(_('First Name'), max_length=30, help_text=_('First name of the speaker'))
    lastname = models.CharField(_('Last Name'), max_length=30, help_text=_('Last name of the speaker'))
    company = models.CharField(_('Company / Organization'), max_length=70, null=True, blank=True,
                               help_text=_('Company of the speaker'))
    position = models.CharField(_('Position'), max_length=50, null=True, blank=True,
                                help_text=_('Position of the speaker'))
    profile = RichTextField(_('Profile'), null=True, blank=True, help_text=_('Profile of the speaker'))
    photo = models.ImageField(_("Photo"), upload_to="uploads", null=True, blank=True,
                              help_text=_('Photo of the speaker'))
    qrcode = models.OneToOneField(QRcode, null=True, blank=True)

    QRTYPE = 's'
    THUMB_PREFIX = 'per'
    THUMB_FIELDS = ['photo']
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's')]

    class Meta:
        db_table = 'speaker'
        verbose_name = _('Speaker')
        verbose_name_plural = _('Speakers')

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)

    @classmethod
    def get_data(cls):
        speakers = dict([(s['id'], s) for s in
                         Speaker._get_values(['id', 'firstname', 'lastname', 'position', 'company', 'photo'],
                                             ['profile'])]) or {'none': True}
        return speakers


class DelegateTranslation(TModel):
    source = models.ForeignKey('Delegate', related_name='translations')
    profile = RichTextField(_('Profile'), help_text=_('Profile of the delegate'))


class Delegate(UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application which presents this delegate'))
    firstname = models.CharField(_('First Name'), max_length=30, help_text=_('First name of the delegate'))
    lastname = models.CharField(_('Last Name'), max_length=30, help_text=_('Last name of the delegate'))
    company = models.CharField(_('Company / Organization'), max_length=30, null=True, blank=True,
                               help_text=_('Company of the delegate'))
    position = models.CharField(_('Position'), max_length=30, null=True, blank=True,
                                help_text=_('Position of the delegate'))
    profile = RichTextField(_('Profile'), help_text=_('Profile of the delegate'))
    photo = models.ImageField(_("Photo"), upload_to="uploads", null=True, blank=True,
                              help_text=_('Photo of the delegate'))

    THUMB_PREFIX = 'dlg'
    THUMB_FIELDS = ['photo']
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's')]

    class Meta:
        db_table = 'delegate'
        verbose_name = _('Delegate')
        verbose_name_plural = _('Delegates')

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)

    @classmethod
    def get_data(cls):
        delegates = dict([(d['id'], d) for d in
                          Delegate._get_values(['id', 'firstname', 'lastname', 'company', 'position', 'photo'],
                                               ['profile'])]) or {'none': True}
        return delegates


class Photo(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that has this photo'))
    title = models.CharField(_('Title'), max_length=30, help_text=_('Title of the photo'))
    sort = models.SmallIntegerField(_('Sort'), default=0, help_text=_('Order of the photo'))
    photo = models.ImageField(_("Photo"), upload_to="uploads", help_text=_('Photo to upload'))

    THUMB_PREFIX = 'gl'
    THUMB_FIELDS = ['photo']
    THUMB_SIZES = [(100, 100, 's'), (150, 150, 'n')]

    class Meta:
        ordering = ['sort', 'id']
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    def __unicode__(self):
        return self.title


class ExhibitorTranslation(TModel):
    source = models.ForeignKey('Exhibitor', related_name='translations')
    company = models.CharField(_('Company'), max_length=30)
    profile = RichTextField(_('Profile'))


class Exhibitor(UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'), blank=True,
                            help_text=_('The application which presents this exhibitor'))
    company = models.CharField(_('Company / Organization'), max_length=80, help_text=_('Company of the exhibitor'))
    profile = RichTextField(_('Profile'), help_text=_('Profile of the exhibitor'))
    phone = models.CharField(_("Phone"), max_length=15, null=True, blank=True, default='',
                             help_text=_('Phone number of the exhibitor (0XXX XXX XX XX)'))
    email = models.EmailField(_("Email"), null=True, blank=True, default='', help_text=_('E-mail of the exhibitor'))
    logo = models.ImageField(_("Detail logo"), upload_to="uploads", blank=True, null=True,
                             help_text=_('Logo for the exhibitor'))
    node = models.OneToOneField('Node', null=True, blank=True, help_text=_('The node where this exhibitor will be'))
    qrcode = models.OneToOneField(QRcode, null=True, blank=True)

    THUMB_PREFIX = 'exh'
    THUMB_FIELDS = ['logo']
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (480, 480, 'l')]
    QRTYPE = 'x'

    class Meta:
        db_table = 'exhibitor'
        verbose_name = _('Exhibitor')
        verbose_name_plural = _('Exhibitors')

    def __unicode__(self):
        return self.company

    @classmethod
    def get_data(cls):
        exhibitors = {}
        node2exh = {}
        for e in cls._get_values(['id', 'phone', 'email', 'logo', 'node', 'node__map_id'], ['company', 'profile']):
            node2exh[e['node']] = e['id']
            exhibitors[e['id']] = e
            exhibitors[e['id']]['files'] = list(
                ExhibitorFiles.objects.filter(exhibitor__id=e['id']).values_list('id', flat=True))
        if not exhibitors:
            exhibitors = {'none': True}
        return exhibitors, node2exh


class ExhibitorFilesTranslation(TModel):
    source = models.ForeignKey('ExhibitorFiles', related_name='translations')
    title = models.CharField(_('title'), max_length=60)


class ExhibitorFiles(UModel):
    """Exhibitor Documents"""

    app = models.ForeignKey(Application, verbose_name=_('Application'), blank=True,
                            help_text=_('The application which this exhibitor file belongs to'))
    title = models.CharField(_('Title'), max_length=60, help_text=_('Name of the file'))
    exhibitor = models.ForeignKey(Exhibitor, verbose_name=_('Exhibitor'),
                                  help_text=_('The exhibitor who owns this file'))
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    file = models.FileField(_("File"), upload_to="uploads", help_text=_('File to upload'))

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.title,)

    @classmethod
    def get_data(cls):
        exhibitorfiles = {}
        for s in cls._get_values(['id', 'file'], ['title']):
            exhibitorfiles[s['id']] = s
            exhibitorfiles[s['id']]['icon'] = s['file'].split('.')[-1].replace('jpeg', 'jpg')
        return exhibitorfiles

    def save(self, *args, **kwargs):
        if not self.id:
            self.app = self.exhibitor.app
        super(ExhibitorFiles, self).save(*args, **kwargs)


class EventTranslation(TModel):
    source = models.ForeignKey('Event', related_name='translations')
    title = models.CharField(_('Title'), max_length=30)
    description = RichTextField(_('Description'))


class Event(UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application this event belongs to'))
    title = models.CharField(_('Name'), max_length=30, help_text=_('Title of the event'))
    date = models.DateField(_('Date'), help_text=_('The date that this event takes place'))
    description = RichTextField(_('Description'), help_text=_('Description about the event'))
    speakers = models.ManyToManyField(Speaker, null=True, blank=True,
                                      help_text=_('The speakers that attends to this event'))
    start = models.TimeField(_('Start'), null=True, blank=True, help_text=_('The time when this event starts'))
    end = models.TimeField(_('End'), null=True, blank=True, help_text=_('The time when this event ends'))
    image = models.ImageField(_("Event image"), upload_to="uploads", blank=True, null=True,
                              help_text=_('Image of the event'))
    location = models.CharField(_('Location'), max_length=30, null=True, blank=True,
                                help_text=_('The place where this event takes place'))
    node = models.ForeignKey('Node', null=True, blank=True, help_text=_('The node where this event is'))
    qrcode = models.OneToOneField(QRcode, null=True, blank=True)

    THUMB_PREFIX = 'evnt'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (480, 480, 'l')]
    QRTYPE = 'e'

    @classmethod
    def get_data(cls):
        events = cls._get_values(['id', 'date', 'start', 'end', 'image', 'location', 'node'], ['title', 'description'])
        if events:
            for a in events:
                a['speakers'] = list(Speaker.objects.filter(event__id=a['id']).values_list('id', flat=True))
            events = regroupEvents(events)
        return events

    class Meta:
        db_table = 'event'
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __unicode__(self):
        return self.title


class SponsorType(models.Model):
    """SponsorType"""
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application this sponsor type belongs to'))
    title = models.CharField(_('Title'), max_length=40, help_text=_('Title of the sponsor type'))
    sort = models.SmallIntegerField(_('Sort'), default=0, help_text=_('Order of the sponsor type while listing'))
    #    image = models.ImageField(_("Icon/image"), upload_to="uploads", blank=True, null=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['sort']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.title,)


class Sponsor(models.Model):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application this sponsor belongs to'))
    type = models.ForeignKey(SponsorType, verbose_name=_('Type'), help_text=_('Type of the sponsor'))
    company = models.CharField(_('Company / Organization'), max_length=80, help_text=_('Company of the sponsor'))
    profile = RichTextField(_('Profile'), help_text=_('Profile of the sponsor'))
    phone = models.CharField(_("Phone"), max_length=15, null=True, blank=True, default='',
                             help_text=_('Phone number (0XXX XXX XX XX)'))
    email = models.EmailField(_("Email"), null=True, blank=True, default='', help_text=_('E-mail of the sponsor'))
    logo = models.ImageField(_("Detail logo"), upload_to="uploads", blank=True, null=True,
                             help_text=_('Logo of the sponsor'))
    qrcode = models.OneToOneField(QRcode, null=True, blank=True)

    QRTYPE = 'p'
    THUMB_PREFIX = 'spn'
    THUMB_FIELDS = ['logo']
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (480, 480, 'l')]

    class Meta:
        verbose_name = _('Sponsor')
        verbose_name_plural = _('Sponsors')

    def __unicode__(self):
        return self.company


class MenuCategoryTranslation(models.Model):
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True, help_text=_('Name of the menu category'))
    source = models.ForeignKey('MenuCategory', related_name='translations', help_text=_('Menu category to translate'))


class MenuItemTranslation(models.Model):
    # app = models.ForeignKey(Application)
    source = models.ForeignKey('MenuItem', related_name='translations', help_text=_('Menu item to translate'))

    name = models.CharField(_("Name"), max_length=100, help_text=_('Name of the menu item'))
    description = RichTextField(_("Description"), null=True, blank=True, help_text=_('Description of the menu item'))


class MenuItem(UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'), editable=False,
                            help_text=_('The application that you\'ll add a menu item to'))
    category = models.ForeignKey('MenuCategory', verbose_name=_("Category"), help_text=_('Category of the menu item'))
    name = models.CharField(_("Name"), max_length=100, help_text=_('Name of the menu item'))
    image = models.ImageField(_("Image"), upload_to="uploads", null=True, blank=True,
                              help_text=_('Image of the menu item'))
    description = RichTextField(_("Description"), null=True, blank=True, help_text=_('Description of the menu item'))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, null=True, blank=True,
                                help_text=_('Price of the menu item'))
    cut_price = models.DecimalField(_("Cut Price"), max_digits=10, decimal_places=2, blank=True, null=True,
                                    help_text=_('Cut price of the menu item'))
    showcase = models.BooleanField(_('Showcase'), default=False,
                                   help_text=_('If checked, this menu item will appear on the showcase'))
    prepare_time = models.SmallIntegerField(_('Preparation time'), null=True, blank=True,
                                            help_text=_('As seconds. Enter an integer between 1 - 255'))
    sort = models.SmallIntegerField(_('Sort'), default=1, null=True, blank=True, help_text=_('Sort of the menu item'))

    THUMB_PREFIX = 'mi'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (480, 480, 'lrg'), (750, 750, 'xlrg')]

    def save(self, *args, **kwargs):
        if not self.id:
            self.app = self.category.app
        super(MenuItem, self).save(*args, **kwargs)

    class Meta:
        ordering = ["category", "sort"]
        verbose_name = _("Menu item")
        verbose_name_plural = _("Menu items")

    def __unicode__(self):
        return self.name

    @classmethod
    def get_data(cls):
        return dict([(s['id'], s) for s in cls._get_values(['id', 'price', 'cut_price', 'image', 'showcase'],
                                                           ['name', 'description'])])


class MenuCategory(UModel):
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that you\'ll add a menu category to'))
    name = models.CharField(_("Name"), max_length=50, null=True, blank=True, help_text=_('Name of the menu category'))
    image = models.ImageField(_("Image"), upload_to="uploads", null=True, blank=True,
                              help_text=_('Image of the menu category'))
    sort = models.SmallIntegerField(_('Sort'), default=1, null=True, blank=True,
                                    help_text=_('Order of the menu category'))
    # parent_category = models.ForeignKey("self", blank=True, null=True, verbose_name=_("Parent Category"))

    THUMB_PREFIX = 'mc'
    THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (480, 480, 'lrg'), (750, 750, 'xlrg')]

    @classmethod
    def get_data(cls):
        menu_categories = cls._get_values(['id', 'image'], ['name'])
        for st in menu_categories:
            st['items'] = list(MenuItem.abjects.filter(category=st['id']).values_list('id', flat=True))
        return menu_categories

    class Meta:
        ordering = ["sort"]
        verbose_name = _("Menu category")
        verbose_name_plural = _("Menu categories")

    def __unicode__(self):
        return self.name


DEFAULT_THUMB_FIELDS = ['image']
DEFAULT_THUMB_SIZES = [(60, 60, 'xs'), (80, 80, 's'), (750, 750, 'lrg')]


def createThumbnails(instance):
    if getattr(instance, 'THUMB_PREFIX', None):
        image_fields = getattr(instance, 'THUMB_FIELDS', DEFAULT_THUMB_FIELDS)
        thumb_sizes = getattr(instance, 'THUMB_SIZES', DEFAULT_THUMB_SIZES)
        for img in image_fields:
            customThumbnailer(getattr(instance, img), thumb_sizes, prefix=instance.THUMB_PREFIX)


# noinspection PyUnusedLocal
def update_version(sender, instance, created=True, **kwargs):
    createThumbnails(instance)
    Version.objects.filter(app=instance.app).update(current_version=F('current_version') + 0.01)


# noinspection PyUnusedLocal
def update_app_version(sender, instance, created=True, **kwargs):
    Version.objects.filter(app=instance).update(current_version=F('current_version') + 0.01)


# noinspection PyUnusedLocal
def update_themed_apps(sender, instance, created=True, **kwargs):
    for app in instance.application_set.all():
        Version.objects.filter(app=app).update(current_version=F('current_version') + 0.01)


signals.post_save.connect(update_app_version, sender=Application)

signals.post_save.connect(update_themed_apps, sender=Theme)

for m in (Product, ProductCategory, Campaign, Place, Speaker, Delegate, Exhibitor, Sponsor, SponsorType, Event, News,
          Page, Photo, Map, Node, Matrix, StoreProductCategory, MenuCategory, MenuItem):
    signals.post_save.connect(update_version, sender=m)
    signals.post_delete.connect(update_version, sender=m)


def generate_qrcode(sender, instance, created=True, **kwargs):
    if not instance.qrcode:
        url = "http://%s.uygulamatik.com/#QR%s-%s" % (instance.app.subdomain, instance.QRTYPE, instance.id)
        instance.qrcode = QRcode.objects.create(url=url)
        instance.save()


for m in (Speaker, Exhibitor, Sponsor, Event, News, Page, Map):
    signals.post_save.connect(generate_qrcode, sender=m)
