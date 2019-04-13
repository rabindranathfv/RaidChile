from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string

from cart.cart import Cart
from raidchileapp.models import Category

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
			subtotal = Decimal(0)
			discount = Decimal(0)
			combo = False
			if cart['combo_id']:
				combo = Category.objects.filter(id=cart['combo_id'], available=True).first()
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
				# calculate regular subtotal and combo discount.
				subtotal += Decimal(item['adult_qty']) * item['adult_reg_price'] + Decimal(item['children_qty']) * item['children_reg_price']
				if combo:
					discount += Decimal(item['adult_qty'] + item['children_qty']) * combo.combo_discount

			# Get parameters for email template rendering
			contact_url = request.scheme + '://' + request.get_host() + reverse('raidchileapp:home') + "#contact"
			context = {
				'order': order,
				'combo': combo,
				'contact_url': contact_url,
				'subtotal': subtotal,
				'discount': discount,
				'total': subtotal-discount,
			}
			email_text = render_to_string('emails/user_reservation_confirmation.txt', context)
			email_html = render_to_string('emails/user_reservation_confirmation.html', context)

			# Send email to the reserver's email address
			subject = 'Tour Reservations Confirmed! - Chile Raids'
			email_from = settings.EMAIL_HOST_USER
			email_to = [ order.email, ] ## RESERVER'S EMAIL ADDRESS GOES HERE.
			email_bcc = list(User.objects.filter(groups__name='Emails', is_staff=True).values_list('email', flat=True))

			# Create the email, and attach the HTML version as well.
			msg = EmailMultiAlternatives(subject, email_text, email_from, email_to, bcc=email_bcc)
			msg.attach_alternative(email_html, "text/html")

			msg.send()
			#Clear the session based cart
			cart.clear()

			return redirect('orders:order_create_success')

	return render(request, 'orders/order_create.html', {'form': form})


def order_create_success(request):
	return render(request, 'orders/order_create_success.html')