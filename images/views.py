from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bookmarks.common.decorators import ajax_required

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


@login_required
def image_detail(request, id, slug):
	image = get_object_or_404(Image, slug=slug, id=id)
	return render(request, 'images/image/detail.html', {'image': image})


@ajax_required
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


@login_required
def image_list(request):
	images = Image.objects.all()
	paginator = Paginator(images, 10)
	page = request.GET.get('page')

	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
		images = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
	return render(request, 'images/image/list.html', {'section': 'images', 'images': images})

