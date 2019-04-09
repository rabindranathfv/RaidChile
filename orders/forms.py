from django import forms
from django.conf import settings

from .models import Order


class OrderCreateForm(forms.ModelForm):
	trip_date = forms.DateField(
		input_formats = settings.DATE_FORMATS,
		widget = forms.DateInput(
			attrs={
				'placeholder': 'Planned Date: e.g. DD/MM/YYYY',
				'class': 'w3-input w3-padding-16 w3-border datepicker reservation'
			}
		)
	)


	class Meta:
		model = Order
		fields = [
			'full_name',
			'phone',
			'email',
			'trip_date',
			'message',
		]
		widgets = {
			'full_name': forms.TextInput(
				attrs={
					'placeholder': 'Full name',
					'class': 'w3-input w3-padding-16 w3-border'
				}
			),
			'email': forms.EmailInput(
				attrs={
					'placeholder': 'Email',
					'class': 'w3-input w3-padding-16 w3-border'
				}
			),
			'phone': forms.TextInput(
				attrs={
					'placeholder': 'Phone: e.g.+0123456789',
					'class': 'w3-input w3-padding-16 w3-border'
				}
			),
			'message': forms.Textarea(
				attrs={
					'placeholder': 'Message',
					'rows': 3,
					'cols': 50,
					'class': 'w3-input w3-padding-16 w3-border no-resize'
				}
			),
		}