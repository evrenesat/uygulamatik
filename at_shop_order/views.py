# -*- coding: utf-8 -*-
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from models import OrderHead, LocalOrderItem
from umatik.views import _gcustomer

from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings

__author__ = 'ozgur'
__creation_date__ = '10.03.2013' '22:58'

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
import json

if settings.DEBUG:
    json_sort_keys = True
    json_indent = 4
else:
    json_sort_keys = False
    json_indent = None
# @login_required
# def index(request):
#     return render_to_response("index.html", {'test': 'Elif'}, context_instance=RequestContext(request))


@csrf_exempt
def save_order(request, appid):
    """
    @return: istemciden *k*onsole.log ile gelen exceptionlari kaydeder.
    """
    p = request.POST.copy()
    # customer, is_new = _gcustomer(request, appid)
    bo = OrderHead.objects.create(app_id=appid,  total_price=Decimal(p['sum']), order_table_id=p['table']) #customer=customer,
    #TODO: price should be checekd for client and server differeneces
    for itm in json.loads(p['items']):
        bo.localorderitem_set.create(app_id=appid, product_id=itm['id'], qty=itm['count'])
    bo.calculateTotal()
    # bo.createStoreOrders()
    return HttpResponse(json.dumps({'result': 'ok', 'order_id': bo.id}, ensure_ascii=False),
                        mimetype='application/json')


@login_required
def orderMain(request, appid):
    context = {
        'newOrderCount': OrderHead.objects.filter(app__id=appid, status=1).count(),
        'prepOrderCount': OrderHead.objects.filter(app__id=appid, status=2).count(),
        'readyOrderCount': OrderHead.objects.filter(app__id=appid, status=3).count(),
        'oldOrderCount': OrderHead.objects.filter(app__id=appid, status=4).count(),
        'appid': appid
        # ''
    }
    return render_to_response("aso_main.html", context, context_instance=RequestContext(request))


def orderList(request, appid, status):
    context = {
        'appid': appid,
        'productList': OrderHead.objects.filter(app__id=appid, status=status)
    }
    return render_to_response("aso_list.html", context, context_instance=RequestContext(request))
