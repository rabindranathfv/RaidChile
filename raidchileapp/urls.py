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
	path('tours/', views.search_all_tours, name='search_all_tours'),
	path('tours/<slug:category_slug>/', views.tour_search_by_category, name='tour_search_by_category'),
	path('tours/<int:id>/<slug:slug>/', views.tour_details, name='tour_details'),
	path('combos/', views.search_all_combos, name='search_all_combos'),
	path('combos/<int:id>/<slug:slug>/', views.combo_details, name='combo_details'),
]
