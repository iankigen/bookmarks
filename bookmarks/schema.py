import graphene
from images.schema import Mutation, Query as ImageQuery


class Query(ImageQuery, graphene.ObjectType):
	pass


schema = graphene.Schema(query=Query, mutation=Mutation)
