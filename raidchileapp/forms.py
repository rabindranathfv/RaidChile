from decimal import Decimal

from django import forms
from django.conf import settings
from django.core.validators import RegexValidator

from .models import Location

# Create the forms here
class SearchForm(forms.Form):
	search_terms = forms.CharField(
		label='Search terms',
		required=False,
		max_length=200,
		widget= forms.TextInput(
			attrs={
				'placeholder': 'Search...',
				'class': 'w3-input w3-border'
			}
		)
	)
	locations = forms.ModelMultipleChoiceField(
		label='Locations',
		queryset=Location.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=False
	)
	min_price = forms.DecimalField(
		label='Minimum Price',
		required=False,
		min_value=Decimal(0),
		max_digits=10,
		decimal_places=2,
		widget= forms.NumberInput(
			attrs={
				'class': 'w3-input w3-border w3-round'
			}
		)
	)
	max_price = forms.DecimalField(
		label='Maximum Price',
		required=False,
		min_value=Decimal(0),
		max_digits=10,
		decimal_places=2,
		widget= forms.NumberInput(
			attrs={
				'class': 'w3-input w3-border w3-round'
			}
		)
	)
	"""
	adult_qty = forms.IntegerField(
		label='Adults',
		min_value=1,
		max_value=500,
		widget=forms.NumberInput(
			attrs={
				'value': '1',
				'class': 'w3-input  w3-border'
			}
		)
	)
	kids_qty = forms.IntegerField(
		label='Children',
		min_value=0,
		max_value=500,
		widget=forms.NumberInput(
			attrs={
				'value': '0',
				'class': 'w3-input w3-border'
			}
		)
	)
	"""

"""
class MailListForm(forms.Form):
	name = forms.CharField(	label='Nombre',
							max_length=100,
							widget=forms.TextInput(attrs={'placeholder': 'Su nombre',
														'class': 'w3-input w3-border'})
						)
	email = forms.EmailField(	label='Email',
								max_length=100,
								widget=forms.EmailInput(attrs={'placeholder': 'Su dirección de email',
																'class': 'w3-input w3-border'})
								)
"""

class CommentForm(forms.Form):
	name = forms.CharField(	label='Nombre',
							max_length=100,
							widget=forms.TextInput(attrs={'placeholder': 'Su nombre',
														'class': 'w3-input w3-border'})
						)
	email = forms.EmailField(	label='Email',
								max_length=100,
								widget=forms.EmailInput(attrs={'placeholder': 'Su dirección de email',
																'class': 'w3-input w3-border'})
								)
	comment = forms.CharField(	label='Comentario',
							max_length=500,
							widget=forms.Textarea(attrs={'placeholder': 'Comentario',
														'rows': 2,
														'cols': 50,
														'class': 'w3-input w3-padding-16 w3-border no-resize'})
							)

class ContactForm(forms.Form):
	name = forms.CharField(	label='Full name',
							max_length=100,
							widget=forms.TextInput(attrs={'placeholder': 'Full name',
														'class': 'w3-input w3-padding-16 w3-border'})
							)
	email = forms.EmailField(	label='Email',
								max_length=100,
								widget=forms.EmailInput(attrs={'placeholder': 'Email',
																'class': 'w3-input w3-padding-16 w3-border'})
								)
	phone_number = forms.CharField(	label='Phone',
									max_length=100,
									validators=[RegexValidator('^(\+*\d+)+$', message="Numbers without spaces only.")],
									widget=forms.TextInput(attrs={'placeholder': 'Phone: e.g.+0123456789',
																'class': 'w3-input w3-padding-16 w3-border'})
									)
	"""
	people_qty = forms.IntegerField(	label='Cantidad de Personas',
										min_value=1, max_value=100,
										widget=forms.NumberInput(attrs={'placeholder': 'Cantidad de Personas',
																		'class': 'w3-input w3-padding-16 w3-border'})
										)
	"""
	message = forms.CharField(	label='Message',
								max_length=500,
								widget=forms.Textarea(attrs={'placeholder': 'Message',
															'rows': 3,
															'cols': 50,
															'class': 'w3-input w3-padding-16 w3-border no-resize'})
								)
