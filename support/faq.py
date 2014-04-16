e# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import logging
log = logging.getLogger('genel')
from utils.cache import kes

class MainCategory(models.Model):
    """Tag category"""

    text = models.CharField(_('Name'), max_length=100)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Main Category')
        verbose_name_plural = _('FAQ Main Categories')

    def __unicode__(self):
        return '%s' % (self.text,)

class MainCategoryTranslation(models.Model):
    """Place description"""

    category = models.ForeignKey('MainCategory')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.CharField(_('Translation'), max_length=100)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Main Category Name Translation')
        verbose_name_plural = _('FAQ Main Category Name Translations')

    def __unicode__(self):
        return 'Place #%s Lang:%s' % (self.category_id, self.lang)

class Category(models.Model):
    """Tag category"""
    main_category = models.ForeignKey('MainCategory',  null=True, blank=True)
    text = models.CharField(_('Name'), max_length=100)
#    lang = models.CharField(_('Category'), max_length=2, db_index=True, choices=settings.LANGUAGES)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    order = models.SmallIntegerField(_('Order'),default=100)

    class Meta:
        app_label = 'website'
        ordering = ['order']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Category')
        verbose_name_plural = _('FAQ Categories')

    def __unicode__(self):
        return '%s' % (self.text,)

class CategoryTranslation(models.Model):
    """Place description"""

    category = models.ForeignKey('Category')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.CharField(_('Translation'), max_length=100)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Category Name Translation')
        verbose_name_plural = _('FAQ Category Name Translations')

    def __unicode__(self):
        return 'Place #%s Lang:%s' % (self.category_id, self.lang)

from collections import defaultdict
class Question(models.Model):
    """Place tags"""

    category = models.ForeignKey('Category')
#    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    order = models.SmallIntegerField(_('Order'),default=100)
    text = models.CharField(_('Question'), max_length=250)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    @classmethod
    def getFaqs(cls, lang):
        return kes(lang,'faqs').g({}) or cls._updateCache(lang)

    def getTrans(self,lang):
        return self.questiontranslation_set.filter(lang=lang).values_list('text',flat=True)[0]

    @classmethod
    def _updateCache(cls, lang=None):
        for code,name in settings.LANGUAGES:
            mi = defaultdict(list)
            cat_name_list = CategoryTranslation.objects.filter(lang=code).order_by('category__order').values_list('category_id','text','category__order')
            cat_names = dict([a[:2] for a in cat_name_list])
            cat_order = dict([a[1:] for a in cat_name_list])
            for mc in MainCategory.objects.filter(active=True):
                di = defaultdict(list)
                for a in Answer.objects.select_related().order_by('question__order').filter(lang=code,
                    active=True, question__category__main_category=mc):
                    di[cat_names.get(a.question.category_id,'---')].append({
                        'answer':mark_safe(a.text), 'qid':a.question_id, 'question':a.question.getTrans(code)})
#                log.info('preorder: %s'%di.keys())
#                log.info(cat_order)
                di = sorted(di.items(),key=lambda x: cat_order.get(x[0]))
#                log.info('postorder: %s'%di)
#                di = di.items()
                main_cat_name = mc.maincategorytranslation_set.filter(lang=code).values_list('text',flat=True)
                mi[main_cat_name[0] if main_cat_name else '---' ] = di
            mi = mi.items()
            kes(code,'faqs').s(mi,100)#FIXME: set this to a biger value
            if lang == code:
                lang = mi
        return lang


    def save(self, *args, **kwargs):
        self._updateCache()
        super(Question, self).save(*args, **kwargs)

    class Meta:
        app_label = 'website'
        ordering = ['order']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Question')
        verbose_name_plural = _('FAQ Questions')

    def __unicode__(self):
        return '%s' % (self.text,)


class QuestionTranslation(models.Model):
    """Place description"""

    question = models.ForeignKey('Question')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.CharField(_('Question'), max_length=250)
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Question Translation')
        verbose_name_plural = _('FAQ Question Translations')

    def __unicode__(self):
        return '#%s Lang:%s' % (self.question_id, self.lang)

class Answer(models.Model):
    """Place tags"""

    question = models.ForeignKey('Question')
    lang = models.CharField(max_length=2, db_index=True, choices=settings.LANGUAGES)
    text = models.TextField(_('Answer'))
    active = models.BooleanField(_('Active'), default=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        app_label = 'website'
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('FAQ Answer')
        verbose_name_plural = _('FAQ Answers')

    def __unicode__(self):
        return '%s' % (self.text[:30],)

    def save(self, *args, **kwargs):
        self.question._updateCache()
        super(Answer, self).save(*args, **kwargs)
