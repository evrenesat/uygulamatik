# -*- coding: utf-8 -*-
from django.conf import settings

__author__ = 'Evren Esat Ozkan'

from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.cache import kes
from django.template.defaultfilters import slugify
import logging
from django.utils.html import strip_tags
log = logging.getLogger('genel')
from django.utils import translation
from ckeditor.fields import RichTextField
BLOCK_STATUS=((0, 'None'), (1, 'Incomplete'), (2, 'Complete'))

BLOCK_TYPES=((1, 'HTML Box'), (2, 'Title'), (3, 'Text Box'))


import os
class Block(models.Model):
    """Content blocks"""

    keyword = models.CharField(_('Keyword'), max_length=100)
    status = models.SmallIntegerField(_('Status'), choices=BLOCK_STATUS, default=0)
    type = models.SmallIntegerField(_('Type'), choices=BLOCK_TYPES, default=0)


    def save(self, *args, **kwargs):
        super(Block, self).save(*args, **kwargs)
        for k, n in settings.LANGUAGES:
            cset = self.blocktranslation_set.filter(lang=k)
            if not cset:
                self.blocktranslation_set.create(lang=k)

    class Meta:
        verbose_name = u"Content Block"
        verbose_name_plural = u"Content Blocks"
        ordering = ['type']
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return '%s' % (self.keyword,)


class BlockTranslation(models.Model):
    """block content for each language"""
    KES_PREFIX = 'CEVIR'

    block = models.ForeignKey(Block, verbose_name=_('Türkçesi'))
    keyword = models.CharField(max_length=100, editable=False)
    lang = models.CharField(_('Language Code'), max_length=5, choices=settings.LANGUAGES)
    translation = models.TextField(_('Translation'), default='', blank=True)


    class Meta:
        ordering = ['lang']
        #app_label = 'website'
        verbose_name = _(u"Block Translation")
        verbose_name_plural = _(u"Block Translations")

    def __unicode__(self):
        return '%s for %s' % (self.keyword, self.lang)


    #
    def save(self, *args, **kwargs):
        self.keyword = slugify(self.block.keyword)
        if self.block.type in [2, 3]:
            self.translation = strip_tags(self.translation)
        super(BlockTranslation, self).save(*args, **kwargs)
        kes(self.KES_PREFIX, self.keyword, self.lang).set(self.translation)

    #        ceviri_sayisi = self.kelime.ceviriler_set.exclude(ceviri='').count()
#        status = 0
#        if ceviri_sayisi:
#            status = 2 if ceviri_sayisi == len(LOCALES) else 1
#        if self.block.status != status:
#            self.block.status = status
#            self.block.save()


def __(word):
    """
    db and memcache based translation/content block system that mimics gettext.
    """
    lang_code = translation.get_language()
    lang_code = 'tr'
    try:
        skelime = slugify(word)
        k = kes(BlockTranslation.KES_PREFIX, skelime[:40], lang_code)
        c = k.get()
        if c: return  c
        c = BlockTranslation.objects.filter(keyword=skelime, lang=lang_code).exclude(translation='').values_list(
            'translation', flat=True)
        if c: return k.set(c[0])
        Block.objects.get_or_create(keyword=skelime)
        return k.set(word)
    except:
        raise
        log.exception('cevir taginda patlama')
        return word
