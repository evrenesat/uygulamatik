# -*- coding: utf-8 -*-
from ckeditor.fields import RichTextField
from qurl.models import QRcode
from umatik.models import Application, MenuItem, UModel, TModel, generate_qrcode, update_version

__author__ = 'ozgur'
__creation_date__ = '10.03.2013' '22:58'

from django.db import models
from django.utils.translation import ugettext_lazy as _, activate
from django.db.models import F, signals, Sum


ORDER_HEAD_STATUS = (
    (5, _('Table selected')),
    (10, _('Ordered')),
    (20, _('Preparing')),
    (30, _('Ready')),
    (40, _('On the road')),
    (50, _('On the table')),
    (90, _('Return')),
    (91, _('Sold out')),
    (95, _('Cancelation request')),
    (96, _('Canceled')),
)


class OrderTableTranslation(TModel):
    source = models.ForeignKey('OrderTable', related_name='translations', help_text=_('News to translate'))
    name = models.CharField(max_length=50, verbose_name=_('Table Name'), help_text=_('Name or number of the table'))
    explanation = RichTextField(verbose_name=_('Explanation'),
                                   help_text=_('Use this field to give more information about this table.'), null=True, blank=True)



class OrderTable(UModel):
    """Table , place etc.The table that order was given"""
    app = models.ForeignKey(Application, verbose_name=_('Application'),
                            help_text=_('The application that has this table'))
    name = models.CharField(max_length=50, verbose_name=_('Table Name'), help_text=_('Name or number of the table'))
    qrcode = models.OneToOneField(QRcode, null=True, blank=True)
    explanation = RichTextField(verbose_name=_('Explanation'),
                                   help_text=_('Use this field to give more information about this table.'), null=True, blank=True)
    sort = models.SmallIntegerField(_('Display order'), default=1, null=True, blank=True,
                                    help_text=_('Display order on table list.'))

    QRTYPE = 't'
    @classmethod
    def get_data(cls):
        return dict([(d['id'], d) for d in cls._get_values(['id', ], ['name', 'explanation'])]) or {'none': True}

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['sort', 'name']
        verbose_name = _('Table')
        verbose_name_plural = _('Tables')


class OrderHead(models.Model):
    """It is totally order! No more!"""
    app = models.ForeignKey(Application, verbose_name=_('Application'), help_text=_('The application that has this order'))
    status = models.SmallIntegerField(verbose_name=_('Status'), choices=ORDER_HEAD_STATUS, default=10, help_text=_('Status of the order'))
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now_add=True)
    ptime = models.DateTimeField(verbose_name=_('Completion time'), null=True, blank=True, help_text=_('The date when the order is completed'))
    total_price = models.DecimalField(verbose_name=_('Total price'), decimal_places=2, max_digits=9, null=True, blank=True, help_text=_('Total price of the order'))
    order_table = models.ForeignKey(OrderTable, verbose_name=_('Order Table'), help_text=_('The table that order was given'))

    def calculateTotal(self):
        self.total_price = self.localorderitem_set.aggregate(Sum('line_total'))['line_total__sum']
        self.save()

    def __unicode__(self):
        return '%s' % (self.id,)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class LocalOrderItem(models.Model):
    """siparis"""

    app = models.ForeignKey(Application, verbose_name=_('Application'), help_text=_('The application that has this order item'), editable=False)
    order_head = models.ForeignKey(OrderHead, verbose_name=_('Order'), help_text=_('Main order of the  order item'))
    product = models.ForeignKey(MenuItem, verbose_name=_('Product'), help_text=_('The product that is ordered'))
    price = models.DecimalField(verbose_name=_('Price'), decimal_places=2, max_digits=7, help_text=_('Price of the item'), null=True, blank=True)
    qty = models.IntegerField(verbose_name=_('Quantity'), default=1, help_text=_('Quantity of the order item'))
    line_total = models.DecimalField(_('Line total'), decimal_places=2, max_digits=7, help_text=_('Line total of the order item'), blank=True)
    done = models.BooleanField(default=False, verbose_name=_('Done?'), help_text=_('Is it delivered?'))

    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        verbose_name = _('Order item')
        verbose_name_plural = _('Order Items')

    def __unicode__(self):
        return '%s' % (self.id,)

    def save(self, *args, **kwargs):
    #        super(OrderItem, self).save(*args, **kwargs)
        if not self.app:
            self.app = self.order_head.app
        self.price = self.product.cut_price or self.product.price
        self.line_total = self.price * self.qty
        super(LocalOrderItem, self).save(*args, **kwargs)



for m in (OrderTable,):
    signals.post_save.connect(generate_qrcode, sender=m)
    signals.post_save.connect(update_version, sender=m)
