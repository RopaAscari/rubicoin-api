
import json
import math
import os
import jwt
import time
import bcrypt
import random
import graphene
from sendsms import api
from .models import User
from .types import UserType
from django.conf import settings
from utlis.utils import generate_code, generate_id
from django.core.mail import send_mail
from backend.constants import Constants
from django.utils.html import strip_tags
from backend.execeptions import Exceptions
from notification.models import Notification
from django.template.loader import render_to_string
from .inputs import UserInput, AuthenticateInput, SendVerificationCodeInput, ResetPasswordInput, VerifyCodeInput

MODULE_DIRECTORY = os.path.dirname(__file__)


class RegisterUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, input):

        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(
            input.password.encode('utf-8'), salt).decode('utf8')

        user_email = User.objects.filter(email=input.email)

        if user_email.exists():
            raise Exception(Exceptions.User.EMAIL_EXISTS)

        id = generate_id(User)

        user = User.objects.create(
            id=id,
            email=input.email,
            password=password,
            province=input.province,
            last_name=input.last_name,
            first_name=input.first_name,
            ip_address=input.ip_address,
            country_name=input.country_name,
            country_code=input.country_code,
            phone_number=input.phone_number,
            terms_agreed=input.terms_agreed,
            messaging_token=input.messaging_token,
        )

        id = generate_id(Notification)

        notification =  Notification.objects.create(  
            id=id,
            user_id=user.id,   
            message="Welcome to Rubicoin",
            type=Constants.NotificationTypes.WELCOME,          
        )

        token = jwt.encode({
            'id': user.id,
            'email': user.email,
            'walletConnected': False,
            'province': user.province,
            'lastName': user.last_name,
            'miningRigConnected': False,
            'firstName': user.first_name,
            'ipAddress': user.ip_address,
            'phoneNumber': user.phone_number,
            'country_name': user.country_name,
            'country_code': user.country_code,
            'messaging_token': user.messaging_token
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
        db_user = User.objects.filter(email=input.email).first()

        if db_user == None:
            raise Exception(Exceptions.User.INCORRECT_CREDENTIALS)

        if db_user.ip_address != input.ip_address:

            subject = f'Hi ' + db_user.first_name

            TEMPLATE_PATH = os.path.join(
                MODULE_DIRECTORY, 'templates/unsecure_login.html')
            email_body = render_to_string(
                TEMPLATE_PATH, {'ip': input.ip_address})
            plain_message = strip_tags(email_body)

            send_mail(subject, plain_message,  settings.EMAIL_HOST_USER, [
                input.email], html_message=email_body, fail_silently=False,)
            pass

        if bcrypt.checkpw(input.password.encode('utf-8'), db_user.password.encode('utf-8')):

            token = jwt.encode({
                'email': db_user.email,
                'province': db_user.province,
                'lastName': db_user.last_name,
                'ipAddress': db_user.ip_address,
                'firstName': db_user.first_name,
                'phoneNumber': db_user.phone_number,
                'countryName': db_user.country_name,
                'countryCode': db_user.country_code,
                'messaging_token': user.messaging_token,
                'id': json.dumps(db_user.id, default=str),              
                'walletConnected': db_user.wallet_connected,          
                'miningRigConnected': db_user.mining_rig_connected,
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

        code = generate_code()
        body = f'Your verification code is {code}'

        if(input.verficationType == Constants.VerificationTypes.Email):

            user = User.objects.filter(email=input.email).first()

            if user == None:
                raise Exception(Exceptions.User.EMAIL_NOT_EXIST)
            else:

                subject = f'Hi ' + user.first_name

                response = User.objects.filter(
                    email=input.email).update(verify_code=code, verify_date=time.time())

                if response != 1:
                    raise Exception(Exceptions.User.GENERIC)

                TEMPLATE_PATH = os.path.join(
                    MODULE_DIRECTORY, 'templates/verification_code.html')

                email_body = render_to_string(TEMPLATE_PATH, {'code': code})
                plain_message = strip_tags(email_body)

                send_mail(subject, plain_message,  settings.EMAIL_HOST_USER, [
                          input.email], html_message=email_body, fail_silently=False,)
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
