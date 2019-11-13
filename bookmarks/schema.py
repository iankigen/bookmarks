import graphene
import images.schema


class Query(images.schema.Query, graphene.ObjectType):
	pass


schema = graphene.Schema(query=Query)
