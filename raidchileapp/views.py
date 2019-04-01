from django.shortcuts import render

from .forms import CommentForm, ContactForm, MailListForm, SearchForm

# Create your views here.
def home(request):
	contact_form = ContactForm()
	mail_form = MailListForm()
	search_form = SearchForm()
	context = {'contact_form': contact_form, 'mail_form': mail_form, 'search_form': search_form }
	return render(request, "raidchileapp/home.html", context)

def tour_details(request):
	comment_form = CommentForm()
	context = {'comment_form': comment_form}
	return render(request, "raidchileapp/tour_details.html", context)