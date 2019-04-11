from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.cart_detail, name='cart_detail'),
	path('add/<int:product_id>/', views.cart_add, name='cart_add'),
	path('add/combo/<slug:combo_slug>/', views.cart_add_combo, name='cart_add_combo'),
	path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]