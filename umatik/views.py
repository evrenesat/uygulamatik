#-*- coding:utf-8 -*-
from decimal import Decimal
from collections import defaultdict
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views.decorators import staff_member_required
import re
from django.core import serializers
from django.views.decorators.cache import never_cache
from at_shop_order.models import OrderTable
from umatik.models import *
from umatik.models import _thread_locals
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from operator import itemgetter
from itertools import groupby
from django.template import Context, Template

if settings.DEBUG:
    json_sort_keys = True
    json_indent = 4
else:
    json_sort_keys = False
    json_indent = None




def main(request):
    """
    Anasayfa
    @return: null
    """
    return HttpResponse('', mimetype="application/json")

# guncelleme icin veritabanindaki gerekli tablolardaki tum veriler json formatinda cihaza gonderiliyor
@never_cache
def get_all_records(request, appid):
    get_translations_for = request.GET.get('lang', False)
    #lang 'en' gibi 2 harflik dil kodu
    _thread_locals.app_id = appid
    if get_translations_for:
        _thread_locals.api_lang = get_translations_for
    else:
        _thread_locals.api_lang = ''


    #    images = list()
    # places = Place.objects.filter(app=appid).select_related('node').values('id', 'name', 'description', 'template',
    #                                                                        'category',
    #                                                                        'category__pid', 'node', 'node__map_id',
    #                                                                        'authorized_person', 'address', 'phone',
    #                                                                        'gsm', 'email',
    #                                                                        'logo', 'background', 'pid', 'llogo')
    # for s in places:
    #     s['place_id'] = s['id']
    #     s['id'] = s['pid']
    #     s['category_id'] = s['category']
    #     s['category'] = s['category__pid']
    #     del s['pid']
    #     s['logo'] = imgclean(s['logo'])
    #     s['llogo'] = imgclean(s['llogo'])
        #            images.append(s['llogo'])

    # categories = ProductCategory.objects.select_related().filter(app=appid).values('id', 'parent_category',
    #                                                                                'parent_category__pid',
    #                                                                                'image', 'name', 'pid')
    # for c in categories:
    #     c['product_category_id'] = c['id']
    #     c['id'] = c['pid']
    #     del c['pid']
    #     c['upper_category'] = c['parent_category__pid']
    #     del c['parent_category__pid']
    #     c['image'] = imgclean(c['image'])
    #     #            images.append(c['image'])

    # store_categories = StorePr

    products = Product.objects.select_related().filter(app=appid).values('id', 'category', 'store_category',
                                                                         'place', 'name', 'pid', 'description', 'price',
                                                                         'cut_price', 'discount_rate', 'image',
                                                                         'showcase',
                                                                         'category__pid', 'store_category__pid',
                                                                         'place__pid')
    for p in products:
        p['product_id'] = p['id']
        p['id'] = p['pid']
        del p['pid']
        p['place_id'] = p['place']
        p['category_id'] = p['category']
        p['store_category_id'] = p['store_category']
        p['category'] = p['category__pid']
        p['store_category'] = p['store_category__pid']
        p['place'] = p['place__pid']
        del p['category__pid']
        del p['store_category__pid']
        del p['place__pid']
        p['image'] = imgclean(p['image'])
        #        if p['image']:
    #            p['image'] =
    #            images.append(p['image'])
    #            images.extend(Product.get_thumbs(p['image']))

    # campaigns = Campaign.objects.select_related().filter(app=appid).values('id', 'place', 'category', 'product', 'name',
    #                                                                        'category__pid', 'no_text', 'description',
    #                                                                        'start_date', 'end_date',
    #                                                                        'stock', 'type',
    #                                                                        'image', 'thumb_image', 'special_background',
    #                                                                        'pid', 'place__pid', 'product__pid')
    # for c in campaigns:
    #     c['campaign_id'] = c['id']
    #     c['id'] = c['pid']
    #     del c['pid']
    #     c['category_id'] = c['category']
    #     c['category'] = c['category__pid']
    #     c['place_id'] = c['place']
    #     c['product_id'] = c['product']
    #     c['place'] = c['place__pid']
    #     c['product'] = c['product__pid']
    #     del c['place__pid']
    #     del c['product__pid']
    #     c['image'] = imgclean(c['image'])
    #     c['thumb_image'] = imgclean(c['thumb_image'])
    #     c['special_background'] = imgclean(c['special_background'])

    version = Version.objects.filter(app=appid).order_by('-id')[:1].values('current_version', 'pid', 'id')
    for v in version:
        v['id'] = v['pid']
        del v['pid']


    #############  NEWS & PAGES##################

    # news = dict(
    #     [(d['id'], d) for d in
    #      News.objects.filter(app=appid).values('id', 'title', 'detail', 'image', 'summary', 'timestamp')]
    # ) or {'none': True}

    news = News.get_data()

    pages = dict(
        [(d['id'], d) for d in
         Page.objects.filter(app=appid).values('id', 'title', 'detail', 'image', 'summary', 'timestamp')]
    ) or {'none': True}

    #############  PHOTO GALLERY ##################

    photos = dict([(d['id'], d) for d in Photo.objects.filter(app=appid).values('id', 'title', 'photo')]) or {
        'none': True}

    #############  DELEGATES ##################

    # delegates = dict([(d['id'], d) for d in
    #                   Delegate.objects.filter(app=appid).values('id', 'firstname', 'lastname', 'company',
    #                                                             'position', 'profile', 'photo')]) or {'none': True}

    ############# EVENTS & SPEAKERS##################

    events = Event.get_data()
    speakers = Speaker.get_data()
    # events = Event.objects.filter(app=appid).values('id', 'title', 'description', 'date', 'start', 'end', 'image',
    #                                                 'location', 'node')
    # if events:
    #     for a in events:
    #         a['speakers'] = list(Speaker.objects.filter(event__id=a['id']).values_list('id', flat=True))
    #
    #     speakers = dict([(s['id'], s) for s in
    #                      Speaker.objects.filter(app=appid).values('id', 'firstname', 'lastname', 'profile', 'position',
    #                                                               'company', 'photo')])
    #     events = regroupEvents(events)
    # else:
    #     speakers = []

    #############  Menucategories & menuitems   ##################

    menu_categories = list(MenuCategory.objects.filter(app=appid).values('id', 'name', 'image'))
    for st in menu_categories:
        st['items'] = list(MenuItem.objects.filter(app=appid, category=st['id']).values_list('id', flat=True))
    menu_items = dict([(s['id'], s) for s in
                      MenuItem.objects.filter(app=appid).values('id', 'name', 'description', 'price', 'cut_price',
                                                                'image', 'showcase')])
    #############  Sponsors & SponsorTypes   ##################

    sponsor_types = list(SponsorType.objects.filter(app=appid).values('id', 'title'))
    for st in sponsor_types:
        st['sponsors'] = list(Sponsor.objects.filter(app=appid, type=st['id']).values_list('id', flat=True))
    sponsors = dict([(s['id'], s) for s in Sponsor.objects.filter(app=appid).values('id', 'company', 'profile', 'phone',
                                                                                    'email', 'logo')])
    #############  MODULES ##################

    app = Application.objects.get(id=appid)
    modules = [{'codename': ms.module.codename,
                'title': ms.title,
                'sort': ms.order,
                'visible': ms.visible,
                'icon': ms.customicon.name if ms.customicon else ms.icon.getFileName(),
                }
               for ms in app.moduleselection_set.select_related().filter(active=True)]
    modules.extend([{'codename': module.codename, 'title': '', 'visible': '', 'icon': ''} for module in
                    app.type.modules.filter(visible=False)])

    exhibitors, node2exh = Exhibitor.get_data()

    exhibitorfiles = ExhibitorFiles.get_data()

    #############  MAPS ##################
    #maps = dict([(d['id'], d) for d in Map.objects.filter(app=appid).values('id', 'name', 'map')]) or {'none': True}
    maps = {}
    for d in Map.objects.filter(app=appid):
        maps[d.id] = {'id': d.id, 'offset': d.offset, 'name': d.name, 'image': d.map.name, 'width': d.map.width,
                      'height': d.map.height}
    if not maps:
        maps = {'none': True}
    mapgraph = dict(filter(lambda a: a[1], [(p.id, p.get_node_matrix()) for p in Node.objects.filter(app_id=appid)]))
    coordinates = dict([(n['id'], n) for n in Node.objects.filter(app_id=appid).values('id', 'x', 'y', 'map_id', 'type',
                                                                                       'name')])
    mapnodes = defaultdict(list)
    for n in Node.objects.filter(app_id=appid):
        mapnodes[n.map_id].append(n.id)

    #############  JOIN ALL ##################
    #WORKAROUND FOR AVM
    delegates = Delegate.get_data()
    categories = ProductCategory.get_data()
    store_categories = StoreProductCategory.get_data()
    places = Place.get_data()
    campaigns = Campaign.get_data()


    data = {
        'simple_data': {
            #simple data stored as JSON in `settings` table on client DB
            'exhibitors': dict(exhibitors),
            'exhibitorfiles': dict(exhibitorfiles),
            'sponsors': sponsors or {'none': True},
            'sponsortypes': sponsor_types or {'none': True},
            'speakers': speakers or [],
            "mapgraph": mapgraph,
            "mapnodes": mapnodes,
            "maps": maps,
            "node2exh": node2exh or {'none': True},
            "coordinates": coordinates or [],
            'delegates': delegates or [],
            'modules': modules,
            'menucategories': menu_categories,
            'menuitems': menu_items or [],
            'photos': photos or [],
            'events': events or [],
            'news': news or [],
            'pages': pages or [],
            'cms': Content.get_data(),
            # 'cms_children': [],
            'kafe_tables': OrderTable.get_data(),
            'themecss': app.css,
            'semitransbg': app.theme.transparent_background,
            'verytransbg': app.theme.transparent_background2,
            'avail_langs': list(app.applang_set.values_list('code', flat=True))
            # 'jmt': 'a',#app.theme.jmt #FIXME: delete or preperly fix this
        },
        'appinfo': [],
        'places': list(places),
        'categories': list(categories),
        'store_product_categories': list(store_categories),
        'products': list(products),
        'campaigns': list(campaigns),
        'version': list(version),
        #        'images': filter(lambda n: n.find('_s_') > 0 and bool(n.strip()), _get_image_list(appid))
        'images': _get_image_list(appid)
    }
    #    return HttpResponse( data), mimetype='application/json')

    json_data = json.dumps(data, cls=DjangoJSONEncoder, indent=json_indent, ensure_ascii=False)\
        .replace('"appinfo": []', '"appinfo": %s' % serializers.serialize('json', [app])) \
        .replace('uploads/', '')
        # .replace('"cms_children": []', '"cms_children": %s' % Content.get_child_data())
    return HttpResponse(json_data, mimetype='application/json')


