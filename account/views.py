from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


@login_required
def dashboard(request):
	return render(request, 'account/dashboard.html', {'section': 'Dashboard'})


def register(request):
	user_form = UserRegistrationForm()
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			cd = user_form.cleaned_data
			new_user = user_form.save(commit=False)
			new_user.set_password(cd['password'])
			new_user.save()
			Profile.objects.create(user=new_user)
			return render(request, 'account/register_done.html', {'new_user': new_user})

	return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
	user_form = UserEditForm(instance=request.user)
	profile_form = ProfileEditForm(instance=request.user)
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
	return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
