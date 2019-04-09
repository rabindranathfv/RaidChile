from django.conf import settings
from django.db import models

from raidchileapp.models import Tour


class Order(models.Model):
	full_name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name='full name'
	)
	email = models.EmailField(
		max_length=100,
		verbose_name='email'
	)
	phone = models.CharField(
		max_length=30,
		blank=True,
		verbose_name='phone'
	)
	message = models.TextField(
		max_length=500,
		verbose_name='message'
	)
	trip_date = models.DateField(
		verbose_name='estimated first tour\'s date',
	)
	paid = models.BooleanField(
		default=False,
		verbose_name='is this order paid for?'
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
		ordering = ('-created_at', )

	def __str__(self):
		return 'Reservation Order {}'.format(self.id)

	def is_sale(self):
		return True
		# half_days = self.items.filter( product__tour_type='HALF').count()
		# full_days = self.items.filter( product__tour_type='FULL').count()
		# if (full_days > 2) or (full_days == 2 and half_days > 0):
		# 	return True
		# return False

	def get_total_cost(self):
		if self.is_sale:
			# return sale price
			return sum(item.get_sale_cost() for item in self.items.all())
		# return regular price
		return sum(item.get_reg_cost() for item in self.items.all())


class OrderItem(models.Model):
	order = models.ForeignKey(
		Order,
		related_name='items',
		related_query_name='item',
		on_delete=models.PROTECT,
		verbose_name='reservation order'
	)
	product = models.ForeignKey(
		Tour,
		related_name='reservations',
		related_query_name='reservation',
		on_delete=models.PROTECT,
		verbose_name='tour'
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
	adult_quantity = models.PositiveIntegerField(
		default=1
	)
	children_quantity = models.PositiveIntegerField(
		default=1
	)

	def __str__(self):
		return 'Order Nº{} - Item:{}'.format(self.order.id, self.product.name)

	def get_reg_cost(self):
		return self.adult_reg_price * self.adult_quantity + self.children_reg_price * self.children_quantity

	def get_sale_cost(self):
		return self.adult_sale_price * self.adult_quantity + self.children_sale_price * self.children_quantity