from django.shortcuts import render, redirect

from cart.cart import Cart

from .models import OrderItem
from .forms import OrderCreateForm

# Create an reservation order to persist the user confirmed reservations into the database
def order_create(request):
	cart = Cart(request)
	form = OrderCreateForm(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():
			print ('FORM IS VALID')
			order = form.save()
			# Create an reservation per tour in the cart
			for item in cart:
				OrderItem.objects.create(
					order = order,
					product = item['product'],
					adult_reg_price = item['adult_reg_price'],
					adult_sale_price = item['adult_sale_price'],
					children_reg_price = item['children_reg_price'],
					children_sale_price= item['children_sale_price'],
					adult_quantity=item['adult_qty'],
					children_quantity=item['children_qty']
				)
			cart.clear()
			# Send email to the reserver's email address
			return redirect('orders:order_create_success')

	return render(request, 'orders/order_create.html', {'form': form})


def order_create_success(request):
	return render(request, 'orders/order_create_success.html')