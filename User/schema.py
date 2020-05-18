import graphene
from graphene import relay
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
# from User.models import UserProfile
from User.models import UserProfile


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['username', 'first_name']
        interfaces = (relay.Node, )



class UserProfileNode(DjangoObjectType):
    class Meta:
        model = UserProfile
        filter_fields = {
            'city': ['exact', 'icontains', 'istartswith'],
            'country': ['exact', 'icontains'],
            'user': ['exact'],
            'user__first_name': ['exact']
        }
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    userprofile = relay.Node.Field(UserProfileNode)
    all_userprofile = DjangoFilterConnectionField(UserProfileNode)



