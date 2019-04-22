from decimal import Decimal

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from .models import Location, Tour, Category, Product

# Create the forms here
class SearchForm(forms.Form):
	search_terms = forms.CharField(
		label=_('Search terms'),
		required=False,
		max_length=200,
		widget= forms.TextInput(
			attrs={
				'placeholder': _('Search...'),
				'class': 'w3-input w3-border'
			}
		)
	)
	locations = forms.ModelMultipleChoiceField(
		label=_('Locations'),
		queryset=Location.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=False
	)
	min_price = forms.DecimalField(
		label=_('Minimum Price'),
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
		label=_('Maximum Price'),
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

class CommentForm(forms.Form):
	name = forms.CharField(	label='Name',
							max_length=100,
							widget=forms.TextInput(attrs={'placeholder': 'Name',
														'class': 'w3-input w3-border'})
						)
	email = forms.EmailField(	label='Email',
								max_length=100,
								widget=forms.EmailInput(attrs={'placeholder': 'Email',
																'class': 'w3-input w3-border'})
								)
	comment = forms.CharField(	label='Comment',
							max_length=500,
							widget=forms.Textarea(attrs={'placeholder': 'Comment',
														'rows': 2,
														'cols': 50,
														'class': 'w3-input w3-padding-16 w3-border no-resize'})
							)

########################## ADMIN FORMS ########################
class CategoryAdminForm(forms.ModelForm):
	products = forms.ModelMultipleChoiceField(
		queryset=Product.objects.all(),
		required=False,
		widget=FilteredSelectMultiple(
			verbose_name=_('Products'),
			is_stacked=False
		)
	)

	class Meta:
		model = Category
		fields = ['products']

	def __init__(self, *args, **kwargs):
		super(CategoryAdminForm, self).__init__(*args, **kwargs)

		if self.instance and self.instance.pk:
			self.fields['products'].initial = self.instance.products.all()

	def save(self, commit=True):
		category = super(CategoryAdminForm, self).save(commit=False)

		#if commit:
		category.save()

		#if category.pk:
		category.products.set(self.cleaned_data['products'])
		self.save_m2m()

		return category