def get_thumbs(mdl, appid=0, size_list=[], name='', n_list=[], fields=[], filter_in=''):
    """
    ya dosya adi / listesi uzerinde calisir ya da model verilir herseyi kendi halleder.

    @param mdl: model sinifi
    @param size_list: thumbnail onek listesi
    @param name: dosya adi
    @param n_list: dosya adi listesi
    @param fields: list, modelin bu alanlarini cek
    @param filter_in: dosya adinda bu gecmiyorsa alma
    @return:
    """
    l = set()
    name_list = []
    if name:
        name_list.append(name)
    elif n_list:
        name_list.extend(n_list)
    elif fields:
        qr = mdl.objects.filter(app=appid).values_list(*fields)
        filtered = filter(lambda l: l[0], qr)
        for lst in filtered:
            name_list.extend(lst)

    if not size_list:
        size_list = mdl.THUMB_SIZES
        prefix = mdl.THUMB_PREFIX + '_'
    else:
        prefix = ''

    #    if filter_in:
    #        name_list = filter(lambda i:filter_in not in i, name_list)
    #
    for n in name_list:
        name = re.sub(r'(.*)/(.*)', r'\2', n).replace('jpeg', 'jpg')
        if not filter_in:
            l.add(name)
        for x, y, z in size_list:
            if not filter_in or filter(lambda filter_item: filter_item.endswith(z), filter_in):
                l.add("%s%s_%s" % (prefix, z, name))
    return l


