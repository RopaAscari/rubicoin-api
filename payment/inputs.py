import graphene

class CreatePaymentInput(graphene.InputObjectType):
    uid = graphene.String()
    card_number = graphene.String()
    card_holder_name = graphene.String()
    cvc = graphene.String()  
    address = graphene.String()
    city = graphene.String()
    issuer = graphene.String()
    expiry_date = graphene.String()
    province = graphene.String()
    country = graphene.String()
    postal_code = graphene.String()

class GetUserPaymentMethods(graphene.InputObjectType):
    uid = graphene.String()