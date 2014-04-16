# Create your views here.
from django.http import HttpResponseRedirect, Http404
from qurl.models import QRcode


def redirect_id(request, code):
    try:
        return HttpResponseRedirect(QRcode.objects.filter(code=code).values_list('url', flat=True)[0])
    except:
        raise
        # raise Http404
