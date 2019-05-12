from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from raidchileapp.models import Product


class Order(models.Model):
	full_name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('full name')
	)
	email = models.EmailField(
		max_length=100,
		verbose_name=_('email')
	)
	phone = models.CharField(
		max_length=30,
		blank=True,
		verbose_name=_('phone')
	)
	message = models.TextField(
		max_length=500,
		blank=True,
		verbose_name=_('message')
	)
	trip_date = models.DateField(
		verbose_name=_('estimated first tour\'s date'),
	)
	paid = models.BooleanField(
		default=False,
		verbose_name=_('paid?')
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
		verbose_name=_('order')
		verbose_name_plural=_('orders')

	def __str__(self):
		wording = _('Reservation Order #')
		result =  format_lazy('{words}{number}', words=wording, number=self.id)
		#return 'Reservation Order #{}'.format(self.id)
		return str(result)

	def get_admin_url(self):
		info = (self._meta.app_label, self._meta.model_name)
		admin_url = reverse('admin:%s_%s_change' % info, args=(self.pk,))
		return admin_url

	def is_sale(self):
		return False

	def has_combo(self):
		return self.items.filter(product__product_type="COMBO").exists()

	# Return formated data for django admin.
	def total(self):
		result = intcomma(self.get_total_cost())
		return mark_safe('<span style="font-size: 20px">CLP {}</span>'.format(result))

	def get_total_cost(self, sale=False):
		result = 0
		for item in self.items.all():
			if item.product.product_type == 'COMBO':
				result += item.get_sale_cost()
			else:
				result += item.get_reg_cost()
		return result



class OrderItem(models.Model):
	order = models.ForeignKey(
		Order,
		related_name='items',
		related_query_name='item',
		on_delete=models.PROTECT,
		verbose_name=_('reservation order')
	)
	product = models.ForeignKey(
		Product,
		related_name='reservations',
		related_query_name='reservation',
		on_delete=models.PROTECT,
		verbose_name=_('product')
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
		max_digits=10,
		decimal_places=2,
		verbose_name=_('adults\' sale price')
	)
	children_sale_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		verbose_name=_('children\'s sale price')
	)
	adult_quantity = models.PositiveIntegerField(
		default=1,
		verbose_name=_('adults')
	)
	children_quantity = models.PositiveIntegerField(
		default=1,
		verbose_name=_('children')
	)

	def __str__(self):
		part1= _('Order #')
		part2 = _(' - Item:')
		return str(format_lazy('{p1}{id}{p2}{name}', p1=part1, id=self.order.id, p2=part2, name=self.product))
		#return 'Order #{} - Item:{}'.format(self.order.id, self.product.name)

	# Return formated data for django admin.
	def total_price(self):
		#print ('Calculating total price of: ', self) ## WITHOUT THIS LINE THE OBJECT ISN'T QUERIED AND AN ERROR OCCURS
		result = 0
		if self.product.product_type == 'COMBO':
			result = intcomma(self.get_sale_cost())
		else:
			result = intcomma(self.get_reg_cost())
		return mark_safe('<span style="font-size: 14px">CLP {}</span>'.format(result))

	def get_reg_cost(self):
		return self.adult_reg_price * self.adult_quantity + self.children_reg_price * self.children_quantity

	def get_sale_cost(self):
		return self.adult_sale_price * self.adult_quantity + self.children_sale_price * self.children_quantity