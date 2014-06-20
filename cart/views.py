from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext, HttpResponse
from django.http import Http404

from .models import Cart, CartItem
from products.models import Product
from .forms import ProductQtyForm

# Create your views here.
def add_to_cart(request):
    request.session.set_expiry(0)

    try:
        cart_id = request.session['cart_id']
    except:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
        cart_id = cart.id

    if request.method == "POST":
        form = ProductQtyForm(request.POST)
        if form.is_valid():
            product_slug = form.cleaned_data['slug']
            product_quantity = form.cleaned_data['quantity']

            try:
                product = Product.objects.get(slug=product_slug)
            except:
                product = None

            try:
                cart = Cart.objects.get(id=cart_id)
            except:
                cart = None

            new_cart, created = CartItem.objects.get_or_create(cart=cart, product=product)
            new_cart.quantity = product_quantity

            new_cart.save()
            #print new_cart.product, new_cart.quantity, new_cart.cart

            if created:
                print "CREATED"

            return HttpResponseRedirect('/products/')
        return HttpResponseRedirect('/contact/')
    else:
        raise Http404

def view_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
    except:
        cart = False

    if not cart or not cart.active:
        message = "Your cart is empty"

    if cart and cart.active:
        cart = cart

    return render_to_response('cart/view.html', locals(), context_instance=RequestContext(request))