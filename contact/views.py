from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string


from .forms import ContactForm
# Create your views here.

def form_submit(request):
	form = ContactForm(request.POST or None)
	if request.POST :
		if form.is_valid():
			contact_msg = form.save()
			# Get parameters for email template rendering
			contact_msg_full_admin_url = 'http://' + request.get_host() + contact_msg.get_admin_url()
			context = {
				'contact_msg': contact_msg,
				'contact_msg_full_admin_url': contact_msg_full_admin_url,
			}
			email_text = render_to_string('emails/new_contact_admin_alert.txt', context)
			email_html = render_to_string('emails/new_contact_admin_alert.html', context)

			# Send an email to admin's email
			subject = 'New Contact Message - Chile Raids'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = ['',] ## ADMINS' EMAILS GO HERE.

			send_mail(
				subject,				#Subject
				email_text,				#Message_text
				email_from,				#Email Sender Address
				recipient_list,			#Email Receiver Address
				html_message=email_html,#Message_HTML
			)
			# After successful post, redirect to contact section of homepage. with a message.
			messages.success(request, 'Your contact message was sent successfully! We\'ll contact you as soon as possible.')

			return redirect (reverse ('raidchileapp:home')+'#contact')

	# If the request is GET, just return to the contact section in home template.
	return redirect (reverse ('raidchileapp:home')+'#contact')