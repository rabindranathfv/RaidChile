from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _

from raidchileapp.models import Tour, Combo, Product

from .cart import Cart
from .forms import CartAddProductForm

# Create you shopping cart views here:
@require_POST
def cart_add(request, product_id):
	cart = Cart(request)

	# If there exists a combo already inside the cart redirect to cart detail with an error message.
	if (cart['combo_id'] and cart['combo_id'] != product_id):
		messages.warning(request, _('We\'re sorry. You already have a Tour Combo added. To reserve more or different tours, please remove the combo first.'))
		return redirect('cart:cart_detail')

	tour = get_object_or_404(Tour, id=product_id, product_type="TOUR")
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(
			product=tour,
			adult_qty=cd['adult_quantity'],
			children_qty=cd['children_quantity'],
			update_quantity=cd['update']
		)
	return redirect('cart:cart_detail')

@require_POST
def cart_add_combo(request, product_id):
	cart = Cart(request)
	# If there exists a combo already inside the cart redirect to cart detail with an error message.
	if (cart['combo_id'] and cart['combo_id'] != product_id) or (cart['combo_id'] == None and len(cart) > 0):
		messages.warning(request, _('We\'re sorry. You can only have one Tour Combo OR multiple Tours per reservation. To reserve a combo, please remove your other tours or combo first.'))
		return redirect('cart:cart_detail')

	try:
		combo = Combo.objects.prefetch_related('tours').get(Q(available=True) & Q(id=product_id) & Q(product_type='COMBO'))
	except Combo.DoesNotExist:
		raise Http404("No Tour Combos matches the given query.")

	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(
			product=combo,
			adult_qty=cd['adult_quantity'],
			children_qty=cd['children_quantity'],
			update_quantity=cd['update']
		)
	return redirect('cart:cart_detail')


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:cart_detail')


def cart_detail(request):
	cart = Cart(request)
	combo = False
	if cart['combo_id']:
		combo = Combo.objects.filter(id=cart['combo_id'], available=True).first()

	subtotal = Decimal(0)
	discount = Decimal(0)
	for item in cart:
		add_form = CartAddProductForm(
			initial={
				'adult_quantity': item['adult_qty'],
				'children_quantity': item['children_qty'],
				'update': True,
			}
		)
		item['update_quantity_form'] = add_form
		# calculate regular subtotal and combo discount.
		subtotal += Decimal(item['adult_qty']) * item['adult_reg_price'] + Decimal(item['children_qty']) * item['children_reg_price']
		if combo:
			discount += Decimal(item['adult_qty']) * (item['adult_reg_price'] - item['adult_sale_price']) + Decimal(item['children_qty']) * (item['children_reg_price'] - item['children_sale_price'])

	context = {
		'cart': cart,
		'combo': combo,
		'subtotal': subtotal,
		'discount': discount,
		'total': subtotal-discount,
	}

	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = reverse('cart:cart_detail')
		translation.activate('en')
		context['redirect_url_en'] = reverse('cart:cart_detail')
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = reverse('cart:cart_detail')
	finally:
		translation.activate(cur_language)

	return render(request, 'cart/cart_detail.html', context)