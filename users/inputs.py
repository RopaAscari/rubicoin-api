import graphene
from graphene_django import DjangoObjectType


class UserInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    phone_number = graphene.String()


class AuthenticateInput(graphene.InputObjectType):
    email = graphene.String()
    password = graphene.String()


class SendVerificationCodeInput(graphene.InputObjectType):
    email = graphene.String()
    phoneNumber = graphene.String()
    verficationType = graphene.String()


class ResetPasswordInput(graphene.InputObjectType):
    email = graphene.String()
    new_password = graphene.String()
    old_password = graphene.String()


class VerifyCodeInput(graphene.InputObjectType):
    email = graphene.String()
    code = graphene.String()

class FetchCryptoAssetsInput(graphene.InputObjectType):
    start = graphene.Int()
    limit = graphene.Int()
    conversion = graphene.String()
