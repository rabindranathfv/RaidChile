"""raidchile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

admin.site.index_title = _('Main Menu')
admin.site.site_header = _('Chile Raids - Administration')
admin.site.site_title = _('Chile Raids - Administration')


urlpatterns = i18n_patterns(
    path('', include('raidchileapp.urls')),
    path('contact/', include('contact.urls')),
    path('cart/', include('cart.urls')),
    path('reservations/', include('orders.urls')),
    path('admin/', admin.site.urls),
    # If no prefix is given, use the default language
    prefix_default_language=False
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Development server way of serving media files
