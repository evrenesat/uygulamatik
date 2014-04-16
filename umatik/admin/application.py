#-*- coding:utf-8 -*-
# __author__ = 'Evren Esat Ozkan'
# from django import forms
# from django.utils.encoding import force_text
# from django.utils.safestring import mark_safe
from django.contrib import admin, messages
from django.forms import models as djfm
from django.http import HttpResponseRedirect, Http404
from admin_tabs.helpers import TabbedPageConfig, Config
from admin_tabs.helpers import TabbedModelAdmin as TMA
from umatik.models import *
from django.utils.translation import ugettext_lazy as _
from modmin import Modmin


class ApplicationPageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        info = Config(fields=["name_short", "name_long", 'company', "subdomain" ], name="Info")
        status = Config(fields=["status"], name="Status")
        contact = Config(fields=['phone', 'fax', 'address', 'street', 'city', 'country', 'lat', 'lon'])
        modules = Config(inline="ModuleSelectionInline")
        languages = Config(inline="AppLangInline", name="languages")
        theme = Config(name="", fields=['theme', ])
        design = Config(name="", fields=['header_type', "header_image", "icon", 'logo_small', 'logo_big',
                                         'background_image', 'app_bg', 'show_qrcode_button',
                                         'splash_image', 'background_color', ])
        super = Config(name="SuperUser", fields=['type', 'active'])

    class ColsConfig:
        info = Config(fieldsets=["info", ], css_classes=["col2"])
        status = Config(fieldsets=["status", ], css_classes=["col2"])
        contact = Config(fieldsets=["contact", ])
        modules = Config(fieldsets=["modules", ])
        languages = Config(fieldsets=["languages", ])
        theme = Config(fieldsets=["theme", ])
        design = Config(fieldsets=["design", ])
        super = Config(fieldsets=["super", ])

    class TabsConfig:
        main_tab = Config(name="Basic Info & Status", cols=["info", "status"])
        modules_tab = Config(name="Modules", cols=["modules"])
        languages_tab = Config(name=_("Languages"), cols=["languages"])
        theme_tab = Config(name="Theme", cols=["theme", ])
        design_tab = Config(name="Design & Options", cols=["design", ])
        contact_tab = Config(name="Contact Info", cols=["contact", ])
        super_tab = Config(name="Super", cols=["super", ])


# class ModuleSelectionInlineFormset(djfm.BaseInlineFormSet):
# #    pass
#     def add_fields(self, form, index):
#         super(ModuleSelectionInlineFormset, self).add_fields(form, index)
#         if form.instance:
#             try:
#                 icons = Icon.objects.filter(module=form.instance.module)
#             except Module.DoesNotExist:
#                 icons = Icon.objects.none()
#             else:
#                 form.fields['icon'].queryset = icons


class ModuleSelectionInline(admin.TabularInline):
    model = ModuleSelection
    extra = 0
    raw_id_fields = ['icon']
    # formset = ModuleSelectionInlineFormset
    # readonly_fields = ['module']
    fields = ['title', 'icon', 'customicon', 'active', 'order']
    radio_fields = {"icon": admin.VERTICAL}


class AppLangAdmin(Modmin):
    pass


class AppLangInline(admin.TabularInline):
    model = AppLang
    extra = 2
    fields = ['code', 'main']
    # formset = AppLangInlineFormset
    # readonly_fields = ['module']
    # radio_fields = {"icon": admin.VERTICAL}


