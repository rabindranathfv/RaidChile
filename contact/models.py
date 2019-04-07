from django.db import models

# Create your models here.
class ContactMessage(models.Model):
	full_name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name='full name'
	)
	email = models.EmailField(
		max_length=100,
		verbose_name='email'
	)
	phone = models.CharField(
		max_length=30,
		blank=True,
		verbose_name='phone'
	)
	message = models.TextField(
		max_length=500,
		verbose_name='message'
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='created at'
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name='updated at'
	)