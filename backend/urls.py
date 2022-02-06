
import graphene
from django.urls import path
from django.contrib import admin
from users.schema import userSchema
from crypto.schema import cryptoSchema
from payment.schema import paymentSchema
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


class Query(userSchema.Query, cryptoSchema.Query, paymentSchema.Query, graphene.ObjectType):
    pass


class Mutation(userSchema.Mutation, cryptoSchema.Mutation, paymentSchema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
