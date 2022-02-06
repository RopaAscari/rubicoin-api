from tkinter import W
import graphene
from bitcoin import *
from requests import Session
from users.models import User
from crypto.models import Wallet
from crypto.types import WalletType
from users.gql_types import AssetType
from backend.execeptions import Exceptions
from backend.settings import CRYPTO_API, CRYPTO_API_KEY
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from .inputs import FetchCryptoAssetsInput, CreateWalletInput, FetchWalletInput


class CreateWallet(graphene.Mutation):
    class Arguments:
        arguments = CreateWalletInput(required=True)

    wallet = graphene.Field(WalletType)

    @classmethod
    def mutate(cls, root, info, arguments):
        try:
            uid = arguments.uid
            wallet = Wallet()

            response = User.objects.filter(id=uid)

            if not response.exists():
                raise Exception(Exceptions.User.NOT_FOUND)

            wallet.uid = uid
            wallet.balance = 0.0
            wallet.private_key = random_key()
            wallet.public_key = privtopub(wallet.private_key)
            wallet.wallet_address = pubtoaddr(wallet.public_key)

            wallet.save()

            return CreateWallet(wallet=wallet)
        except Exception as e:
            print(e)
            raise e


class Query(graphene.ObjectType):

    get_user_wallet = graphene.Field(
        WalletType, arguments=FetchWalletInput(required=True))

    assets = graphene.List(
        AssetType, arguments=FetchCryptoAssetsInput(required=True))

    def resolve_get_user_wallet(root, info, **kwargs):
        uid = kwargs['arguments']['uid']
        wallet = Wallet.objects.filter(uid=uid)

        if not wallet.exists():
            raise Exception("Wallet doesn't exist")

        return WalletType(balance=wallet[0].balance, public_key=wallet[0].public_key, wallet_address=wallet[0].wallet_address)

    def resolve_assets(root, info, **kwargs):

        def sanitize(data):
            return AssetType(
                id=data['id'],
                name=data['name'],
                symbol=data['symbol'],
                price=data['quote']['USD']['price'],
                market_cap=data['quote']['USD']['market_cap'],
                percent_change_1h=data['quote']['USD']['percent_change_1h']
            )

        parameters = {
            'start': kwargs['arguments']['start'],
            'limit':  kwargs['arguments']['limit'],
            'convert':  kwargs['arguments']['conversion']
        }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': CRYPTO_API_KEY,
        }

        data = []
        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(CRYPTO_API, params=parameters)
            data = json.loads(response.text)
            data = list(map(sanitize, data['data']))

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return data


class Mutation(graphene.ObjectType):
    create_wallet = CreateWallet.Field()
    #fetch_crypto_assets = FetchCryptoAssets.Field()


cryptoSchema = graphene.Schema(query=Query, mutation=Mutation)
