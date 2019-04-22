from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Category, Feature, Location, Tour, Combo, TourImage
from .forms import CategoryAdminForm

# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
	list_display = [
		'name_es',
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
		(
			'available',
		),
		(
			'name_es',
			'slug_es'
		),
		(
			'name_en',
			'slug_en'
		),
		(
			'name_pt_BR',
			'slug_pt_BR'
		),
		'image',
		'image_tag',
		'products'
	]
	search_fields = ['name_es']
	readonly_fields = [
		'created_at',
		'updated_at',
		'image_tag',
	]
	prepopulated_fields = {
		'slug_es': ('name_es',),
		'slug_en': ('name_en',),
		'slug_pt_BR': ('name_pt_BR',),
	}
	form = CategoryAdminForm

	def get_queryset(self, request):
		qs = super(CategoryAdmin, self).get_queryset(request)
		self.request = request
		return qs

	# Method to display image tag inside django admin
	def image_tag(self, obj):
		img_full_url = self.request.scheme + '://' + str(self.request.get_host()) + obj.image.image.url
		html_img = '<img src="%s" style="max-width: 100%%; max-height: 400px" />'% ( img_full_url )
		return mark_safe(html_img)

admin.site.register(Category, CategoryAdmin)



class FeatureAdmin(admin.ModelAdmin):
	list_display = [
		'name_es',
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
		'name_es',
		'name_en',
		'name_pt_BR',
		(
			'icon',
			'icon_image'
		),
	]
	search_fields = ['name_es']
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
	verbose_name = _('Tour Image')
	verbose_name_plural = _('Tour Images')
	fields = [
		'tourimage',
		'image_thumbnail',
	]
	autocomplete_fields = ['tourimage',]
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
		'name_es',
		'id',
		'available',
		'updated_at',
	]
	list_filter = [
		'available',
		'updated_at',
	]
	list_editable = ['available']
	fields = [
		(
			'updated_at',
			'created_at'
		),
		'available',
		(
			'name_es',
			'slug_es'
		),
		(
			'name_en',
			'slug_en'
		),
		(
			'name_pt_BR',
			'slug_pt_BR'
		),
		'locations',
		'categories',
		'features',
		(
			'duration_type',
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
		'description_es',
		'description_en',
		'description_pt_BR',
	]
	search_fields = [
		'name_es',
		'categories__name_es',
	]
	readonly_fields = [
		'product_type',
		'created_at',
		'updated_at',
	]
	autocomplete_fields = [
		'locations',
		'categories',
		'features',
	]
	prepopulated_fields = {
		'slug_es': ('name_es',),
		'slug_en': ('name_en',),
		'slug_pt_BR': ('name_pt_BR',),
	}
	inlines = [GalleryInline]

admin.site.register(Tour, TourAdmin)



class ComboAdmin(admin.ModelAdmin):
	list_display = [
		'name_es',
		'id',
		'available',
		'updated_at',
	]
	list_filter = [
		'available',
		'updated_at',
	]
	list_editable = ['available']
	fields = [
		(
			'updated_at',
			'created_at'
		),
		'available',
		(
			'name_es',
			'slug_es'
		),
		(
			'name_en',
			'slug_en'
		),
		(
			'name_pt_BR',
			'slug_pt_BR'
		),
		'categories',
		(
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
		'tours',
		'description_es',
		'description_en',
		'description_pt_BR',
		'image',
		'image_tag',
	]
	search_fields = [
		'name_es',
		'categories__name_es',
	]
	readonly_fields = [
		'created_at',
		'updated_at',
		'image_tag',
	]
	autocomplete_fields = [
		'categories',
		'image',
	]
	filter_horizontal = ['tours',]
	prepopulated_fields = {
		'slug_es': ('name_es',),
		'slug_en': ('name_en',),
		'slug_pt_BR': ('name_pt_BR',),
	}

	# Method to display image tag inside django admin
	def image_tag(self, obj):
		img_full_url = self.request.scheme + '://' + str(self.request.get_host()) + obj.image.image.url
		html_img = '<img src="%s" style="max-width: 100%%; max-height: 400px" />'% ( img_full_url )
		return mark_safe(html_img)

admin.site.register(Combo, ComboAdmin)



class TourImageAdmin(admin.ModelAdmin):
	list_display = [
		'alternative_es',
		'image_thumbnail',
		'updated_at',
	]
	list_filter = [
		'updated_at',
	]
	fields = [
		(
			'updated_at',
			'created_at'
		),
		'image_tag',
		'image',
		'alternative_es',
		'alternative_en',
		'alternative_pt_BR',
		'tours',
	]
	search_fields = ['alternative_es', 'tours__name_es']
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

		# Method to display icon image tag inside django admin
	def image_thumbnail(self, obj):
		img_full_url = self.request.scheme + '://' + str(self.request.get_host()) + obj.image.url
		html_img = '<img src="%s" style="max-height: 200px" />'% ( img_full_url )
		return mark_safe(html_img)

admin.site.register(TourImage, TourImageAdmin)