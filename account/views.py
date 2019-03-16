from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserRegistrationForm


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
			return render(request, 'account/register_done.html', {'new_user': new_user})

	return render(request, 'account/register.html', {'user_form': user_form})
