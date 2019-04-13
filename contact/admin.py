from django.contrib import admin

from .models import ContactMessage
# Register your models here.

class ContactMessagesAdmin(admin.ModelAdmin):
	list_display = [
		'full_name',
		'email',
		'created_at',
		'updated_at',
	]
	list_filter = [
		'created_at',
	]
	fields = [
		(
			'updated_at',
			'created_at'
		),
		'full_name',
		(
			'email',
			'phone'
		),
		'message',
	]
	search_fields = [
		'full_name',
		'email',
		'phone',
	]
	readonly_fields = [
		'updated_at',
		'created_at',
	]

admin.site.register(ContactMessage, ContactMessagesAdmin)