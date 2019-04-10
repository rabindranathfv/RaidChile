from django.contrib import admin
from .models import Category, Feature, Location, Tour, TourImage

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'slug',
		'updated_at',
	]
	list_filter = [
		'name',
		'updated_at',
	]
	prepopulated_fields = {
		'slug': ('name',),
	}

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


class TourAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'available',
		'updated_at',
	]
	list_filter = [
		'available',
		'updated_at',
	]
	list_editable = ['available']
	#fields
	search_fields = [
		'name',
		'categories__name',
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
	inlines = [GalleryInline]
	exclude = ('tours',)

admin.site.register(TourImage, TourImageAdmin)