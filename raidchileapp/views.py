from django.shortcuts import render

from .forms import CommentForm, ContactForm, MailListForm, SearchForm

# Create your views here.
def home(request):
	contact_form = ContactForm()
	mail_form = MailListForm()
	search_form = SearchForm()
	context = {'contact_form': contact_form, 'mail_form': mail_form, 'search_form': search_form }
	return render(request, "raidchileapp/home.html", context)

def tour_details(request, id, slug):
	comment_form = CommentForm()
	context = {'comment_form': comment_form}
	return render(request, "raidchileapp/tour_details.html", context)

def tour_search_by_category(request, category_slug):
	search_form = SearchForm()
	context = {'search_form': search_form }
	return render(request, "raidchileapp/tour_search.html", context)

# Template testing views
def tour_details_dummy(request):
	comment_form = CommentForm()
	context = {'comment_form': comment_form}
	return render(request, "raidchileapp/tour_details.html", context)

def tour_search_dummy(request):
	search_form = SearchForm()
	context = {'search_form': search_form }
	return render(request, "raidchileapp/tour_search.html", context)