
from math import exp
from .models import  Wallet
from graphene_django import DjangoObjectType

class WalletType(DjangoObjectType):
    class Meta:
        model = Wallet
        fields = (
            'uid',
            'balance',
            'public_key',
            'wallet_address',
        )