def _get_image_list(appid, startup=True):
    filter_in = ['_s', '_xs', '_n'] if startup else ''
    images = imgcleanlist(Place.objects.filter(app=appid, logo__isnull=False).values_list('logo', 'llogo'))
    images.extend(
        imgcleanlist(ProductCategory.objects.filter(app=appid).filter(image__isnull=False).values_list('image')))

    for ms in ModuleSelection.objects.filter(app_id=appid).filter(active=True):
        if ms.customicon:
            images.append(ms.customicon.name)
        else:
            images.append(ms.icon.getFileName())

    for m in Map.objects.filter(app_id=appid).values_list('map', flat=True):
        images.extend([imgclean(m), 's_%s' % imgclean(m)])

    x=get_thumbs(MenuItem, appid=appid, fields=['image'], filter_in=filter_in)
    images.extend(
        get_thumbs(Campaign, appid=appid, fields=['image', 'thumb_image', 'special_background'], filter_in=filter_in))
    images.extend(get_thumbs(Photo, appid=appid, fields=['photo'], filter_in=filter_in))
    images.extend(get_thumbs(Delegate, appid=appid, fields=['photo'], filter_in=filter_in))
    images.extend(get_thumbs(Speaker, appid=appid, fields=['photo'], filter_in=filter_in))
    images.extend(get_thumbs(Sponsor, appid=appid, fields=['logo'], filter_in=filter_in))
    images.extend(get_thumbs(Exhibitor, appid=appid, fields=['logo'], filter_in=filter_in))
    images.extend(get_thumbs(Product, appid=appid, fields=['image'], filter_in=filter_in))
    images.extend(get_thumbs(News, appid=appid, fields=['image'], filter_in=filter_in))
    images.extend(get_thumbs(Page, appid=appid, fields=['image'], filter_in=filter_in))
    images.extend(get_thumbs(Event, appid=appid, fields=['image'], filter_in=filter_in))
    images.extend(get_thumbs(MenuItem, appid=appid, fields=['image'], filter_in=filter_in))
    images.extend(get_thumbs(MenuCategory, appid=appid, fields=['image'], filter_in=filter_in))
    images.extend(Application.get_theme_images(appid))

    images.extend(imgcleanlist(
        Application.objects.filter(pk=appid, logo_small__isnull=False).values_list('logo_small', 'logo_big',
                                                                                   'header_image', 'background_image')))

    return images


