from django.contrib import admin

from .models import ContactMessage
# Register your models here.

class ContactMessagesAdmin(admin.ModelAdmin):
	list_display = ['full_name', 'email', 'created_at', 'updated_at']
	list_filter = ['full_name', 'created_at']

admin.site.register(ContactMessage, ContactMessagesAdmin)