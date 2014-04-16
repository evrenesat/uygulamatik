__author__ = 'Evren Esat Ozkan'

from django.templatetags.static import register
import sys
#sys.path.insert(0,'/home/yalcin/PycharmProjects/cenevar/blok')
from blok.models import __

#assert 0,models

@register.simple_tag()
def blk(kelime):
    return __(kelime)


