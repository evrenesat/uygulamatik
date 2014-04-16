__author__ = 'yalcin'

from blok.models import Block, BlockTranslation
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django.db import models




class CeviriInline(admin.TabularInline):
#    formfield_overrides = {
#        models.TextField: {'widget': CKEditorWidget()},
#    }
    model = BlockTranslation
    extra = 0



class BlockAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'type','status')
    readonly_fields = ['keyword','status']
    list_editable = ['type',]
    save_on_top = True
    inlines = [CeviriInline, ]



class BlockTranslationAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'translation')
    readonly_fields = ['block','lang']
    list_editable = ('translation',)
    save_on_top = True



admin.site.register(Block, BlockAdmin)
admin.site.register(BlockTranslation, BlockTranslationAdmin)
