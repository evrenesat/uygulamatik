from django.db import models
from django.db.models import signals
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
# Create your models here.

import string
from django.utils.timezone import now


BASE_LIST = string.digits + string.letters + '_@'
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))


def base_decode(string, reverse_base=BASE_DICT):
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(string[::-1]):
        ret += (length ** i) * reverse_base[c]

    return ret


def base_encode(integer, base=BASE_LIST):
    length = len(base)
    ret = ''
    while integer != 0:
        ret = base[integer % length] + ret
        integer /= length

    return ret


base_url = 'http://chart.googleapis.com/chart?chf=a,s,000000&chs=100x100&cht=qr&chld=|2&chl=http%3A%2F%2F9oo.nl%2F'
big_base_url = 'http://chart.googleapis.com/chart?chf=a,s,000000&chs=300x300&cht=qr&chld=|2&chl=http%3A%2F%2F9oo.nl%2F'


class QRcode(models.Model):
    '''unique id provider for short url redirection with qrcode support'''

    url = models.URLField()
    code = models.CharField(_('Code'), max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(_('Creation'), default=now)


    class Meta:
        ordering = ['timestamp']
        get_latest_by = "timestamp"
        #verbose_name = _('')
        #verbose_name_plural = _('')

    def __unicode__(self):
        return mark_safe('<img src="%s%s">' % (base_url, self.code,))


def generate_code(sender, instance, created=True, **kwargs):
    if not instance.code:
        instance.code = base_encode(instance.id)
        instance.save()


signals.post_save.connect(generate_code, sender=QRcode)
