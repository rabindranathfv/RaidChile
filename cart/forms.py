from django import forms
from django.utils.translation import gettext_lazy as _


class CartAddProductForm(forms.Form):
	adult_quantity = forms.IntegerField(
		label=_('Adults'),
		min_value=1,
		widget= forms.NumberInput(
			attrs={
				'class': 'w3-input w3-border'
			}
		)
	)
	children_quantity = forms.IntegerField(
		label=_('Children'),
		initial=0,
		min_value=0,
		widget= forms.NumberInput(
			attrs={
				'class': 'w3-input w3-border'
			}
		)
	)
	update = forms.BooleanField(
		required=False,
		initial=False,
		widget=forms.HiddenInput
	)