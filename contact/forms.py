from django import forms
from django.core.validators import RegexValidator

from .models import ContactMessage

class ContactForm2(forms.ModelForm):
	
	phone_number = forms.CharField(
		label='Phone',
		max_length=100,
		validators=[RegexValidator(
			'^(\+*\d+)+$',
			message="Numbers without spaces only."
		)],
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

class ContactForm(forms.Form):
	name = forms.CharField(
		label='Full name',
		max_length=100,
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Full name',
				'class': 'w3-input w3-padding-16 w3-border'
			}
		)
	)
	email = forms.EmailField(
		label='Email',
		max_length=100,
		widget=forms.EmailInput(
			attrs={
				'placeholder': 'Email',
				'class': 'w3-input w3-padding-16 w3-border'
			}
		)
	)
	phone_number = forms.CharField(
		label='Phone',
		max_length=100,
		validators=[RegexValidator(
			'^(\+*\d+)+$',
			message="Numbers without spaces only."
		)],
		widget=forms.TextInput(
			attrs={
				'placeholder': 'Phone: e.g.+0123456789',
				'class': 'w3-input w3-padding-16 w3-border'
			}
		)
	)
	message = forms.CharField(
		label='Message',
		max_length=500,
		widget=forms.Textarea(
			attrs={
				'placeholder': 'Message',
				'rows': 3,
				'cols': 50,
				'class': 'w3-input w3-padding-16 w3-border no-resize'
			}
		)
	)
