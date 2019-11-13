import graphene
from graphene_django import DjangoObjectType

from .models import Image


class ImageType(DjangoObjectType):
	class Meta:
		model = Image


class Query(graphene.ObjectType):
	images = graphene.List(ImageType)

	def resolve_images(self, info, **kwargs):
		return Image.objects.all()
