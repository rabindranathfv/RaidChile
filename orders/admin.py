from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	verbose_name = _('Tour reservation')
	verbose_name_plural = _('Tour reservations')
	#raw_id_fields = ['product']

	fields = [
		'product',
		'adult_reg_price',
		'children_reg_price',
		'adult_quantity',
		'children_quantity',
		'total_price',
	]
	autocomplete_fields = ['product']
	readonly_fields = ['total_price']



class OrderAdmin(admin.ModelAdmin):
	list_display = [
		'id',
		'full_name',
		'email',
		'paid',
		'total',
		'created_at',
	]
	list_filter = [
		'paid',
		'created_at',
	]
	fields = [
		(
			'updated_at',
			'created_at'
		),
		(
			'full_name',
			'email'
		),
		(
			'phone',
			'trip_date'
		),
		'message',
		(
			'total',
			'paid'
		),
	]
	search_fields = [
		'full_name',
		'email',
		'id',
	]
	readonly_fields = [
		'created_at',
		'updated_at',
		'total',
	]

	inlines = [OrderItemInline]



admin.site.register(Order, OrderAdmin)