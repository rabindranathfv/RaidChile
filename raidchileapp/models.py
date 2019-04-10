from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

# Create your models here.
# Vertical distribution is for better 'git diff' readability
class Category(models.Model):
	name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name='name'
	)
	slug = models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True
	)
	image = models.ForeignKey(
		'TourImage',
		blank=True,
		null=True,
		related_name='categories',
		related_query_name='category',
		on_delete=models.SET_NULL
	)
	short_desc = models.TextField(
		blank=True,
		max_length=200,
		verbose_name='short description'
	)
	available = models.BooleanField(
		default=True,
		verbose_name='available'
	)
	combo = models.BooleanField(
		default=False,
		verbose_name='Is it tour combo?'
	)
	combo_discount = models.DecimalField(
		default = Decimal(0),
		max_digits=10,
		decimal_places=2,
		verbose_name='combo discount'
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='created at'
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name='updated at'
	)

	class Meta:
		ordering = ('name', )
		verbose_name = 'Category / Combo'
		verbose_name_plural = 'Categories / Combos'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('raidchileapp:tour_search_by_category', args=[self.slug])



class Feature(models.Model):
	name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name='name'
	)
	icon = models.CharField(max_length=150,
		default="fa-eye",
		help_text='String from Font Awesome icons e.g. "fa-eye"',
		verbose_name='icon'
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='created at'
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name='updated at'
	)

	class Meta:
		ordering = ('name', )
		verbose_name = 'feature'
		verbose_name_plural = 'features'

	def __str__(self):
		return self.name

	# Method to display icon image tag inside django admin
	def icon_image(self):
		icon_class= 'fa-eye'
		if self.icon.strip().startswith('fa'):
			icon_class = self.icon.strip()
		return mark_safe('<i class="fa %s fa-3x"></i>' % (icon_class))

	icon_image.short_description = 'Icon image'



class Location(models.Model):
	name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name='name'
	)
	region = models.CharField(
		max_length=150,
		db_index=True,
		blank=True,
		verbose_name='region',
		help_text='Helps users to search by coincidence.'
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='created at'
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name='updated at'
	)

	class Meta:
		ordering = ('name', )
		verbose_name = 'location'
		verbose_name_plural = 'locations'

	def __str__(self):
		return self.name



class Tour(models.Model):
	TOUR_TYPE_CHOICES = (
		('HALF', 'Half-Day'),
		('FULL', 'Full-Day')
	)

	name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name='name'
	)
	locations = models.ManyToManyField(
		Location,
		blank=True,
		related_name='tours',
		related_query_name='tour'
	)
	categories = models.ManyToManyField(
		Category,
		blank=True,
		related_name='tours',
		related_query_name='tour',
	)
	features = models.ManyToManyField(
		Feature,
		blank=True,
		related_name='tours',
		related_query_name='tour'
	)
	available = models.BooleanField(
		default=True,
		verbose_name='available'
	)
	tour_type = models.CharField(
		choices=TOUR_TYPE_CHOICES,
		max_length=4,
		verbose_name='type of tour'
	)
	slug = models.SlugField(
		max_length=150,
		unique=True ,
		db_index=True
	)
	description = models.TextField(
		verbose_name='tour description'
	)
	duration = models.PositiveSmallIntegerField(
		verbose_name='duration (in hours)'
	)
	min_pax_number = models.PositiveSmallIntegerField(
		default=1,
		verbose_name='minimum passenger number'
	)
	adult_reg_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		verbose_name='adults\' regular price'
	)
	children_reg_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		verbose_name='children\'s regular price'
	)
	adult_sale_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		verbose_name='adults\' sale price'
	)
	children_sale_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		verbose_name='children\'s sale price'
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='created at'
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name='updated at'
	)

	class Meta:
		ordering = ('name', )
		verbose_name = 'tour'
		verbose_name_plural = 'tours'
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
		verbose_name='alternative text',
		help_text='Image title.'
	)
	image = models.ImageField(
		upload_to="tours_images/%Y/%m/%d",
		verbose_name='image'
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='created at'
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name='updated at'
	)

	class Meta:
		ordering = ('alternative', )
		verbose_name = 'tour image'
		verbose_name_plural = 'tour images'

	def __str__(self):
		return self.alternative