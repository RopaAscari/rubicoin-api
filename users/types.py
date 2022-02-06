
from math import exp
from .models import  User
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'last_name',
            'first_name', 
            'date_created',
            'phone_number',
            'wallet_connected',
            'mining_rig_connected'
        )




