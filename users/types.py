
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
            'province',           
            'last_name',
            'ip_address',
            'first_name',
            'country_code',
            'country_name',
            'date_created',
            'phone_number',
            'terms_agreed',
            'messaging_token',
            'wallet_connected',
            'mining_rig_connected'           
        )
