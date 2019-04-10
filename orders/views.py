from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string

from cart.cart import Cart

from .models import OrderItem
from .forms import OrderCreateForm

# Create an reservation order to persist the user confirmed reservations into the database
def order_create(request):
	cart = Cart(request)
	# Redirect to the cart details if there are no items in the cart.
	if not cart:
		return redirect('cart:cart_detail')

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
			# Get parameters for email template rendering
			contact_url = self.request.scheme + '://' + request.get_host() + reverse('raidchileapp:home') + "#contact"
			context = {
				'order': order,
				'contact_url': contact_url,
			}
			email_text = render_to_string('emails/user_reservation_confirmation.txt', context)
			email_html = render_to_string('emails/user_reservation_confirmation.html', context)

			# Send email to the reserver's email address
			subject = 'Tour Reservations Confirmed! - Chile Raids'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [ order.email, ] ## RESERVER'S EMAIL ADDRESS GOES HERE.

			send_mail(
				subject,				#Subject
				email_text,				#Message_text
				email_from,				#Email Sender Address
				recipient_list,			#Email Receiver Address
				html_message=email_html,#Message_HTML
			)
			return redirect('orders:order_create_success')

	return render(request, 'orders/order_create.html', {'form': form})


def order_create_success(request):
	return render(request, 'orders/order_create_success.html')