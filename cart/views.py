from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext, HttpResponse
from .models import Cart, CartItem
from products.models import Product
from .forms import ProductQtyForm

# Create your views here.
def add_to_cart(request):
    try:
        cart_id = request.session['cart_id']
    except:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart_id
        cart_id = cart_id

    if request.method == "POST":
        form = ProductQtyForm(request.POST)
        if form.is_valid():
            product_slug = form.cleaned_date['slug']
            product_quantity = form.cleaned_date['quantity']

            try:
                product = Product.object.get(slug=product_slug)
            except:
                product = None

            new_cart = CartItem(cart=cart_id, product=product, quantity=product_quantity)
            new_cart.save()

            return HttpResponseRedirect('/products/')
    else:
        raise Http404

