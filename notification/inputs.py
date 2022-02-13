import graphene
from graphene_django import DjangoObjectType


class SendNotificationInput(graphene.InputObjectType):
    type = graphene.String()
    user_id = graphene.String()
    message = graphene.String()
    
class FetchNotificationInput(graphene.InputObjectType):
    user_id = graphene.String()

class UpdateReadNotificationsInput(graphene.InputObjectType):
    user_id = graphene.String()