@never_cache
def get_image_list(request, appid):
    images = _get_image_list(appid, False)
    return HttpResponse(json.dumps({'images': images}, cls=DjangoJSONEncoder, indent=json_indent),
                        mimetype='application/json')

@csrf_exempt
@never_cache
def settext(request, appid, lang):
    keys = json.loads(request.POST['keys'])
    # for l in AppLang.objects.filter(app_id=appid).values_list('code', flat=True):
    for l in AppLang.objects.exclude(code='en').values_list('code', flat=True):
        existing_keys = Block.objects.filter(lang=l).values_list('keyword', flat=True)
        nonexistent_keys = filter(lambda key: key not in existing_keys, keys)
        # Block.objects.bulk_create(map(lambda k:Block(keyword=k, app_id=appid, lang=l), nonexistent_keys))
        Block.objects.bulk_create(map(lambda k:Block(keyword=k, lang=l), nonexistent_keys))
    data = ['ok']
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), mimetype='application/json')


@never_cache
def gettext(request, appid, lang):
    #TODO: appid'i dikkate almiyoruz. custom tempalte destegi gelene kadar cok da sart degil gibi
    data = {
        'messages': {
            "": {'domain': "messages",
                 'lang': lang,
                 'plural_forms': "nplurals=2; plural=(n != 1);",
            },
            #        "a key": ['', "the translation", "the plural translations"]
            #        "%d key": ['', "%d key", "%d keys"]
        },

    }
    for bt in Block.objects.filter(lang=lang).values_list('keyword', 'translation'): #, translated=True
        data['messages'][bt[0]] = ['', bt[1] or bt[0]]
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), mimetype='application/json')


@never_cache
def pack_image_list(request, appid):
    app = Application.objects.get(pk=appid)
    images = filter(lambda n: n.find('_lrg_') == -1 and bool(n.strip()), _get_image_list(appid))
    images = '\n'.join(map(lambda n: 'http://appstatic.uygulamatik.com/media/uploads/%s' % n, images))
    return HttpResponse(images, mimetype='text/plain')


# sunucu db ile cihaz db versiyon kiyaslamasi
def get_version(request, appid):
    version, is_new = Version.objects.get_or_create(app_id=appid)
    return HttpResponse(json.dumps({'current_version': str(version.current_version)}), mimetype='application/json')

#    return HttpResponse(json.dumps(data, cls=myJSONEncoder), mimetype='application/json')

# django'nun json kodlayicisi tarihleri formatlamakta yetersiz, ekleme yapildi
class myJSONEncoder(DjangoJSONEncoder):
    """
    JSON çıktısı alırken gerekli formatlamaları yapan sınıf
    """

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%d/%m/%Y %H:%M")
        return DjangoJSONEncoder.default(self, o)


