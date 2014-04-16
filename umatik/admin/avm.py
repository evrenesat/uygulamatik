#-*- coding:utf-8 -*-
# __author__ = 'Evren Esat Ozkan'
from django.contrib import admin
from django.db.models import Q
from admin_tabs.helpers import TabbedPageConfig, Config
from umatik.models import *
from django.utils.translation import ugettext_lazy as _
from modmin import Modmin
from modmin import LanguagesInline, TransConfig


class PlacePageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        place = Config(fields=["app", "category", "name", "template", "node"])
        details = Config(fields=["description", "authorized_person", "address", "phone", "gsm", "email"])
        logos = Config(fields=["logo", "llogo", "background"])
        products = Config(inline="ProductInline")

    class ColsConfig:
        place = Config(fieldsets=["place"], css_classes=["col1"])
        details = Config(fieldsets=["details"], css_classes=["col1"])
        logos = Config(fieldsets=["logos"], css_classes=["logos"])
        products = Config(fieldsets=["products"])

    class TabsConfig:
        main_tab = Config(name="Place", cols=["place"])
        details_tab = Config(name="Details", cols=["details"])
        logos_tab = Config(name="Logos", cols=["logos"])
        products_tab = Config(name="Products", cols=["products"])


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ProductInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'store_category':
            if request._obj_ is not None:
            #                   assert 0, list(field.queryset.all())
                field.queryset = field.queryset.filter(place_id=request._obj_.id)
            #                   assert 0, field.queryset
            else:
                field.queryset = field.queryset.none()

        return field


class ProductCategoryTranslationInline(LanguagesInline):
    model = ProductCategoryTranslation


class ProductCategoryConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=["parent_category", "image", "order", "image", "name"])
        translations = Config(inline="ProductCategoryTranslationInline")


class ProductCategoryAdmin(Modmin):
    list_display = ['id', 'name', 'image', 'order']
    list_editable = ['order']
    search_fields = ['name']

    page_config_class = ProductCategoryConfig
    inlines = [ProductCategoryTranslationInline, ]


class StoreProductCategoryTranslationInline(LanguagesInline):
    model = StoreProductCategoryTranslation


class StoreProductCategoryConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=["place", "order", "name"])
        translations = Config(inline="StoreProductCategoryTranslationInline")


class StoreProductCategoryAdmin(Modmin):
    has_place = True
    # place_exclude = ['place', ]
    page_config_class = StoreProductCategoryConfig
    inlines = [StoreProductCategoryTranslationInline, ]


class CampaignPageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        info = Config(fields=["name", "app", "type", "category", "place", "product"])
        details = Config(fields=["description", "start_date", "end_date", "stock"])
        images = Config(fields=["no_text", "image", "thumb_image", "special_background"])

    class ColsConfig:
        info = Config(fieldsets=["info"], css_classes=["col1"])
        details = Config(fieldsets=["details"], css_classes=["col1"])
        images = Config(fieldsets=["images"], css_classes=["col1"])

    class TabsConfig:
        info_tab = Config(name="Info", cols=["info"])
        details_tab = Config(name="Details", cols=["details"])
        images_tab = Config(name="Images", cols=["images"])


class CampaignTranslationInline(LanguagesInline):
    model = CampaignTranslation


class CampaignConfig(TransConfig):
    class FieldsetsConfig:
        details = Config(fields=["type", "category", "place", "product", "name",
                                 "description", "start_date", "end_date", "no_text",
                                 "stock", "image", "thumb_image", "special_background"])
        translations = Config(inline="CampaignTranslationInline")


class CampaignAdmin(Modmin):
    page_config_class = CampaignPageConfig
    list_display = ['id', 'name', 'product', 'image']
    search_fields = ['name']
    # place_exclude = ['place', ]
    raw_id_fields = ('product', 'place')
    has_place = True
    page_config_class = CampaignConfig
    inlines = [CampaignTranslationInline, ]


