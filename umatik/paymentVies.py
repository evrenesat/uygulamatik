# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

__author__ = 'ozgur'
__creation_date__ = '09.03.2013' '15:56'

from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response
from django.template import RequestContext
import models as umodels


@login_required
def mainPaymentView(request):
    app = umodels.Application.objects.get(id=request.session['appid'])
    context = {
        'appName': app.name_long,
        'appCompany': app.company,

    }
    return render_to_response("payment/paymentMain.html", context, context_instance=RequestContext(request))


@login_required
def freePaymentView(request):
    app = umodels.Application.objects.get(id=request.session['appid'])
    app.published = True
    app.status = umodels.ApplicationStatus.objects.get(id=1)
    app.save()
    # app.save()
    context = {
        'appId': app.id,
        'appName': app.name_long,
        'appCompany': app.company,

    }
    return render_to_response("payment/paymentFree.html", context, context_instance=RequestContext(request))