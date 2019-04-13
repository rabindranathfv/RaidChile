from decimal import Decimal

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from .models import Location, Tour, Category

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

########################## ADMIN FORMS ########################
class CategoryAdminForm(forms.ModelForm):
	tours = forms.ModelMultipleChoiceField(
		queryset=Tour.objects.all(),
		required=False,
		widget=FilteredSelectMultiple(
			verbose_name='Tours',
			is_stacked=False
		)
	)

	class Meta:
		model = Category
		fields = ['tours']

	def __init__(self, *args, **kwargs):
		super(CategoryAdminForm, self).__init__(*args, **kwargs)

		if self.instance and self.instance.pk:
			self.fields['tours'].initial = self.instance.tours.all()

	def save(self, commit=True):
		category = super(CategoryAdminForm, self).save(commit=False)

		#if commit:
		category.save()

		#if category.pk:
		category.tours.set(self.cleaned_data['tours'])
		self.save_m2m()

		return category