class ApplicationAdmin(TMA):
    page_config_class = ApplicationPageConfig
    change_template = 'admin/umatik/application/change_form.html'
    inlines = (AppLangInline, ModuleSelectionInline, )
    # save_on_top = True
    exclude = []
    # readonly_fields = []
    radio_fields = {"theme": admin.VERTICAL}
    # app_limited_fk = ['lang']
    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     if not self.app_limited_fk:
    #         return super(ApplicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #     field = super(ApplicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #     if not request.user.is_superuser and db_field.name in self.app_limited_fk:
    #         field.queryset = field.queryset.filter(app_id=request.session['appid'])
    #     return field

    def response_change(self, request, obj, post_url_continue=None):
        messages.info(request, _('Application saved successfuly'))
        return HttpResponseRedirect("../%s" % obj.id)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ApplicationAdmin, self).get_readonly_fields(request, obj=None)
        else:
            return 'status'

    def save_model(self, request, obj, form, change):
    #        if not obj.id:
    #            super(ApplicationAdmin, self).save_model(request, obj, form, change)
    #

        super(ApplicationAdmin, self).save_model(request, obj, form, change)
        obj.createModuleSelections()
        if 'name_short' in form.changed_data or not obj.subdomain:
            obj.subdomain = slugify(obj.name_short)
            super(ApplicationAdmin, self).save_model(request, obj, form, change)
        if 'theme' in form.changed_data:
            obj.updateTheme()

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(ApplicationAdmin, self).get_form(request, obj, **kwargs)
    #     secililer = obj.subcats.values_list('id',flat=True) if obj else []
    #     qs = form.base_fields['subcats'].queryset.exclude(
    #         id__in=AnaKategoriler.subcats.through.objects.filter(id__in=secililer).values_list('category', flat=True))
    #     catfilter = int(request.GET.get('catfilter', 2)) # 2:orta kategoriler, 1:ana kategoriler, 3: tum kategoriler
    #     if catfilter == 2:
    #         qs = qs.filter(Q(parent__in=Category.objects.filter(parent__isnull=True).values_list('id', flat=True))|Q(id__in=secililer))
    #     elif catfilter == 1:
    #         qs = qs.filter(Q(parent__isnull=True)|Q(id__in=secililer))
    #     form.base_fields['subcats'].queryset = qs
    #     return form

    def queryset(self, request):
        qs = super(ApplicationAdmin, self).queryset(request)
        if not request.user.is_superuser:
        #            appid = request.session['appid']
        #            placeid = request.session['placeid']
            qs = qs.filter(pk__in=request.user.profile.apps.values_list('id', flat=True), active=True)
        return qs




class ModuleSelectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'app', 'active', 'order']
    list_editable = ['active', 'order']


class IconCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort']
    list_editable = ['sort']


class IconAdmin(admin.ModelAdmin):
    list_display = ('ikon',)
    # filter_horizontal = ("theme",)
    list_filter = ('category','module')

    def change_view(self, request, extra_context=None):
        """
        django adminde "can use" diye bir permission olmadigi icin workaround yaptik.
        """
        if not request.user.is_superuser:
            raise Http404
        return super(IconAdmin, self).change_view(request, extra_context)



class ThemeImageInline(admin.TabularInline):
    model = ThemeImage
    extra = 5
    readonly_fields = ['filename']


class ThemeAdmin(admin.ModelAdmin):
    inlines = [ThemeImageInline]
    list_display = ['name', 'codename', 'active', 'order']
    list_editable = ['active', 'order']


class ThemeImageAdmin(admin.ModelAdmin):
    pass



class ModuleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"codename": ("name",)}
    list_display = ['name', 'codename', 'visible', 'active', 'order']
    list_editable = ['codename', 'visible', 'active', 'order']


class AppTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"codename": ("name",)}
    filter_horizontal = ("modules",)



class ApplicationStatusAdmin(admin.ModelAdmin):
    pass



#
# class CeviriInline(admin.TabularInline):
# #    formfield_overrides = {
# #        models.TextField: {'widget': CKEditorWidget()},
# #    }
#     model = BlockTranslation
#     extra = 0



class BlockAdmin(Modmin):
    list_display = ('keyword', 'translation', 'lang', 'translated')
    readonly_fields = ['keyword', 'translated', 'lang']
    list_editable = ['translation']
    save_on_top = True
    list_filter = ['lang', 'translated']
    # inlines = [CeviriInline, ]



# class BlockTranslationAdmin(admin.ModelAdmin):
#     list_display = ('keyword', 'translation')
#     readonly_fields = ['block','lang']
#     list_editable = ('translation',)
#     save_on_top = True
#


# admin.site.register(Block, BlockAdmin)
# admin.site.register(BlockTranslation, BlockTranslationAdmin)
