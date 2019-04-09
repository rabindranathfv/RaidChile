from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

	# Exclude sale prices when regular prices are applied and viceversa
	def get_exclude(self, request, obj=None):
		if obj is None:
			return ['adult_reg_price', 'adult_sale_price', 'children_reg_price', 'children_sale_price',]
		# elif obj.order.is_sale():
		# 	return ['adult_reg_price', 'children_reg_price',]

		return ['adult_sale_price', 'children_sale_price',]




class OrderAdmin(admin.ModelAdmin):
	list_display = [
		'id',
		'full_name',
		'email',
		'paid',
		'created_at',
		'updated_at'
	]
	list_filter = [
		'paid',
		'created_at',
		'updated_at'
	]
	inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)