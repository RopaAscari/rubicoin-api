import stripe
import graphene
from backend import settings
from payment.models import Card
from payment.types import PaymentType
from backend.execeptions import Exceptions
from utlis.utils import generate_id
from .inputs import CreatePaymentInput, GetUserPaymentMethods

stripe.api_key = settings.STRIPE_DEV_SK


class CreatePaymentMethod(graphene.Mutation):
    class Arguments:
        arguments = CreatePaymentInput(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, arguments):
        def generate_card_token(cardnumber, expmonth, expyear, cvv):

            data = stripe.Token.create(
                card={
                    "number": cardnumber,
                    "exp_month": expmonth,
                    "exp_year": expyear,
                    "cvc": cvv,
                },
            )

            card_token = data['id']

            return card_token

        def create_payment_charge(tokenid, amount):

            payment = stripe.Charge.create(
                # convert amount to cents
                amount=int(amount)*100,
                currency='usd',
                description='Example charge',
                source=tokenid,
            )

            payment_check = payment['paid']

            return payment_check

        try:
            success = False

            card = Card()

            card.id = generate_id(Card)

            card.uid = arguments.uid
            card.cvc = arguments.cvc
            card.card_number = arguments.card_number
            card.expiry_date = arguments.expiry_date
            card.card_holder_name = arguments.card_holder_name

            card.city = arguments.city
            card.address = arguments.address
            card.country = arguments.country
            card.province = arguments.province
            card.postal_code = arguments.postal_code

            card.issuer = arguments.issuer

            card_exp_year = card.expiry_date[2:4]
            card_exp_month = card.expiry_date[0:2]

            # Use Stripe's library to make requests...
            card_token = generate_card_token(
                card.card_number, card_exp_month, card_exp_year,  card.cvc)
 
            charge_response = create_payment_charge(card_token, 1)

            if charge_response:
                card.save()

            success = charge_response

            return CreatePaymentMethod(success=success)
        except Exception as e:
            print(e)
            raise Exception(Exceptions.Payment.CREATE_FAILED)


class Query(graphene.ObjectType):
    cards = graphene.List(PaymentType)
    get_user_payment_methods = graphene.List(
        PaymentType, arguments=GetUserPaymentMethods(required=True))

    def resolve_cards(root, info, **kwargs):
        return Card.objects.all()

    def resolve_get_user_payment_methods(root, info, **kwargs):
        return Card.objects.filter(uid=kwargs['arguments']['uid'])


class Mutation(graphene.ObjectType):
    create_payment_method = CreatePaymentMethod.Field()


paymentSchema = graphene.Schema(query=Query, mutation=Mutation)
