from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse


from .forms import ContactForm
# Create your views here.

def form_submit(request):
	form = ContactForm(request.POST or None)
	if request.POST :
		if form.is_valid():
			contact_msg = form.save()
			contact_msg_full_admin_url = request.get_host() + contact_msg.get_admin_url()

			# Send an email to admin's email
			subject = 'New Contact Message - Chile Raids'
			message =  'This is the link to the see the message:\n\n' + contact_msg_full_admin_url
			email_from = settings.EMAIL_HOST_USER
			recipient_list = ['',] ## ADMINS' EMAILS GO HERE.

			send_mail( subject, message, email_from, recipient_list )
			# After successful post, redirect to contact section of homepage. with a message.
			messages.success(request, 'Your contact message was sent successfully! We\'ll contact you as soon as possible.')

			return redirect (reverse ('raidchileapp:home')+'#contact')

	# If the request is GET, just return to the contact section in home template.
	return redirect (reverse ('raidchileapp:home')+'#contact')