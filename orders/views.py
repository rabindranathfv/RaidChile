from decimal import Decimal

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation
from django.utils.html import strip_tags
from django.utils.translation import gettext as _

from cart.cart import Cart
from raidchileapp.models import Combo

from .models import OrderItem
from .forms import OrderCreateForm


def get_email_html_translated(language, template, context):
	with translation.override(language):
		return render_to_string(template, context)


# Create an reservation order to persist the user confirmed reservations into the database
def order_create(request):
	cart = Cart(request)
	# Redirect to the cart details if there are no items in the cart.
	if not cart:
		return redirect('cart:cart_detail')

	form = OrderCreateForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			#print ('FORM IS VALID')
			order = form.save()
			subtotal = Decimal(0)
			discount = Decimal(0)
			combo = False
			if cart['combo_id']:
				combo = get_object_or_404(Combo, id=cart['combo_id'], available=True)
			# Create a reservation order item per tour in the cart
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
				# calculate regular subtotal and combo discountes price of applicable.
				subtotal += Decimal(item['adult_qty']) * item['adult_reg_price'] + Decimal(item['children_qty']) * item['children_reg_price']
				if combo:
					discount += Decimal(item['adult_qty']) * (item['adult_reg_price'] - item['adult_sale_price']) + Decimal(item['children_qty']) * (item['children_reg_price'] - item['children_sale_price'])

			## Send an email to the reserver in their browsing language.
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
			email_html = render_to_string('emails/user_reservation_confirmation.html', context)
			email_text = strip_tags(email_html)
			#print (email_text)
			subject = _('Tour Reservations Confirmed! - Chile Raid')
			email_from = settings.EMAIL_HOST_USER
			email_to = [ order.email, ] ## RESERVER'S EMAIL ADDRESS GOES HERE.
			admin_emails = list(User.objects.filter(groups__name='Emails', is_staff=True).values_list('email', flat=True))

			# Create the email, and attach the HTML version as well.
			msg = EmailMultiAlternatives(subject, email_text, email_from, email_to)
			msg.attach_alternative(email_html, "text/html")
			msg.send()

			## Send an email to the admins(if any) in forced Spanish language.
			if admin_emails:
				subject2 = 'An User Has Confirmed New Tour Reservations - Chile Raid'
				order_admin_url = request.scheme + '://' + request.get_host() + order.get_admin_url()
				cur_language = translation.get_language()
				try:
					translation.activate('es')
					subject2 = _('An User Has Confirmed New Tour Reservations - Chile Raid')
					order_admin_url = request.scheme + '://' + request.get_host() + order.get_admin_url()
				finally:
					translation.activate(cur_language)
				## Parse admin html forcing spanish language
				context['order_admin_url'] = order_admin_url
				email_html = get_email_html_translated('es','emails/admin_reservation_confirmation.html', context)
				email_text = strip_tags(email_html)
				#print (email_text)
				msg2 = EmailMultiAlternatives(subject2, email_text, email_from, admin_emails)
				msg2.attach_alternative(email_html, "text/html")
				msg2.send()

			#Clear the session based cart and redirect to success page
			cart.clear()
			return redirect('orders:order_create_success')

	context = {'form': form}
	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = reverse('orders:order_create')
		translation.activate('en')
		context['redirect_url_en'] = reverse('orders:order_create')
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = reverse('orders:order_create')
	finally:
		translation.activate(cur_language)

	return render(request, 'orders/order_create.html', context)


def order_create_success(request):
	context = dict()
	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = reverse('orders:order_create_success')
		translation.activate('en')
		context['redirect_url_en'] = reverse('orders:order_create_success')
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = reverse('orders:order_create_success')
	finally:
		translation.activate(cur_language)
	return render(request, 'orders/order_create_success.html', context)