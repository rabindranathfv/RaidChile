import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string

from .forms import ContactForm
# Create your views here.

#Captcha Validation Fuction
def is_captcha_valid(request):
	''' Begin reCAPTCHA validation '''
	recaptcha_response = request.POST.get('g-recaptcha-response')
	url = 'https://www.google.com/recaptcha/api/siteverify'
	values = {
		'secret': settings.RECAPTCHA_SECRET_KEY,
		'response': recaptcha_response
	}
	data = urllib.parse.urlencode(values).encode()
	req =  urllib.request.Request(url, data=data)
	response = urllib.request.urlopen(req)
	result = json.loads(response.read().decode())
	''' End reCAPTCHA validation '''
	if result['success']:
		return True

	return False





def form_submit(request):
	form = ContactForm(request.POST or None)
	if request.POST :
		if form.is_valid():

			# Validate captcha
			if is_captcha_valid(request):

				contact_msg = form.save()
				# Get parameters for email template rendering
				contact_msg_full_admin_url = request.scheme + '://' + request.get_host() + contact_msg.get_admin_url()
				context = {
					'contact_msg': contact_msg,
					'contact_msg_full_admin_url': contact_msg_full_admin_url,
				}
				email_text = render_to_string('emails/new_contact_admin_alert.txt', context)
				email_html = render_to_string('emails/new_contact_admin_alert.html', context)
				# Obtain the recipients list from the user group called "Emails"
				recipients_list = list(User.objects.filter(groups__name='Emails', is_staff=True).values_list('email', flat=True))
				print (recipients_list)
				# Send an email to admin's email
				subject = 'New Contact Message - Chile Raids'
				email_from = settings.EMAIL_HOST_USER

				send_mail(
					subject,				#Subject
					email_text,				#Message_text
					email_from,				#Email Sender Address
					recipients_list,			#Email Receiver Address
					html_message=email_html,#Message_HTML
				)
				#After successful post, redirect to contact section of homepage. with a message.
				messages.success(request, 'Your contact message was sent successfully! We\'ll contact you as soon as possible.')
			else:
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')

			return redirect (reverse ('raidchileapp:home')+'#contact')

	# If the request is GET, just return to the contact section in home template.
	return redirect (reverse ('raidchileapp:home')+'#contact')