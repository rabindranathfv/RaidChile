from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.
# Vertical distribution is for better 'git diff' readability
class Category(models.Model):
	name_en = models.CharField(
		max_length=150,
		verbose_name=_('name (in English)')
	)
	name_es = models.CharField(
		max_length=150,
		verbose_name=_('name (in Spanish)')
	)
	name_pt_BR = models.CharField(
		max_length=150,
		verbose_name=_('name (in Portuguese)')
	)
	slug_en = models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True,
		verbose_name=_('slug (in English)')
	)
	slug_es= models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True,
		verbose_name=_('slug (in Spanish)')
	)
	slug_pt_BR= models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True,
		verbose_name=_('slug (in Portuguese)')
	)
	image = models.ForeignKey(
		'TourImage',
		blank=True,
		null=True,
		related_name='categories',
		related_query_name='category',
		on_delete=models.SET_NULL,
		verbose_name=_('image')
	)
	available = models.BooleanField(
		default=True,
		verbose_name=_('available')
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('created at')
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name=_('updated at')
	)

	class Meta:
		ordering = ('name_es', )
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	def __str__(self):
		cur_language = translation.get_language()
		if cur_language == 'es':
			return self.name_es
		elif cur_language == 'pt-br':
			return self.name_pt_BR
		else:
			return self.name_en

	def get_absolute_url(self):
		cur_language = translation.get_language()
		if cur_language == 'es':
			return reverse('raidchileapp:tour_search_by_category', args=[self.slug_es])
		elif cur_language == 'pt-br':
			return reverse('raidchileapp:tour_search_by_category', args=[self.slug_pt_BR])
		else:
			return reverse('raidchileapp:tour_search_by_category', args=[self.slug_en])



class Feature(models.Model):
	name_en = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name (in English)')
	)
	name_es = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name (in Spanish)')
	)
	name_pt_BR = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name (in Portuguese)')
	)
	icon = models.CharField(max_length=150,
		default="fa-eye",
		help_text=_('String from Font Awesome icons e.g. "fa-eye"'),
		verbose_name=_('icon')
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('created at')
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name=_('updated at')
	)

	class Meta:
		ordering = ('-created_at', )
		verbose_name = _('feature')
		verbose_name_plural = _('features')

	def __str__(self):
		cur_language = translation.get_language()
		if cur_language == 'es':
			return self.name_es
		elif cur_language == 'pt-br':
			return self.name_pt_BR
		else:
			return self.name_en

	# Method to display icon image tag inside django admin
	def icon_image(self):
		icon_class= 'fa-eye'
		if self.icon.strip().startswith('fa'):
			icon_class = self.icon.strip()
		return mark_safe('<i class="fa %s fa-3x"></i>' % (icon_class))
	icon_image.short_description = _('Icon image')



class Location(models.Model):
	name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name')
	)
	region = models.CharField(
		max_length=150,
		db_index=True,
		blank=True,
		verbose_name=_('region'),
		help_text=_('Helps users to search by coincidence.')
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('created at')
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name=_('updated at')
	)

	class Meta:
		ordering = ('name', )
		verbose_name = _('location')
		verbose_name_plural = _('locations')

	def __str__(self):
		return self.name



