from decimal import Decimal

from django.conf import settings

from raidchileapp.models import Tour


class Cart(object):
	# Initialize the variable 'cart' from the session.
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	# Method to add a product to the cart
	# In this case the product will be a tour.
	def add(self, product, adult_qty=1, children_qty=0, update_quantity=False):
		# Convert product id into a string because Django uses json to serialize session data and json only allows string names
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {
				'adult_qty': 0,
				'children_qty': 0,
				'adult_reg_price': str(product.adult_reg_price),
				'children_reg_price': str(product.children_reg_price),
				'adult_sale_price': str(product.adult_sale_price),
				'children_sale_price': str(product.children_sale_price),
			}
		if update_quantity:
			self.cart[product_id]['adult_qty'] = adult_qty
			self.cart[product_id]['children_qty'] = children_qty
		else:
			self.cart[product_id]['adult_qty'] += adult_qty
			self.cart[product_id]['children_qty'] += children_qty
		self.save()

	# Saving the cart into the session
	def save(self):
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True

	# Method to remove a product from the cart
	# In this case the product will be a tour.
	def remove(self, product):
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	# Method to describe how to iterate across all the items in the cart.
	# Calculating its regular and sale price given the actual adult and children quantities.
	def __iter__(self):
		product_ids = self.cart.keys()
		products = Tour.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['adult_reg_price'] = Decimal(item['adult_reg_price'])
			item['children_reg_price'] = Decimal(item['children_reg_price'])
			item['adult_sale_price'] = Decimal(item['adult_sale_price'])
			item['children_sale_price'] = Decimal(item['children_sale_price'])
			item['total_reg_price'] = item['adult_reg_price'] * item['adult_qty'] + item['children_reg_price'] * item['children_qty']
			item['total_sale_price'] = item['adult_sale_price'] * item['adult_qty'] + item['children_sale_price'] * item['children_qty']
			yield item

	# Method to calculate how many tours are in the cart.
	def __len__(self):
		return len(self.cart.values())

	# Method to calculate the total regular price of the cart items.
	def get_total_reg_price(self):
		return sum(Decimal(item['adult_reg_price']) * item['adult_qty'] + Decimal(item['children_reg_price']) * item['children_qty'] for item in self.cart.values())

	# Method to calculate the total sale price of the cart items.
	def get_total_sale_price(self):
		return sum(Decimal(item['adult_sale_price']) * item['adult_qty'] + Decimal(item['children_sale_price']) * item['children_qty'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True
