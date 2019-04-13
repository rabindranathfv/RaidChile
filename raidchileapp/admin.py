from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Feature, Location, Tour, TourImage
from .forms import CategoryAdminForm

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'combo',
		'available',
		'updated_at',
	]
	list_filter = ['updated_at',]
	list_editable = ['available',]
	fields = [
		(
			'updated_at',
			'created_at'
		),
		'available',
		(
			'name',
			'slug'
		),
		(
			'combo_discount',
			'combo',

		),
		'short_desc',
		'image',
		'image_tag',
		'tours'
	]
	search_fields = ['name']
	readonly_fields = [
		'created_at',
		'updated_at',
		'image_tag',
	]
	prepopulated_fields = {
		'slug': ('name',),
	}
	form = CategoryAdminForm

	def get_queryset(self, request):
		qs = super(CategoryAdmin, self).get_queryset(request)
		self.request = request
		return qs

	# Method to display icon image tag inside django admin
	def image_tag(self, obj):
		img_full_url = self.request.scheme + '://' + str(self.request.get_host()) + obj.image.image.url
		html_img = '<img src="%s" style="max-width: 100%%; max-height: 400px" />'% ( img_full_url )
		return mark_safe(html_img)

admin.site.register(Category, CategoryAdmin)


class FeatureAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'icon',
		'updated_at',
	]
	list_filter = ['updated_at']
	list_editable = ['icon']
	fields = [
		(
			'updated_at',
			'created_at'
		),
		'name',
		(
			'icon',
			'icon_image'
		),
	]
	search_fields = ['name']
	readonly_fields = [
		'created_at',
		'updated_at',
		'icon_image'
	]

	class Media:
		# Add the font-awesome css to the django admin of this model
		css = {
			'all': ('css/font-awesome.min.css',)
		}


admin.site.register(Feature, FeatureAdmin)


class LocationAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'region',
		'updated_at',
	]
	list_filter = ['updated_at',]
	list_editable = ['region',]
	fields = [
		(
			'updated_at',
			'created_at'
		),
		(
			'name',
			'region'
		),
	]
	search_fields = [
		'name',
		'region',
	]
	readonly_fields = [
		'created_at',
		'updated_at',
	]

admin.site.register(Location, LocationAdmin)


class GalleryInline(admin.TabularInline):
	model = TourImage.tours.through
	extra = 0
	verbose_name = 'Tour image'
	verbose_name_plural = 'Tour images'
	fields = [
		'tourimage',
		'image_thumbnail',
	]
	readonly_fields = ['image_thumbnail',]

	def get_queryset(self, request):
		qs = super(GalleryInline, self).get_queryset(request)
		self.request = request
		return qs

	# Method to display icon image tag inside django admin
	def image_thumbnail(self, obj):
		img_full_url = self.request.scheme + '://' + str(self.request.get_host()) + obj.tourimage.image.url
		html_img = '<img src="%s" style="max-height: 200px" />'% ( img_full_url )
		return mark_safe(html_img)




class TourAdmin(admin.ModelAdmin):
	list_display = [
	    'id',
		'name',
		'available',
		'updated_at',
	]
	list_filter = [
		'available',
		'updated_at',
	]
	list_editable = ['name', 'available']
	fields = [
		(
			'updated_at',
			'created_at'
		),
		'available',
		(
			'name',
			'slug'
		),
		'locations',
		'categories',
		'features',
		(
			'tour_type',
			'duration',
			'min_pax_number'
		),
		(
			'adult_reg_price',
			'children_reg_price'
		),
		(
			'adult_sale_price',
			'children_sale_price'
		),
		'description',
	]
	search_fields = [
		'name',
		'categories__name',
	]
	readonly_fields = [
		'created_at',
		'updated_at',
	]
	autocomplete_fields = [
		'locations',
		'categories',
		'features',
	]
	prepopulated_fields = {'slug': ('name',)}
	inlines = [GalleryInline]


admin.site.register(Tour, TourAdmin)


class TourImageAdmin(admin.ModelAdmin):
	list_display = [
		'alternative',
		'updated_at',
	]
	list_filter = [
		'alternative',
		'updated_at',
	]
	fields = [
		(
			'updated_at',
			'created_at'
		),
		(
			'image',
			'alternative',
		),
		'image_tag',
		'tours',
	]
	search_fields = ['alternative', 'tours__name']
	readonly_fields = [
		'created_at',
		'updated_at',
		'image_tag',
	]
	filter_horizontal = ['tours',]

	def get_queryset(self, request):
		qs = super(TourImageAdmin, self).get_queryset(request)
		self.request = request
		return qs

	# Method to display icon image tag inside django admin
	def image_tag(self, obj):
		img_full_url = self.request.scheme + '://' + str(self.request.get_host()) + obj.image.url
		html_img = '<img src="%s" style="max-width: 100%%; max-height: 400px" />'% ( img_full_url )
		return mark_safe(html_img)


admin.site.register(TourImage, TourImageAdmin)