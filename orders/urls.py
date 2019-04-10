from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
	path('confirm/', views.order_create, name='order_create'),
	path('confirm/success/', views.order_create_success, name='order_create_success')
]