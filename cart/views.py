import datetime

from django.shortcuts import render_to_response, HttpResponseRedirect, RequestContext, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Cart, CartItem
from products.models import Product
from profiles.models import Profile
from profiles.forms import AddressForm

from orders.models import Order
from .forms import ProductQtyForm

from orders.custom import id_generator
import stripe
stripe.api_key = "sk_test_LFUiJWOW8O8ecMsXQmhzmDxs"


def add_to_cart(request):
    request.session.set_expiry(0)

    try:
        cart_id = request.session['cart_id']
    except:
        cart = Cart()
        cart.user = request.user
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

            if product_quantity > 0:
                new_cart.quantity = product_quantity
                new_cart.total = int(new_cart.quantity) * new_cart.product.price
                new_cart.save()
            else:
                pass

            return HttpResponseRedirect('/cart/')
        return HttpResponseRedirect('/contact/')
    else:
        raise Http404

def add_stripe(user):
    profile, created = Profile.objects.get_or_create(user=user)

    if len(profile.stripe_id) > 2:
        pass
    else:
        new_customer = stripe.Customer.create(
            email=user.email,
            description="Added to stripe on %s" % (datetime.datetime.now())
        )
        profile.stripe_id = new_customer.id
        profile.save()

    return profile.stripe_id

def view_cart(request):
    #request.session.set_expiry(10)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['cart_items'] = len(cart.cartitem_set.all())
    except:
        cart = False

    if not cart or not cart.active:
        message = "Your cart is empty"

    if cart and cart.active:
        cart = cart
        cart.total = 0
        for item in cart.cartitem_set.all():
            cart.total += item.total
            cart.save()

    try:
        stripe_id = add_stripe(user=request.user)
    except:
        pass

    return render_to_response('cart/view.html', locals(), context_instance=RequestContext(request))


@login_required()
def checkout(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
    except:
        cart = False

    if cart:
        amount = int(cart.total * 100)

    try:
        stripe_id = add_stripe(user=request.user)
    except:
        pass

    new_number = id_generator()

    new_order, created = Order.objects.get_or_create(cart=cart, user=request.user)

    if created:
        new_order.status = 'Started'
        new_order.order_id = str(new_number[:2]) + str(new_order.cart.id) + str(new_number[3:])
        new_order.save()

    address_form = AddressForm(request.POST or None)
    if request.method == "POST":
        address_form = AddressForm(request.POST)
        token = request.POST['stripeToken']
        profile = Profile.objects.get(user=request.user)
        stripe.Charge.create(amount=amount,
                             currency="usd",
                             card=token,
                             description="Payment for Cart")

        if address_form.is_valid():
            form = address_form.save(commit=False)
            print form

        return HttpResponseRedirect('/products/')

    return render_to_response('cart/checkout.html', locals(), context_instance=RequestContext(request))