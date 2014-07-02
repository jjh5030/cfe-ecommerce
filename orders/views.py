from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Order

def view_orders(request):
    try:
        orders = Order.objects.filter(user=request.user)
    except:
        pass

    return render_to_response('orders/all.html', locals(), context_instance=RequestContext(request))