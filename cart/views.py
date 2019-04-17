from decimal import Decimal

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from raidchileapp.models import Category, Tour

from .cart import Cart
from .forms import CartAddProductForm

# Create you shopping cart views here:
@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Tour, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(
			product=product,
			adult_qty=cd['adult_quantity'],
			children_qty=cd['children_quantity'],
			update_quantity=cd['update']
		)
	return redirect('cart:cart_detail')

@require_POST
def cart_add_combo(request, combo_slug):
	cart = Cart(request)
	products = Tour.objects.filter(
		Q(available=True) & (
			Q(categories__slug_es=combo_slug) |
			Q(categories__slug_en=combo_slug) |
			Q(categories__slug_pt_BR=combo_slug)
		)
	)
	if not products:
		raise Http404("No Tour matches the given query.")

	form = CartAddProductForm(request.POST)
	if form.is_valid():
		for product in products:
			cd = form.cleaned_data
			cart.add(
				product=product,
				adult_qty=cd['adult_quantity'],
				children_qty=cd['children_quantity'],
				update_quantity=cd['update']
			)
	return redirect('cart:cart_detail')


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Tour, id=product_id)
	cart.remove(product)
	return redirect('cart:cart_detail')


def cart_detail(request):
	cart = Cart(request)
	combo = False
	if cart['combo_id']:
		combo = Category.objects.filter(id=cart['combo_id'], available=True).first()
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
			discount += Decimal(item['adult_qty'] + item['children_qty']) * combo.combo_discount


	context = {
		'cart': cart,
		'combo': combo,
		'subtotal': subtotal,
		'discount': discount,
		'total': subtotal-discount,
	}
	return render(request, 'cart/cart_detail.html', context)