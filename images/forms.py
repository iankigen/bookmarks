from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'url', 'description')
		widgets = {
			'url': forms.HiddenInput,
		}

	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ('jpeg', 'jpg')
		extension = url.split('.')[-1].lower()
		if extension not in valid_extensions:
			raise forms.ValidationError('The given URL does not match valid image extensions.')
		return url

	def save(self, *args, commit=True, **kwargs):
		image_obj = super(ImageForm, self).save(commit=False)
		image_url = self.cleaned_data['url']
		image_name = "{}.{}".format(slugify(image_obj.title), image_url.split('.')[-1].lower())

		# download image
		response = request.urlopen(image_url)
		image_obj.image.save(image_name, ContentFile(response.read()), save=False)
		if commit:
			image_obj.save()
		return image_obj

