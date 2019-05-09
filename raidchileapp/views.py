from decimal import Decimal

from django.db.models import Avg, Count, Q, Prefetch, Max
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _

from cart.forms import CartAddProductForm
from contact.forms import ContactForm

from .models import Category, Feature, Location, Tour, Combo, TourImage, Review
from .forms import ReviewForm, SearchForm

##################################
def tour_filter_search(request, queryset, search_form, sale_price_filter=False):
	# Verify querystring parameters integrity.
	# Delete non-form and empty fields from the get request.
	form_fields = search_form.fields.keys()
	filter_parameters = { k:v for k,v in request.GET.items() if k in form_fields and k != 'locations' and v }

	## Adding primitive search function by word coincidence:
	search_words = None

	# If there are search terms, filter tours by their title (depends on the language)
	if filter_parameters.get('search_terms', None):
		search_words = filter_parameters['search_terms'].split(" ", 5)
		cur_language = translation.get_language()
		for word in search_words:
			if cur_language == 'es':
				queryset = queryset.filter(name_es__icontains=word)
			elif cur_language == 'pt-br':
				queryset = queryset.filter(name_pt_BR__icontains=word)
			else:
				queryset = queryset.filter(name_en__icontains=word)

	if 'locations' in request.GET.keys():
		# Using getlist to obtain the multiple choices
		filter_parameters['locations'] = request.GET.getlist('locations')

	# Validating parameters data type and constraints
	# Constraint: Max price > min price else swap them.
	min_price = Decimal(filter_parameters.get('min_price', 0))
	max_price = Decimal(filter_parameters.get('max_price', 0))
	if (min_price and max_price) and (max_price < min_price):
		min_price, max_price = max_price, min_price
		filter_parameters['min_price'], filter_parameters['max_price'] = filter_parameters['max_price'], filter_parameters['min_price']

	# Filtering tours depending on existing filter parameters
	# Locations
	if filter_parameters.get('locations', None):
		queryset = queryset.filter(locations__in=filter_parameters['locations'])
	# Min Price
	if filter_parameters.get('min_price', None):
		if sale_price_filter:
			queryset = queryset.filter(Q(adult_sale_price__gte=min_price))
		else:
			queryset = queryset.filter(Q(adult_reg_price__gte=min_price))

	# Max Price
	if filter_parameters.get('max_price', None):
		if sale_price_filter:
			queryset = queryset.filter(Q(adult_sale_price__lte=max_price))
		else:
			queryset = queryset.filter(Q(adult_reg_price__lte=max_price))
	return queryset

##################################  Views  ##################################
def home(request):
	contact_form = ContactForm(request.POST or None)
	search_form = SearchForm()
	combos = Combo.objects.filter(available=True).order_by('name_es').annotate(Count('tours')).prefetch_related('image')[:4] # First 4 combos

	context = {
		'combos': combos,
		'contact_form': contact_form,
		'search_form': search_form,
	}

	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = reverse('raidchileapp:home')
		translation.activate('en')
		context['redirect_url_en'] = reverse('raidchileapp:home')
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = reverse('raidchileapp:home')
	finally:
		translation.activate(cur_language)

	return render(request, "raidchileapp/home.html", context)


def tour_details(request, id, slug):
	try:
		tour = Tour.objects.prefetch_related('reviews').get(
			Q(available=True) &
			Q(id=id) & (
				Q(slug_es=slug) |
				Q(slug_en=slug) |
				Q(slug_pt_BR=slug)
			)
		)
	except Tour.DoesNotExist:
		raise Http404("No Tour matches the given query.")
	# Initialize the cart_add_ Product form with the minimun number of passengers
	cart_product_form = CartAddProductForm(
		initial={
			'adult_quantity': tour.min_pax_number,
		}
	)
	review_form = ReviewForm(initial={'product':tour, 'rating':3})
	print (review_form)
	review_list = tour.reviews.filter(visible=True)

	reviews_data = {'total_reviews': review_list.count()}
	avg_reviews = review_list.aggregate(avg_reviews=Avg('rating'))
	reviews_data = {**reviews_data, **avg_reviews}

	context = {
		'tour': tour,
		'review_list' : review_list[:5],
		'rating_range' : list(range(1,6)),
		'reviews_data': reviews_data,
		'cart_product_form' : cart_product_form,
	}

	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = tour.get_absolute_url()
		translation.activate('en')
		context['redirect_url_en'] = tour.get_absolute_url()
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = tour.get_absolute_url()
	finally:
		translation.activate(cur_language)

	# Reviews form processing
	if request.method == 'POST':
		review_form  = ReviewForm(request.POST)
		print('Entered POST')
		if review_form.is_valid():
			print('Form valid: Saving and redirecting')
			review_form.save()
			return redirect("raidchileapp:tour_details", id=id, slug=slug)
		else:
			print(review_form.errors)
			print(review_form.cleaned_data)

	context['review_form'] = review_form
	return render(request, "raidchileapp/tour_details.html", context)


