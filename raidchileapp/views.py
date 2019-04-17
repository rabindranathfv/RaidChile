from django.db.models import Count, Q, Prefetch, Max
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import translation
from django.utils.translation import gettext as _

from cart.forms import CartAddProductForm
from contact.forms import ContactForm

from .models import Category, Feature, Location, Tour, TourImage
from .forms import CommentForm, SearchForm

##################################
def tour_filter_search(request, queryset, search_form):
	# Verify querystring parameters integrity.
	# Delete non-form and empty fields from the get request.
	form_fields = search_form.fields.keys()
	filter_parameters = { k:v for k,v in request.GET.items() if k in form_fields and k != 'locations' and v }

	## Adding primitive search function by word coincidence:
	search_words = None

	if filter_parameters.get('search_terms', None):
		search_words = filter_parameters['search_terms'].split(" ", 5)
		for word in search_words:
			queryset = queryset.filter(name__icontains=word)


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
	contact_form = ContactForm(request.POST or None)
	search_form = SearchForm()
	categories = Category.objects.filter(available=True, combo=True).annotate(Count('tour')).prefetch_related('image')[:4] # First 4 categories

	context = {
		'categories': categories,
		'contact_form': contact_form,
		'search_form': search_form
	}

	return render(request, "raidchileapp/home.html", context)


def tour_details(request, id, slug):
	tour = get_object_or_404(Tour, id=id, slug=slug, available=True)

	# Initialize the cart_add_ Product form with the minimun number of passengers
	cart_product_form = CartAddProductForm(
		initial={
			'adult_quantity': tour.min_pax_number,
		}
	)
	comment_form = CommentForm()
	context = {
		'tour': tour,
		'comment_form': comment_form,
		'cart_product_form' : cart_product_form,
	}

	return render(request, "raidchileapp/tour_details.html", context)


def search_all_tours(request):
	search_form = SearchForm(request.GET or None)
	categories = Category.objects.filter(combo=False, available=True)
	combos = Category.objects.filter(combo=True, available=True)
	tours = Tour.objects.filter(available=True).prefetch_related('features', 'images')

	# If there are querystring parameters present in the url, proceed to filter tours.
	if request.GET:
		tours = tour_filter_search(request, tours, search_form)

	context = {
		'tours': tours,
		'categories': categories,
		'combos': combos,
		'search_form': search_form,
	}
	return render(request, "raidchileapp/tour_search.html", context)


def tour_search_by_category(request, category_slug):
	search_form = SearchForm(request.GET or None)
	categories = Category.objects.filter(combo=False, available=True)
	combos = Category.objects.filter(combo=True, available=True)
	try:
		category = Category.objects.get(
			Q(available=True) & (
				Q(slug_es=category_slug) |
				Q(slug_en=category_slug) |
				Q(slug_pt_BR=category_slug)
			)
		)
	except Category.DoesNotExist:
		raise Http404("No Category matches the given query.")
	tours = Tour.objects.filter(available=True, categories__in=[category.id]).prefetch_related('features', 'images')
	min_pax = None

	# Calculate minimun passenger of combo = larges amount of all tours.
	if category.combo:
		min_pax = tours.aggregate(Max('min_pax_number'))


	# If there are querystring parameters present in the url, proceed to filter tours.
	if request.GET and not category.combo:
		tours = tour_filter_search(request, tours, search_form)

	context = {
		'tours': tours,
		'category': category,
		'combos': combos,
		'categories': categories,
		'search_form': search_form,
	}


	# If the category is a combo, don't display the filters or search bar.
	if category.combo :
		context['min_pax'] = min_pax['min_pax_number__max'] or 0
		# Initialize reservation miniform
		cart_product_form = CartAddProductForm(
			initial={
				'adult_quantity': min_pax['min_pax_number__max'] or 0,
			}
		)
		context['cart_product_form'] = cart_product_form
		return render(request, "raidchileapp/tour_combo.html", context)

	return render(request, "raidchileapp/tour_search.html", context)