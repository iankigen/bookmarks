import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from .models import Image


class UserType(DjangoObjectType):
	class Meta:
		model = User


class ImageType(DjangoObjectType):
	class Meta:
		model = Image
		interfaces = (graphene.relay.Node,)


class CreateImageMutation(graphene.Mutation):
	image = graphene.Field(ImageType)

	class Arguments:
		title = graphene.String()

	def mutate(self, info, title):
		user = info.context.user
		return CreateImageMutation(image=Image.objects.create(user=user, title=title))


class Mutation(graphene.ObjectType):
	create_image = CreateImageMutation.Field()


class Query(graphene.ObjectType):
	images = graphene.List(ImageType)
	users = graphene.List(UserType)

	def resolve_images(self, info, **kwargs):
		user = info.context.user
		if user.is_authenticated:
			return Image.objects.all()
		return Image.objects.none()

	def resolve_users(self, info, **kwargs):
		return User.objects.all()
