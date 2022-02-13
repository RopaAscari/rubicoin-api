
import os
import graphene
import firebase_admin
from django.urls import path
from django.contrib import admin
from users.schema import userSchema
from firebase_admin import firestore
from crypto.schema import cryptoSchema
from firebase_admin import credentials
from payment.schema import paymentSchema
from graphene_django.views import GraphQLView
from notification.schema import notificationSchema
from django.views.decorators.csrf import csrf_exempt


ROOT_DIR  = os.path.join( os.path.dirname( __file__ ), '..' )
CERTIFICATE_PATH = os.path.join(
                ROOT_DIR, 'firebase/rubicoin-321a9-firebase-adminsdk-i7fpc-f9617bc7cc.json')

# Use a service account
cred = credentials.Certificate(CERTIFICATE_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()

class Query(userSchema.Query, notificationSchema.Query, cryptoSchema.Query, paymentSchema.Query, graphene.ObjectType):
    pass

class Mutation(userSchema.Mutation,notificationSchema.Mutation, cryptoSchema.Mutation, paymentSchema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
