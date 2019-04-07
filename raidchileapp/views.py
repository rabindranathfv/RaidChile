from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Category, Feature, Location, Tour, TourImage
from .forms import CommentForm, ContactForm, SearchForm

##################################
def tour_filter_search(request, queryset, search_form):
	# Verify querystring parameters integrity.
	# Delete non-form and empty fields from the get request.
	form_fields = search_form.fields.keys()
	filter_parameters = { k:v for k,v in request.GET.items() if k in form_fields and k != 'locations' and v }

	if 'locations' in request.GET.keys():
		# Using getlist to obtain the multiple choices
		filter_parameters['locations'] = request.GET.getlist('locations')

	# Validating parameters data type and constraints
	# Constraint: Max price > min price else swap them.
	min_price = filter_parameters.get('min_price', None)
	max_price = filter_parameters.get('max_price', None)
	if (min_price and max_price) and (max_price < min_price):
		filter_parameters['min_price'], filter_parameters['max_price'] = filter_parameters['max_price'], filter_parameters['min_price']

	# Filtering tours depending on existing filter parameters
	# Locations
	if filter_parameters.get('locations', None):
		queryset = queryset.filter(locations__in=filter_parameters['locations'])
	# Min Price
	if filter_parameters.get('min_price', None):
		queryset = queryset.filter(Q(adult_reg_price__gte=filter_parameters['min_price']) | Q(adult_sale_price__gte=filter_parameters['min_price']))
	# Max Price
	if filter_parameters.get('max_price', None):
		queryset = queryset.filter(Q(adult_reg_price__lte=filter_parameters['max_price']) | Q(adult_sale_price__lte=filter_parameters['max_price']))

	return queryset

##################################
def home(request):
	contact_form = ContactForm()
	search_form = SearchForm()
	categories = Category.objects.all()[:4] # First 4 categories
	context = {
		'categories': categories,
		'contact_form': contact_form,
		'search_form': search_form
	}
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
	search_form = SearchForm(request.GET or None)
	categories = Category.objects.all()
	tours = Tour.objects.filter(available=True)

	# If there are querystring parameters present in the url, proceed to filter tours.
	if request.GET:
		tours = tour_filter_search(request, tours, search_form)

	context = {
		'tours': tours,
		'categories': categories,
		'search_form': search_form,
	}
	return render(request, "raidchileapp/tour_search.html", context)


def tour_search_by_category(request, category_slug):
	search_form = SearchForm(request.GET or None)
	categories = Category.objects.all()
	category = get_object_or_404(Category, slug=category_slug)
	tours = Tour.objects.filter(available=True, categories__in=[category.id])
	print ("HOLA!!")
	print (tours)
	print (category, category.id)
	# If there are querystring parameters present in the url, proceed to filter tours.
	if request.GET:
		tours = tour_filter_search(request, tours, search_form)

	print ("HOLA!!")
	print (tours)
	print (category)

	context = {
		'tours': tours,
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