@csrf_exempt
def get_map_graph(request, appid):
    """
    @return json map graph for dijkstra.js
    """
    graph = ','.join([p.get_nbhd_json() for p in Node.objects.filter(app_id=appid) if p.get_nbhd_json()])

    return HttpResponse('{%s}' % graph, mimetype='application/json')


@never_cache
def get_theme_css(request, appid):
    """
    @return selected themes css content
    """
    css = Application.objects.filter(id=appid).values_list('theme__processed_css', flat=True)
    return HttpResponse(css, mimetype='text/css')



def getappid(request):
    """
    @return selected themes css content
    """
    if 'HTTP_REFERER' in request.META:
        subdomain = request.META['HTTP_REFERER'].split('.')[0].replace('http://','')
        id = Application.objects.filter(subdomain=subdomain).values_list('id', flat=True)[0]
    else:
        id = 0
    return HttpResponse('APPID=%s;' % id, mimetype='application/javascript')



def appid_from_domain(request, subdomain=None):
    """
    @return selected themes css content
    """
    if not subdomain and 'HTTP_REFERER' in request.META:
        subdomain = request.META['HTTP_REFERER'].split('.')[0].replace('http://','')
    aid = Application.objects.filter(subdomain=subdomain).values_list('id', flat=True)
    if aid:
        aid = aid[0]
    else:
        aid = 0
    return HttpResponse('{"id":%s}' % aid, mimetype='application/json')



@never_cache
def get_theme_css_for_web(request, appid):
    """
    @return selected themes css content.
    """
    css = Application.objects.filter(id=appid).values_list('theme__web_processed_css', flat=True)
    return HttpResponse(css, mimetype='text/css')


def save_client_error(request, appid):
    """
    @return: istemciden *k*onsole.log ile gelen exceptionlari kaydeder.
    """
    log = Elog.objects.create(msg=request.POST['msg'], app_id=appid)
    return HttpResponse('ok', mimetype='application/json')


def create_new_translation(request, appid):
    """graph_json
    @return: istemciden gelen tanimsiz ceviri metinlerini olusturur.
    """
    log = Elog.objects.create(msg=request.POST['msg'], app_id=appid)
    return HttpResponse('ok', mimetype='application/json')


def _gcustomer(request, appid):
    """

    @param request:
    @return: get_or_creates a customer object from post data
    """
    cust = json.loads(request.POST['customer'])
    return Customer.objects.get_or_create(app_id=appid, mobile=cust['tel'],
                                          defaults={
                                              'name': cust['name'],
                                              'mail': cust['email'],
                                              'address': cust['address']
                                          })


#CONTENT_TYPE={'place':'Place','activity':'Activity'}
# FEEDBACK_TYPE_DICT = {'thanks': 1, 'suggestion': 2, 'complaint': 3}


@csrf_exempt
def save_feedback(request, appid):
    """
    @return: istemciden *k*onsole.log ile gelen exceptionlari kaydeder.
    """
    p = request.POST.copy()

    content_type = p.get('content_type', 'place')
    customer, newcustomer = _gcustomer(request, appid)

    fb = Feedback.objects.create(app_id=appid, customer=customer,
                                 type=p['mood'],
                                 msg=p['msg'])
    ctid = ContentType.objects.get(model=content_type).id if content_type != 'host' else 0
    #    if ctid:
    #        fb.content_type_id = ctid
    #        fb.object_id = p.get('oid', 0)
    #        fb.save()
    #
    if p.get('oid') and content_type == 'place':
        fb.place_id = p.get('oid')
        fb.save()
    elif not p.get('oid'):
        fb.forhost = True
        fb.save()

    return HttpResponse(json.dumps({'result': 'ok'}, ensure_ascii=False), mimetype='application/json')


@csrf_exempt
def save_order(request, appid):
    """
    @return: istemciden *k*onsole.log ile gelen exceptionlari kaydeder.
    """
    p = request.POST.copy()
    customer, newcustomer = _gcustomer(request, appid)
    bo = BaseOrder.objects.create(app_id=appid, customer=customer, total_price=Decimal(p['sum']))
    #TODO: price should be checekd for client and server differeneces
    for itm in json.loads(p['items']):
        OrderItem.objects.create(app_id=appid, product_id=itm['product'], qty=int(itm['count']), baseorder=bo)
    bo.calculateTotal()
    bo.createStoreOrders()
    return HttpResponse(json.dumps({'result': 'ok', 'order_id': bo.id}, ensure_ascii=False),
                        mimetype='application/json')
