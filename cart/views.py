from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from raidchileapp.models import Tour

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


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Tour, id=product_id)
	cart.remove(product)
	return redirect('cart:cart_detail')


def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		add_form = CartAddProductForm(
			initial={
				'adult_quantity': item['adult_qty'],
				'children_quantity': item['children_qty'],
				'update': True,
			}
		)
		item['update_quantity_form'] = add_form
	return render(request, 'cart/cart_detail.html', {'cart': cart})