from decimal import Decimal

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from .models import Location, Tour, Category, Product, Review

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


class ReviewForm(forms.ModelForm):

	class Meta:
		model = Review
		fields = ['product', 'rating', 'full_name', 'email', 'message']
		widgets = {
			'product': forms.HiddenInput(),
			'rating': forms.HiddenInput(),
			'full_name': forms.TextInput(
				attrs={
					'placeholder': _('Full name'),
					'class': 'w3-input w3-padding-16 w3-border'
				}
			),
			'email': forms.EmailInput(
				attrs={
					'placeholder': _('E-mail'),
					'class': 'w3-input w3-padding-16 w3-border'
				}
			),
			'message': forms.Textarea(
				attrs={
					'placeholder': _('Review (800 characters max.)'),
					'rows': 3,
					'cols': 50,
					'class': 'w3-input w3-padding-16 w3-border no-resize'
				}
			)
		}


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