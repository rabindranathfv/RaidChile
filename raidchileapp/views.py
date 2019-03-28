from django.shortcuts import render

from .forms import ContactForm, MailListForm

# Create your views here.
def home(request):
	contact_form = ContactForm()
	mail_form = MailListForm()
	context = {'contact_form': contact_form, 'mail_form': mail_form }
	return render(request, "raidchileapp/home.html", context)