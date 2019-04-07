from django import forms
from django.core.validators import RegexValidator

from .models import ContactMessage

class ContactForm(forms.ModelForm):

	phone_number = forms.CharField(
		label='Phone',
		required=False,
		max_length=100,
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Phone: e.g.+0123456789',
				'class': 'w3-input w3-padding-16 w3-border'
			}
		)
	)

	class Meta:
		model = ContactMessage
		fields = [
			'full_name',
			'email',
			'phone',
			'message'
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
			'message': forms.Textarea(
				attrs={
					'placeholder': 'Message',
					'rows': 3,
					'cols': 50,
					'class': 'w3-input w3-padding-16 w3-border no-resize'
				}
			)
		}