class Product(models.Model):
	PRODUCT_CHOICES = (
		('TOUR', _('Tour')),
		('COMBO', _('Combo'))
	)
	name_en = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name (in English)')
	)
	name_es = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name (in Spanish)')
	)
	name_pt_BR = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name (in Portuguese)')
	)
	categories = models.ManyToManyField(
		Category,
		blank=True,
		related_name='products',
		related_query_name='product',
		verbose_name=_('categories')
	)
	available = models.BooleanField(
		default=True,
		verbose_name=_('available')
	)
	slug_en = models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True,
		verbose_name=_('slug (in English)')
	)
	slug_es= models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True,
		verbose_name=_('slug (in Spanish)')
	)
	slug_pt_BR= models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True,
		verbose_name=_('slug (in Portuguese)')
	)
	product_type = models.CharField(
		choices=PRODUCT_CHOICES,
		max_length=5,
		verbose_name=_('type of product')
	)
	description_en = models.TextField(
		verbose_name=_('description (in English)'),
		help_text=_('Long if tour. Short if Combo.')
	)
	description_es = models.TextField(
		verbose_name=_('description (in Spanish)'),
		help_text=_('Long if tour. Short if Combo.')
	)
	description_pt_BR = models.TextField(
		verbose_name=_('description (in Portuguese)'),
		help_text=_('Long if tour. Short if Combo.')
	)
	min_pax_number = models.PositiveSmallIntegerField(
		default=1,
		verbose_name=_('minimum passenger number')
	)
	adult_reg_price = models.DecimalField(
		default = Decimal(0),
		max_digits=10,
		decimal_places=2,
		verbose_name=_('adults\' regular price')
	)
	children_reg_price = models.DecimalField(
		default = Decimal(0),
		max_digits=10,
		decimal_places=2,
		verbose_name=_('children\'s regular price')
	)
	adult_sale_price = models.DecimalField(
		default = Decimal(0),
		max_digits=10,
		decimal_places=2,
		verbose_name=_('adults\' sale price')
	)
	children_sale_price = models.DecimalField(
		default = Decimal(0),
		max_digits=10,
		decimal_places=2,
		verbose_name=_('children\'s sale price')
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('created at')
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name=_('updated at')
	)
	def __str__(self):
		cur_language = translation.get_language()
		if cur_language == 'es':
			return self.name_es
		elif cur_language == 'pt-br':
			return self.name_pt_BR
		else:
			return self.name_en

	def get_description(self):
		cur_language = translation.get_language()
		if cur_language == 'es':
			return self.description_es
		elif cur_language == 'pt-br':
			return self.description_pt_BR
		else:
			return self.description_en

	# Easily set all the prices of a product to the given price.
	def set_all_prices(self, price):
		price = Decimal(price)
		self.adult_reg_price = price
		self.adult_sale_price = price
		self.children_reg_price = price
		self.children_sale_price = price


class Tour(Product):
	TOUR_DURATION_CHOICES = (
		('HALF', _('Half-Day')),
		('FULL', _('Full-Day'))
	)
	locations = models.ManyToManyField(
		Location,
		blank=True,
		related_name='tours',
		related_query_name='tour',
		verbose_name=_('locations')
	)
	features = models.ManyToManyField(
		Feature,
		blank=True,
		related_name='tours',
		related_query_name='tour',
		verbose_name=_('features')
	)
	duration_type = models.CharField(
		choices=TOUR_DURATION_CHOICES,
		max_length=4,
		verbose_name=_('type of tour')
	)
	duration = models.PositiveSmallIntegerField(
		verbose_name=_('duration (in hours)')
	)

	class Meta:
		ordering = ('-created_at', )
		verbose_name = _('Tour')
		verbose_name_plural = _('Tours')

	# Return the name of the product using the logic implemented in the parent class
	def __str__(self):
		return super().__str__()

	# Return the description of the product using the logic implemented in the parent class
	def get_description(self):
		return super().get_description()

	def get_absolute_url(self):
		cur_language = translation.get_language()
		if cur_language == 'es':
			return reverse('raidchileapp:tour_details', args=[self.id, self.slug_es])
		elif cur_language == 'pt-br':
			return reverse('raidchileapp:tour_details', args=[self.id, self.slug_pt_BR])
		else:
			return reverse('raidchileapp:tour_details', args=[self.id, self.slug_en])

	# For the type of product to be tour when saving a tour.
	def save(self, *args, **kwargs):
		self.product_type = 'TOUR'
		old = Tour.objects.filter(id=getattr(self,'id',None)).first()
		# If object already saved in DB
		if old:
			old = {'adult_reg_price': old.adult_reg_price, 'children_reg_price': old.children_reg_price}
			combos = self.combos.all()
			super().save(*args, **kwargs)  # Call the "real" save() method to save the prices.
			# If adult regular price changed, update all the combos' prices this tour is part of.
			if old['adult_reg_price'] != self.adult_reg_price:
				for combo in combos:
					prices = combo.tours.all().aggregate(
						adult_price=models.Sum('adult_reg_price') ,
					)
					combo.adult_reg_price = prices['adult_price'] or Decimal(0)
					combo.save()
			# If children regular price changed, update all the combos' prices this tour is part of.
			if old['children_reg_price'] != self.children_reg_price:
				for combo in combos:
					prices = combo.tours.all().aggregate(
						children_price=models.Sum('children_reg_price')
					)
					combo.children_reg_price = prices['children_price'] or Decimal(0)
					combo.save()
		super().save(*args, **kwargs)  # Call the "real" save() method.



