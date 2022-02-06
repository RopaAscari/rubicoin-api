import graphene

class USD(graphene.Interface):
    price = graphene.Float()

class Quote(graphene.Interface):
    USD = USD

class AssetType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    slug = graphene.String()
    price = graphene.Float()
    symbol = graphene.String()
    date_added = graphene.Date()
    market_cap = graphene.Float()
    num_market_pairs = graphene.Int()
    percent_change_1h = graphene.Float()
    