def search_all_tours(request):
	search_form = SearchForm(request.GET or None)
	categories = Category.objects.filter(available=True)
	tours = Tour.objects.filter(available=True).prefetch_related('features', 'images')

	# If there are querystring parameters present in the url, proceed to filter tours.
	if request.GET:
		tours = tour_filter_search(request, tours, search_form)

	context = {
		'type': 'tour',
		'tours': tours,
		'categories': categories,
		'search_form': search_form,
	}

	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = reverse('raidchileapp:search_all_tours')
		translation.activate('en')
		context['redirect_url_en'] = reverse('raidchileapp:search_all_tours')
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = reverse('raidchileapp:search_all_tours')
	finally:
		translation.activate(cur_language)

	return render(request, "raidchileapp/tour_search.html", context)


def tour_search_by_category(request, category_slug):
	search_form = SearchForm(request.GET or None)
	categories = Category.objects.filter(available=True)
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

	# If there are querystring parameters present in the url, proceed to filter tours.
	if request.GET:
		tours = tour_filter_search(request, tours, search_form)

	context = {
		'type': 'tour',
		'tours': tours,
		'category': category,
		'categories': categories,
		'search_form': search_form,
	}

		# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = category.get_absolute_url()
		translation.activate('en')
		context['redirect_url_en'] = category.get_absolute_url()
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = category.get_absolute_url()
	finally:
		translation.activate(cur_language)

	return render(request, "raidchileapp/tour_search.html", context)


def combo_details(request, id, slug):
	try:
		combo = Combo.objects.prefetch_related('tours').get(
			Q(available=True) &
			Q(id=id) & (
				Q(slug_es=slug) |
				Q(slug_en=slug) |
				Q(slug_pt_BR=slug)
			)
		)
	except Combo.DoesNotExist:
		raise Http404("No Tour Combo matches the given query.")
	# Initialize the cart_add_ Product form with the minimun number of passengers
	cart_product_form = CartAddProductForm(
		initial={
			'adult_quantity': combo.min_pax_number,
		}
	)

	context = {
		'combo': combo,
		'cart_product_form' : cart_product_form,
	}

	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = combo.get_absolute_url()
		translation.activate('en')
		context['redirect_url_en'] = combo.get_absolute_url()
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = combo.get_absolute_url()
	finally:
		translation.activate(cur_language)

	return render(request, "raidchileapp/combo_details.html", context)


def search_all_combos(request):
	search_form = SearchForm(request.GET or None)
	categories = Category.objects.filter(available=True)
	combos = Combo.objects.filter(available=True).prefetch_related('image')

	if request.GET:
		combos = tour_filter_search(request, combos, search_form, sale_price_filter=True)

	context = {
		'type': 'combo',
		'combos': combos.annotate(Count('tours')),
		'categories': categories,
		'search_form': search_form,
	}

	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = reverse('raidchileapp:search_all_combos')
		translation.activate('en')
		context['redirect_url_en'] = reverse('raidchileapp:search_all_combos')
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = reverse('raidchileapp:search_all_combos')
	finally:
		translation.activate(cur_language)

	return render(request, "raidchileapp/combo_search.html", context)


def tour_detail_in_combo(request, id, slug, tour_id):
	try:
		combo = Combo.objects.prefetch_related('tours').get(
			Q(available=True) &
			Q(id=id) & (
				Q(slug_es=slug) |
				Q(slug_en=slug) |
				Q(slug_pt_BR=slug)
			)
		)
		tour = combo.tours.prefetch_related('images').get(id=tour_id)
	except Combo.DoesNotExist:
		raise Http404("No Tour Combo matches the given query.")
	except Tour.DoesNotExist:
		raise Http404("No Tour matches the given query.")

	cart_product_form = CartAddProductForm(
		initial={
			'adult_quantity': tour.min_pax_number,
		}
	)
	comment_form = CommentForm()
	context = {
		'in_combo': True,
		'combo': combo,
		'tour': tour,
		'comment_form': comment_form,
		'cart_product_form' : cart_product_form,
	}

	# Set language switcher urls
	cur_language = translation.get_language()
	try:
		translation.activate('es')
		context['redirect_url_es'] = reverse('raidchileapp:tour_detail_in_combo', args=[combo.id, combo.slug_es, tour.id])
		translation.activate('en')
		context['redirect_url_en'] = reverse('raidchileapp:tour_detail_in_combo', args=[combo.id, combo.slug_en, tour.id])
		translation.activate('pt-br')
		context['redirect_url_pt_BR'] = reverse('raidchileapp:tour_detail_in_combo', args=[combo.id, combo.slug_pt_BR, tour.id])
	finally:
		translation.activate(cur_language)

	return render(request, "raidchileapp/tour_details.html", context)
