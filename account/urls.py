from django.urls import path, include
from .views import dashboard, register

urlpatterns = [
	path('register/', register, name='register'),
	path('', include('django.contrib.auth.urls')),
	path('', dashboard, name='dashboard'),
]
