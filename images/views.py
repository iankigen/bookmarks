from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import ImageForm
from .models import Image


@login_required
def image_create(request):
	if request.method == 'POST':
		form = ImageForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new_image = form.save(commit=False)
			new_image.user = request.user
			new_image.save()
			messages.success(request, 'Image added successfully')
			return redirect(new_image.get_absolute_url())
	else:
		form = ImageForm(request.GET)
		return render(request, 'images/image/create.html', {'form': form})


def image_detail(request, id, slug):
	image = get_object_or_404(Image, slug=slug, id=id)
	return render(request, 'images/image/detail.html', {'image': image})


@require_POST
@login_required
def image_like(request):
	image_id = request.POST.get('id', '')
	action = request.POST.get('action', '')
	if image_id and action:
		try:
			image = Image.objects.get(id=image_id)
			if action == 'like':
				image.users_like.add(request.user)
			else:
				image.users_like.remove(request.user)
			return JsonResponse({'status': 'ok'})
		except:
			pass
	return JsonResponse({'status': 'fail'})
