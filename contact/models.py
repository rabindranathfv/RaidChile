from django.db import models
from django.urls import reverse

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

	class Meta:
		ordering = ('-created_at',)
		verbose_name = 'contact message'
		verbose_name_plural = 'contact messages'

	def __str__(self):
		return self.full_name + ' - ' + self.created_at.strftime("%d/%m/%Y %I:%M %p")

	def get_admin_url(self):
		info = (self._meta.app_label, self._meta.model_name)
		admin_url = reverse('admin:%s_%s_change' % info, args=(self.pk,))
		return admin_url