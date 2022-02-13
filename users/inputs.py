import graphene
from graphene_django import DjangoObjectType


class Country(graphene.InputObjectType):
    code = graphene.String()
    name = graphene.String()


class UserInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    password = graphene.String()
    province = graphene.String()
    ip_address = graphene.String()
    messaging_token = graphene.String()
    country_code = graphene.String()
    country_name = graphene.String()
    phone_number = graphene.String()
    terms_agreed = graphene.Boolean()

class AuthenticateInput(graphene.InputObjectType):
    email = graphene.String()
    password = graphene.String()
    ip_address = graphene.String()

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
