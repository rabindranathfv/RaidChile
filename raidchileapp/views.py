from django.shortcuts import render, get_object_or_404

from .models import Category, Feature, Location, Tour, TourImage
from .forms import CommentForm, ContactForm, MailListForm, SearchForm



def home(request):
	contact_form = ContactForm()
	mail_form = MailListForm()
	search_form = SearchForm()
	context = {'contact_form': contact_form, 'mail_form': mail_form, 'search_form': search_form }
	return render(request, "raidchileapp/home.html", context)


def tour_details(request, id, slug):
	tour = get_object_or_404(Tour, id=id, slug=slug, available=True)
	comment_form = CommentForm()
	context = {
		'tour': tour,
		'comment_form': comment_form,
	}
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