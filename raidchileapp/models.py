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
	short_desc_en = models.TextField(
		blank=True,
		max_length=200,
		verbose_name=_('short description (in English)'),
		help_text=_('Only necessary if it\'s a combo.')
	)
	short_desc_es = models.TextField(
		blank=True,
		max_length=200,
		verbose_name=_('short description (in Spanish)'),
		help_text=_('Only necessary if it\'s a combo.')
	)
	short_desc_pt_BR = models.TextField(
		blank=True,
		max_length=200,
		verbose_name=_('short description (in Portuguese)'),
		help_text=_('Only necessary if it\'s a combo.')
	)
	available = models.BooleanField(
		default=True,
		verbose_name=_('available')
	)
	combo = models.BooleanField(
		default=False,
		verbose_name=_('Is it tour combo?')
	)
	combo_discount = models.DecimalField(
		default = Decimal(0),
		max_digits=10,
		decimal_places=2,
		verbose_name=_('combo discount')
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
		verbose_name = _('Category / Combo')
		verbose_name_plural = _('Categories / Combos')

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
	name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name')
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
		ordering = ('name', )
		verbose_name = _('feature')
		verbose_name_plural = _('features')

	def __str__(self):
		return self.name

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



class Tour(models.Model):
	TOUR_TYPE_CHOICES = (
		('HALF', _('Half-Day')),
		('FULL', _('Full-Day'))
	)

	name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('name')
	)
	locations = models.ManyToManyField(
		Location,
		blank=True,
		related_name='tours',
		related_query_name='tour',
		verbose_name=_('locations')
	)
	categories = models.ManyToManyField(
		Category,
		blank=True,
		related_name='tours',
		related_query_name='tour',
		verbose_name=_('categories')
	)
	features = models.ManyToManyField(
		Feature,
		blank=True,
		related_name='tours',
		related_query_name='tour',
		verbose_name=_('features')
	)
	available = models.BooleanField(
		default=True,
		verbose_name=_('available')
	)
	tour_type = models.CharField(
		choices=TOUR_TYPE_CHOICES,
		max_length=4,
		verbose_name=_('type of tour')
	)
	slug = models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True
	)
	description = models.TextField(
		verbose_name=_('tour description')
	)
	duration = models.PositiveSmallIntegerField(
		verbose_name=_('duration (in hours)')
	)
	min_pax_number = models.PositiveSmallIntegerField(
		default=1,
		verbose_name=_('minimum passenger number')
	)
	adult_reg_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		verbose_name=_('adults\' regular price')
	)
	children_reg_price = models.DecimalField(
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

	class Meta:
		ordering = ('name', )
		verbose_name = _('tour')
		verbose_name_plural = _('tours')
		indexes = [ models.Index(fields=['id', 'slug']),]

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('raidchileapp:tour_details', args=[self.id, self.slug])



class TourImage(models.Model):
	tours = models.ManyToManyField(
		Tour,
		blank=True,
		related_name='images',
		related_query_name='image'
	)
	alternative = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('alternative text'),
		help_text=_('Image title.')
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
		ordering = ('alternative', )
		verbose_name = _('tour image')
		verbose_name_plural = _('tour images')

	def __str__(self):
		return self.alternative