
from math import exp
from .models import Card
from graphene_django import DjangoObjectType


class PaymentType(DjangoObjectType):
    class Meta:
        model = Card
        fields = (
            'uid',
            'cvc',
            'city',
            'address',
            'country',
            'province',
            'issuer',
            'card_number',
            'expiry_date',
            'postal_code',
            'date_created',         
            'card_holder_name',
        )
