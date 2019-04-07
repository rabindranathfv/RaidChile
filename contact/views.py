from django.contrib import messages
from django.shortcuts import render, redirect, reverse

from .forms import ContactForm
# Create your views here.

def form_submit(request):
	form = ContactForm(request.POST or None)
	if request.POST :
		if form.is_valid():
			form.save()
			# Send an email to admin's email

			# After successful post, redirect to contact section of homepage. with a message.
			messages.success(request, 'Your contact message was sent successfully! We\'ll contact you as soon as possible.')
			return redirect (reverse ('raidchileapp:home')+'#contact')

	# If the request is GET, just return to the contact section in home template.
	return redirect (reverse ('raidchileapp:home')+'#contact')