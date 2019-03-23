from django.urls import path
from .views import image_create, image_detail, image_like

app_name = 'images'

urlpatterns = [
	path('create/', image_create, name='create'),
	path('detail/<id>/<slug>/', image_detail, name='detail'),
	path('like/', image_like, name='like'),
]