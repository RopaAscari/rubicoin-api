
import json
import math
import os
from backend.execeptions import Exceptions
import jwt
import time
import bcrypt
import random
import graphene
from users.models import User
from .models import Notification
from .types import NotificationType
from firebase_admin import messaging
from notification.inputs import FetchNotificationInput, SendNotificationInput, UpdateReadNotificationsInput


class SendNotification(graphene.Mutation):
    class Arguments:
        input = SendNotificationInput(required=True)

    verified = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        curr_time = time.time()

        user = User.objects.filter().first()

        print(user)

        if user == None:
            pass

        message = messaging.Message(
            data={
                'type': input.type,
                'message': input.message
            },
            token=user.messaging_token,
        )

        response = messaging.send(message)

        return SendNotificationInput(success=response)

class UpdateReadNotifications(graphene.Mutation):
    class Arguments:
        input = UpdateReadNotificationsInput(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):

        response = Notification.objects.filter(user_id=input.user_id).update(is_unread=False)

        if response <= 0:
            raise Exception()

        success = True

        return UpdateReadNotificationsInput(success=success)


class Query(graphene.ObjectType):
    notifications = graphene.List(NotificationType,arguments=FetchNotificationInput(required=True))

    def resolve_notifications(root, info, **kwargs):
        user_id = kwargs['arguments']['user_id']
        return Notification.objects.filter(user_id=user_id)


class Mutation(graphene.ObjectType):
    send_notification = SendNotification.Field()
    update_read_notifications = UpdateReadNotifications.Field()


notificationSchema = graphene.Schema(query=Query, mutation=Mutation)
