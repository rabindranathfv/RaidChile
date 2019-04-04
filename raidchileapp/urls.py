"""raidchileapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""
from django.urls import path

from . import views

app_name = 'raidchileapp'
urlpatterns = [
	path('', views.home, name='home'),
	path('tours/<slug:category_slug>/', views.tour_search_by_category, name='tour_search_by_category'),
	path('tours/<int:id>)/<slug:slug>/', views.tour_details, name='tour_details'),
	# Template testing urls
	path('tours/details', views.tour_details_dummy, name='tour_details'),
	path('tours/search', views.tour_search_dummy, name='tour_search'),
]
