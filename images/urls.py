from django.urls import path
from .views import image_create, image_detail

app_name = 'images'

urlpatterns = [
	path('create/', image_create, name='create'),
	path('detail/<id>/<slug>/', image_detail, name='detail')
]