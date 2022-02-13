
from math import exp
from .models import  Notification
from graphene_django import DjangoObjectType

class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = (
            'id',           
            'type',
            'avatar',
            'message',
            'user_id',
            'is_unread',                     
            'date_created',              
        )
