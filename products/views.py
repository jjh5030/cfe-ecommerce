from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from cart.forms import ProductQtyForm
from .models import Product


def all_products(request):
    products = Product.objects.all()
    return render_to_response('products/all.html', locals(), context_instance=RequestContext(request))

def single_product(request, slug):
    add_product = ProductQtyForm()
    product = get_object_or_404(Product, slug=slug)
    return render_to_response('products/single.html', locals(), context_instance=RequestContext(request))

def search(request):
    try:
        q = request.GET.get('q', '')
    except:
        q = False

    if q:
        k = q.split()
        print k
        if len(k) > 1:
            products = []
            for i in k:
                products_all = Product.objects.filter(title__icontains=i).distinct()
                for product in products_all:
                    if product not in products:
                        products.append(product)
        else:
            products = Product.objects.filter(title__icontains=q)

    return render_to_response('products/search.html', locals(), context_instance=RequestContext(request))