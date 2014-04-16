# -*-  coding: utf-8 -*-
from hashlib import md5
import os
from django.utils.http import urlquote

__author__ = 'Evren Esat Ozkan'

import memcache
from django.core.cache import cache
#cache = memcache.Client(['127.0.0.1:11211'], debug=0)
from django.conf import settings

from django.utils.encoding import smart_unicode, smart_str

sitekey = settings.CACHE_MIDDLEWARE_KEY_PREFIX
#sure = settings.CACHE_MIDDLEWARE_SECONDS
sure = 99999

class kes:
    def __init__(self, *args):
        list(args).insert(0,sitekey)
        self.key = smart_str('_'.join([str(n) for n in args]))

    def __unicode__(self):
        return '%s icin onbellek nesnesi' % self.key


    def get(self, default=None):
        """
        cacheden donen degeri, o yoksa `default` degeri dondurur
        """
        d = cache.get(self.key)
        return d if d is not None else default

    def set(self, val=1, lifetime=sure):
        """
        val :: atanacak deger (istege bagli bossa 1 atanir).
        lifetime :: önbellek süresi, varsayilan 100saat
        """
        cache.set(self.key, val, lifetime)
        return val

    def delete(self, *args):
        """
        cache degerini temizler
        """
        return cache.delete(self.key)

    def incr(self, delta=1):
        """
        degeri delta kadar arttirir
        """
        return cache.incr(self.key, delta=delta)

    def decr(self, delta=1):
        """
        degeri delta kadar azaltir
        """
        return cache.decr(self.key, delta=delta)

def del_temp_cache(name, *variables):
    cache_key = 'template.cache.%s.%s' % (name, md5(u':'.join([urlquote(var) for var in variables])).hexdigest())
    cache.delete(cache_key)

def del_temp_cache_for_langs(name, *args):
    for l,v in settings.LANGUAGES:
        vars = list(args)
        vars.append(l)
        del_temp_cache(name, *vars)

def del_kes_for_langs(*args):
    for l,v in settings.LANGUAGES:
        vars = list(args)
        vars.append(l)
        kes(*vars).d()


from django.http import HttpRequest
from django.utils.cache import get_cache_key

def expire_page(path):
    request = HttpRequest()
    for l,v in settings.LANGUAGES:
        request.path = '/%s%s' % (l, path)
        key = get_cache_key(request)
        cache.delete(key)
