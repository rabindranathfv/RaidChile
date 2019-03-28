from django.shortcuts import render

from .forms import ContactForm

# Create your views here.
def home(request):
	contact_form = ContactForm()
	context = {'contact_form': contact_form }
	return render(request, "raidchileapp/home.html", context)