class ProductAdmin(Modmin):
    list_display = ['id', 'name', 'store_category', 'price', 'cut_price', 'discount_rate', 'showcase']
    list_filter = ['category', ]
    # super_list_display = ('place',) #TODO: duzenlenecek
    # super_list_filter = ('place',)
    search_fields = ['name', 'image']
    raw_id_fields = ('store_category', 'place')
    place_exclude = ['place', 'category']
    list_per_page = 50
    #    list_editable = ['price', 'cut_price', 'discount_rate', 'showcase']
    has_place = True

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.category_id = Place.objects.filter(pk=obj.place_id).values_list('category', flat=True)[0]
        super(ProductAdmin, self).save_model(request, obj, form, change)

#    def save_model(self, request, obj, form, change):
#        if self.place_exclude and not request.user.is_superuser:
#            obj.place_id = Profile.get_placeid_by_username(request.user.username)
#            obj.category_id = Place.objects.filter(pk=obj.place_id).values_list('category', flat=True)[0]
#        obj.save()


class CustomerAdmin(Modmin):
    has_place = True

    def queryset(self, request):
        qs = super(CustomerAdmin.__base__, self).queryset(request)
        if request.user.is_superuser:
            return qs
        placeid = request.session['placeid']
        return qs.filter(Q(storeorder__place_id=placeid) | Q(feedback__place_id=placeid)).distinct()


class StoreProductCategoryAdmin(Modmin):
    has_place = True
    place_exclude = ['place', ]


class BaseOrderPageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        base_order = Config(fields=["type", "status", "customer", "ptime", "total_price"])
        order_items = Config(inline="OrderItemInline")

    class ColsConfig:
        base_order = Config(fieldsets=["base_order"], css_classes=["col1"])
        order_items = Config(fieldsets=["order_items"], css_classes=["col1"])

    class TabsConfig:
        main_tab = Config(name="Base Order", cols=["base_order"])
        order_items_tab = Config(name="Order Items", cols=["order_items"])


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['baseorder', 'product', 'price', 'qty', 'line_total']
    exclude = ['place']


class BaseOrderAdmin(Modmin):
    page_config_class = BaseOrderPageConfig
    has_place = True
    list_display = ['timestamp', 'customer', 'total_price']
    #    search_fields = ['name', 'image']
    raw_id_fields = ('customer', )
    inlines = [OrderItemInline, ]
    date_hierarchy = 'timestamp'


class StoreOrderPageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        order = Config(fields=["app", "ept", "status", "customer", "baseorder", "place", "ptime", "total_price"])
        order_items = Config(inline="OrderItemInline")

    class ColsConfig:
        order = Config(fieldsets=["order"], css_classes=["col1"])
        order_items = Config(fieldsets=["order_items"], css_classes=["col1"])

    class TabsConfig:
        main_tab = Config(name="Order", cols=["order"])
        order_items_tab = Config(name="Order Items", cols=["order_items"])


class StoreOrderAdmin(Modmin):
    page_config_class = StoreOrderPageConfig
    has_place = True
    list_display = ['timestamp', 'place', 'total_price']
    #    search_fields = ['name', 'image']
    raw_id_fields = ('baseorder', 'place', 'customer')
    inlines = [OrderItemInline, ]
    date_hierarchy = 'timestamp'


class PlaceTranslationInline(LanguagesInline):
    model = PlaceTranslation


class PlaceConfig(TabbedPageConfig):
    class FieldsetsConfig:
        details = Config(fields=['name', 'category', 'email', 'authorized_person', 'template',
                                 'description', 'address', 'phone', 'gsm', 'email', 'logo',
                                 'llogo', 'background'])
        translations = Config(inline="PlaceTranslationInline")
        product = Config(inline="ProductInline")

    class ColsConfig:
        details = Config(fieldsets=["details"])
        product = Config(fieldsets=["product"])
        translations = Config(fieldsets=["translations"])

    class TabsConfig:
        main_tab = Config(name="Details", cols=["details"])
        product_tab = Config(name="Products", cols=["product"])
        translations_tab = Config(name="Translations", cols=["translations"])


class PlaceAdmin(Modmin):
    list_display = ['name', 'category', 'email', 'authorized_person']
    search_fields = ['name']
    page_config_class = PlaceConfig
    inlines = [PlaceTranslationInline, ProductInline]
    list_filter = ['category', ]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(PlaceAdmin, self).get_form(request, obj, **kwargs)
