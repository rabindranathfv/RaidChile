from django import forms
from django.utils.translation import ugettext as _


class CartAddProductForm(forms.Form):
	adults_quantity = forms.IntegerField(
		label=_('Adults'),
		min_value=1
	)
	children_quantity = forms.IntegerField(
		label=_('Children'),
		min_value=0
	)
	update = forms.BooleanField(
		required=False,
		initial=False,
		widget=forms.HiddenInput
	)