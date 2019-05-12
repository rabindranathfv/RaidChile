from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ContactMessage(models.Model):
	full_name = models.CharField(
		max_length=150,
		db_index=True,
		verbose_name=_('full name')
	)
	email = models.EmailField(
		max_length=100,
		verbose_name=_('email')
	)
	phone = models.CharField(
		max_length=30,
		blank=True,
		verbose_name=_('phone')
	)
	message = models.TextField(
		max_length=500,
		verbose_name=_('message')
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('created at')
	)
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name=_('updated at')
	)

	class Meta:
		ordering = ('-created_at',)
		verbose_name = _('contact message')
		verbose_name_plural = _('contact messages')

	def __str__(self):
		return self.full_name + ' - ' + self.created_at.strftime("%d/%m/%Y %I:%M %p")

	def get_admin_url(self):
		info = (self._meta.app_label, self._meta.model_name)
		admin_url = reverse('admin:%s_%s_change' % info, args=(self.pk,))
		return admin_url