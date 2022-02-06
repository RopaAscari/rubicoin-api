
import jwt
import time
import bcrypt
import random
import graphene
from sendsms import api
from .models import User
from .types import UserType
from django.conf import settings
from django.core.mail import send_mail
from backend.constants import Constants
from backend.execeptions import Exceptions
from .inputs import UserInput, AuthenticateInput, SendVerificationCodeInput, ResetPasswordInput, VerifyCodeInput

class RegisterUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, input):
        user = User()
        user.email = input.email
        user.first_name = input.first_name
        user.last_name = input.last_name

        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(
            input.password.encode('utf-8'), salt).decode('utf8')

        user.phone_number = input.phone_number
        user.save()

        token = jwt.encode({
            'id':user.id,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'walletConnected': False,
            'miningRigConnected': False,
            'phoneNumber': user.phone_number,
        }, "secret", algorithm="HS256")

        return RegisterUser(user=user, token=token)


class AuthenticateUser(graphene.Mutation):
    class Arguments:
        input = AuthenticateInput(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, input):
        user = User()
        response = User.objects.filter(email=input.email)

        if not response.exists():
            raise Exception(Exceptions.User.INCORRECT_CREDENTIALS)

        db_user = response[0]

        if bcrypt.checkpw(input.password.encode('utf-8'), db_user.password.encode('utf-8')):
            token = jwt.encode({
                'email': db_user.email,
                'firstName': db_user.first_name,
                'lastName': db_user.last_name,
                'phoneNumber': db_user.phone_number,
            }, "secret", algorithm="HS256")

            return AuthenticateUser(user=user, token=token)
        else:
            raise Exception(Exceptions.User.INCORRECT_CREDENTIALS)


class SendVerificationCode(graphene.Mutation):
    class Arguments:
        input = SendVerificationCodeInput(required=True)

    success = graphene.Boolean()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, input):

        subject = f'Hi'
        code = random.randint(0, 999999)
        body = f'Your verification code is {code}'

        if(input.verficationType == Constants.VerificationTypes.Email):
            print(input.email)
            user = User.objects.filter(email=input.email)

            if not user.exists():
                raise Exception(Exceptions.User.EMAIL_NOT_EXIST)
            else:

                response = User.objects.filter(
                    email=input.email).update(verify_code=code, verify_date=time.time())

                if response != 1:
                    raise Exception(Exceptions.User.GENERIC)

                send_mail(subject, body, settings.EMAIL_HOST_USER, [input.email],
                          fail_silently=False,
                          )
        else:
            user = User.objects.filter(phone_number=input.phoneNumber)

            if not user.exists():
                raise Exception(Exceptions.User.PHONE_NOT_EXIST)
            else:
                api.send_sms(body=body, from_phone='+41791111111',
                             to=[input.phoneNumber])

        return SendVerificationCode(success=True)


class ResetPassword(graphene.Mutation):
    class Arguments:
        input = ResetPasswordInput(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        response = User.objects.filter(email=input.email)

        if not response.exists():
            raise Exception(Exceptions.User.GENERIC)

        db_user = response[0]

        if not bcrypt.checkpw(input.old_password.encode('utf-8'), db_user.password.encode('utf-8')):
            raise Exception(Exceptions.User.INCORRECT_PASSWORD)

        salt = bcrypt.gensalt()
        new_password = bcrypt.hashpw(
            input.new_password.encode('utf-8'), salt).decode('utf8')

        response = User.objects.filter(
            email=input.email).update(password=new_password)

        if response != 1:
            raise Exception(Exceptions.User.GENERIC)

        return ResetPassword(success=True)


class VerifyCode(graphene.Mutation):
    class Arguments:
        input = VerifyCodeInput(required=True)

    verified = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        curr_time = time.time()

        user = User.objects.filter(email=input.email)

        if not user.exists():
            raise Exception(Exceptions.User.PHONE_NOT_EXIST)

        verified = int(
            round((curr_time - float(user[0].verify_date)) / 60)) < 10

        if not verified:
            raise Exception(Exceptions.User.CODE_EXPIRED)

        if user[0].verify_code != input.code:
            raise Exception(Exceptions.User.CODE_EXPIRED)

        return VerifyCode(verified=verified)

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

class Mutation(graphene.ObjectType):
    verify_code = VerifyCode.Field()
    register_user = RegisterUser.Field()
    reset_password = ResetPassword.Field()
    authenticate_user = AuthenticateUser.Field()
    send_verification_code = SendVerificationCode.Field()

userSchema = graphene.Schema(query=Query, mutation=Mutation)
