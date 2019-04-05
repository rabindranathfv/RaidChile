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


def search_all_tours(request):
	tours = None
	search_form = SearchForm(request.GET or None)
	categories = Category.objects.all()

	# If there are querystring parameters present in the url, proceed to filter tours.
	if request.GET:
		# Verify querystring parameters integrity.
		print ("Busqueda con Filtros.", request.GET)
		# Filter tours
	else:
		# Return all the tours, without filtering, not retrieving their description or features.
		print ("Busqueda SIN Filtros!")
		tours = Tour.objects.defer('description').filter(available=True)


	context = {
		'tours': tours,
		'categories': categories,
		'search_form': search_form,
	}
	return render(request, "raidchileapp/tour_search.html", context)


def tour_search_by_category(request, category_slug):
	search_form = SearchForm()
	categories = Category.objects.all()
	category = get_object_or_404(Category, slug=category_slug)

	context = {
		'category': category,
		'categories': categories,
		'search_form': search_form,
	}
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