class Combo(Product):
	tours = models.ManyToManyField(
		Tour,
		related_name='combos',
		related_query_name='combo',
		verbose_name=_('Tours included in the combo')
	)
	image = models.ForeignKey(
		'TourImage',
		blank=True,
		null=True,
		related_name='combos',
		related_query_name='combo',
		on_delete=models.SET_NULL,
		verbose_name=_('image'),
		help_text=_('Appears in the homepage.')
	)
	class Meta:
		ordering = ('-created_at', )
		verbose_name = _('Tour Combo')
		verbose_name_plural = _('Tour Combos')

	# Return the name of the product using the logic implemented in the parent class
	def __str__(self):
		return super().__str__()

	# Return the description of the product using the logic implemented in the parent class
	def get_description(self):
		return super().get_description()

	# For the type of product to be combo when saving a combo.
	def save(self, *args, **kwargs):
		self.product_type = 'COMBO'
		super().save(*args, **kwargs)  # Call the "real" save() method.

# Setting a m2m post-save Signal
# After saving a combo and whenever their tours change, calculate and set the combo's prices.
def signal_combo_m2m_price_calculate(signal, sender, **kwargs):
	combo = kwargs['instance']
	print ("SENDER", sender)
	print ("KWARGS_PK_SET,", kwargs['pk_set'])
	if kwargs['pk_set']:
		prices = combo.tours.all().aggregate(
			adult_price=models.Sum('adult_reg_price') ,
			children_price=models.Sum('children_reg_price')
		)
		combo.adult_reg_price = prices['adult_price'] or Decimal(0)
		combo.adult_sale_price = prices['adult_price'] or Decimal(0)
		combo.children_reg_price = prices['children_price'] or Decimal(0)
		combo.children_sale_price = prices['children_price'] or Decimal(0)
		combo.save()

models.signals.m2m_changed.connect(signal_combo_m2m_price_calculate, Combo.tours.through)

class TourImage(models.Model):
	tours = models.ManyToManyField(
		Tour,
		blank=True,
		related_name='images',
		related_query_name='image'
	)
	alternative_en = models.CharField(
		max_length=150,
		verbose_name=_('alternative text (in English)'),
		help_text=_('Image description in English.')
	)
	alternative_es = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('alternative text (in Spanish)'),
		help_text=_('Image description in Spanish.')
	)
	alternative_pt_BR = models.CharField(
		max_length=150,
		verbose_name=_('alternative text (in Portuguese)'),
		help_text=_('Image description in Portuguese.')
	)
	image = models.ImageField(
		upload_to="tours_images/%Y/%m/%d",
		verbose_name=_('image')
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('created at')
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name=_('updated at')
	)

	class Meta:
		ordering = ('-created_at', )
		verbose_name = _('tour image')
		verbose_name_plural = _('tour images')

	def __str__(self):
		cur_language = translation.get_language()
		if cur_language == 'es':
			return self.alternative_es
		elif cur_language == 'pt-br':
			return self.alternative_pt_BR
		else:
			return self.alternative_en