from django import forms
from django.core.validators import RegexValidator

# Create the forms here

class SearchForm(forms.Form):
	search_terms = forms.CharField(	label='Términos de Busqueda',
									required=False,
									max_length=200,
									widget= forms.TextInput(attrs={	'placeholder': 'Buscar...',
																	'class': 'w3-input  w3-border'})
									)
	reservation_date = forms.DateField(	label = 'Fecha de Reservación',
										required=False,
										widget= forms.DateInput(attrs={'class': 'w3-input  w3-border'})
									)
	adult_qty = forms.IntegerField(	label='Adultos',
										min_value=1,
										max_value=100,
										widget=forms.NumberInput(attrs={'value': '1',
																		'class': 'w3-input  w3-border'})
									)
	kids_qty = forms.IntegerField(	label='Niños',
										min_value=0,
										max_value=100,
										widget=forms.NumberInput(attrs={'value': '0',
																		'class': 'w3-input w3-border'})
									)

class MailListForm(forms.Form):
	# Campo de nombre no requerido tambien.
	email = forms.EmailField(	label='Email',
								max_length=100,
								widget=forms.EmailInput(attrs={'placeholder': 'Su dirección de email',
																'class': 'w3-input w3-border'})
								)

class ContactForm(forms.Form):
	name = forms.CharField(	label='Nombre',
							max_length=100,
							widget=forms.TextInput(attrs={'placeholder': 'Nombre',
														'class': 'w3-input w3-padding-16 w3-border'})
							)
	email = forms.EmailField(	label='Email',
								max_length=100,
								widget=forms.EmailInput(attrs={'placeholder': 'Email',
																'class': 'w3-input w3-padding-16 w3-border'})
								)
	phone_number = forms.CharField(	label='Teléfono',
									max_length=100,
									validators=[RegexValidator('^(\+*\d+)+$', message="El número de teléfono no debe contener espacios")],
									widget=forms.TextInput(attrs={'placeholder': 'Teléfono',
																'class': 'w3-input w3-padding-16 w3-border'})
									)
	people_qty = forms.IntegerField(	label='Cantidad de Personas',
										min_value=1, max_value=100,
										widget=forms.NumberInput(attrs={'placeholder': 'Cantidad de Personas',
																		'class': 'w3-input w3-padding-16 w3-border'})
										)
	message = forms.CharField(	label='Mensaje',
								max_length=500,
								widget=forms.Textarea(attrs={'placeholder': 'Mensaje',
															'rows': 3,
															'cols': 50,
															'class': 'w3-input w3-padding-16 w3-border no-resize'})
								)
