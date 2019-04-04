from django.contrib import admin
from .models import Category, Feature, Location, Tour, TourImage

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'updated_at']
	list_filter = ['name', 'updated_at']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class FeatureAdmin(admin.ModelAdmin):
	list_display = ['name', 'icon', 'updated_at']
	list_filter = ['name', 'updated_at']
	list_editable = ['icon']

admin.site.register(Feature, FeatureAdmin)


class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'region', 'updated_at']
	list_filter = ['name', 'updated_at']
	list_editable = ['region']

admin.site.register(Location, LocationAdmin)


class GalleryInline(admin.TabularInline):
	model = TourImage.tours.through


class TourAdmin(admin.ModelAdmin):
	list_display = ['name', 'available', 'updated_at']
	list_filter = ['available', 'updated_at']
	list_editable = ['available']
	prepopulated_fields = {'slug': ('name',)}
	inlines = [GalleryInline]

admin.site.register(Tour, TourAdmin)


class TourImageAdmin(admin.ModelAdmin):
	list_display = ['alternative', 'updated_at']
	list_filter = ['alternative', 'updated_at']
	inlines = [GalleryInline]
	exclude = ('tours',)

admin.site.register(TourImage, TourImageAdmin)