import graphene
from graphene_django import DjangoObjectType


class FetchCryptoAssetsInput(graphene.InputObjectType):
    start = graphene.Int()
    limit = graphene.Int()
    conversion = graphene.String()

class CreateWalletInput(graphene.InputObjectType):
    uid = graphene.String()

class FetchWalletInput(graphene.InputObjectType):
    uid = graphene.String()