from decimal import Decimal

from django.conf import settings
from django.db.models import Count

from raidchileapp.models import Tour, Category


class Cart(object):
	# Initialize the variable 'cart' from the session.
	def __init__(self, request):
		self.session = request.session

		cart = self.session.get(settings.CART_SESSION_ID)

		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {'items': {}, 'combo_id': False}

		self.cart = cart
		self.half_days = 0
		self.full_days = 0


	# Method to add a product to the cart
	# In this case the product will be a tour.
	def add(self, product, adult_qty=1, children_qty=0, update_quantity=False):
		# Convert product id into a string because Django uses json to serialize session data and json only allows string names
		product_id = str(product.id)
		if product_id not in self.cart['items']:
			self.cart['items'][product_id] = {
				'adult_qty': 0,
				'children_qty': 0,
				'adult_reg_price': str(product.adult_reg_price),
				'children_reg_price': str(product.children_reg_price),
				'adult_sale_price': str(product.adult_sale_price),
				'children_sale_price': str(product.children_sale_price),
			}
		# Does the newly added item creates a combo?
		self.cart['combo_id'] = None
		self.is_combo()
		if update_quantity:
			self.cart['items'][product_id]['adult_qty'] = adult_qty
			self.cart['items'][product_id]['children_qty'] = children_qty
		else:
			self.cart['items'][product_id]['adult_qty'] += adult_qty
			self.cart['items'][product_id]['children_qty'] += children_qty
		self.save()

	# Saving the cart into the session
	def save(self):
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True

	# Method to remove a product from the cart
	# In this case the product will be a tour.
	def remove(self, product):
		product_id = str(product.id)
		if product_id in self.cart['items']:
			del self.cart['items'][product_id]
			# Do the remaining items create a combo?
			self.cart['combo_id'] = False
			self.is_combo()
			self.save()

	def __getitem__(self, key):
		return self.cart[key]


	# Method to describe how to iterate across all the items in the cart.
	# Calculating its regular and sale price given the actual adult and children quantities.
	def __iter__(self):
		product_ids = self.cart['items'].keys()
		products = Tour.objects.filter(id__in=product_ids)
		self.half_days = 0
		self.full_days = 0
		for product in products:
			self.cart['items'][str(product.id)]['product'] = product
			if product.tour_type == 'HALF':
				self.half_days += 1
			elif product.tour_type == 'FULL':
				self.full_days += 1

		for item in self.cart['items'].values():
			item['adult_reg_price'] = Decimal(item['adult_reg_price'])
			item['children_reg_price'] = Decimal(item['children_reg_price'])
			item['adult_sale_price'] = Decimal(item['adult_sale_price'])
			item['children_sale_price'] = Decimal(item['children_sale_price'])
			item['total_reg_price'] = item['adult_reg_price'] * item['adult_qty'] + item['children_reg_price'] * item['children_qty']
			item['total_sale_price'] = item['adult_sale_price'] * item['adult_qty'] + item['children_sale_price'] * item['children_qty']
			yield item

	# Method to calculate how many tours are in the cart.
	def __len__(self):
		return len(self.cart['items'].values())

	# Method to calculate the total regular price of the cart items.
	def get_total_reg_price(self):
		return sum(Decimal(item['adult_reg_price']) * item['adult_qty'] + Decimal(item['children_reg_price']) * item['children_qty'] for item in self.cart['items'].values())

	# Method to calculate the total sale price of the cart items.
	def get_total_sale_price(self):
		return sum(Decimal(item['adult_sale_price']) * item['adult_qty'] + Decimal(item['children_sale_price']) * item['children_qty'] for item in self.cart['items'].values())

	# Return whether the current cart contents qualify as a sale
	def is_sale(self):
		# if (self.full_days > 2) or (self.full_days == 2 and self.half_days > 0):
		# 	return True
		return False

	# Return whether the current cart contents qualify as combo
	# If it does, sets the id of the matching combo.
	def is_combo(self):
		if not self.cart['combo_id']:
			tour_cart_ids = [ int(k) for k in self.cart['items'].keys() ]
			## Filter the combos with tour number less or equal than the number of tours in the cart
			## First come the combos with more tours.
			combos = Category.objects.annotate(Count('tour')).filter(available=True, combo=True, tour__count__lte=len(tour_cart_ids)).order_by('-tour__count').values_list('id', flat=True)
			## For each combo, turn all it's tours into a set a compare with the tours in the cart
			## made into a set as well.
			for combo in combos:
				combo_tours = Tour.objects.filter(available=True, categories__id=combo).values_list('id', flat=True)
				combo_tours_set = set(combo_tours)
				is_combo = combo_tours_set <= set(tour_cart_ids)
				if is_combo:
					# If we found a combo, we'll set it's id on the cart to later compute the discount.
					self.cart['combo_id'] = combo
					#print ("COMBO_ID SET: ", self.cart['combo_id'])

					return True

			return False

		return True

	# Clear the cart contents
	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.cart['combo_id'] = False
		self.session.modified = True
		self.half_days = 0
		self.full_days = 0