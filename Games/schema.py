import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from django.db.models import Q
from Games.models import Games, ContactUs
from graphene import relay


class GamesType(DjangoObjectType):
    class Meta:
        model = Games


class ContactType(DjangoObjectType):
    class Meta:
        model = ContactUs
        filter_fields = ['name']
        # interfaces = (relay.Node,)


'''********************************** Mutation **********************************'''


class GamesInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    game_url = graphene.String()
    image_url = graphene.String()
    category = graphene.String()


class CreateGames(graphene.Mutation):
    class Arguments:
        input = GamesInput(required=True)

    status = graphene.Boolean()
    game = graphene.Field(GamesType)

    @staticmethod
    def mutate(root, info, input=None):
        status = True
        games_instance = Games(name=input.name,
                               game_url=input.game_url,
                               image_url=input.image_url,
                               category=input.category
                               )
        games_instance.save()
        return CreateGames(status=status, game=games_instance)



class UpdateGame(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = GamesInput(required=True)

    status = graphene.Boolean()
    game = graphene.Field(GamesType)

    @staticmethod
    def mutate(root, info, id, input=None):
        status = False
        try:
            game = Games.objects.get(pk=id)
        except Games.DoesNotExist:
            game = None

        if game:
            status = True
            game.name = input.name
            game.game_url = input.game_url
            game.image_url = input.image_url
            game.category = input.category
            game.save()
            return UpdateGame(status=status, game=game)
        return UpdateGame(status=status, game=None)


###############################################################################################


class ContactInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()
    subject = graphene.String()
    message = graphene.String()


class CreateContact(graphene.Mutation):
    class Arguments:
        input = ContactInput(required=True)

    ok = graphene.Boolean()
    contact = graphene.Field(ContactType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        contact_instance = ContactUs(name=input.name, email=input.email, subject=input.subject, message=input.message)
        contact_instance.save()
        return CreateContact(ok=ok, contact=contact_instance)



class DeleteContact(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        ok = False
        try:
            contact_instance = ContactUs.objects.get(pk=id)
        except ContactUs.DoesNotExist:
            contact_instance = None

        if contact_instance:
            ok = True
            contact_instance.delete()
            return DeleteContact(ok=ok)
        return DeleteContact(ok=ok)



class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
    delete_contact = DeleteContact.Field()
    create_game = CreateGames.Field()
    update_game = UpdateGame.Field()


'''********************************** Query **********************************'''


class Query(graphene.ObjectType):
    contact = graphene.Field(ContactType, id=graphene.Int())
    contacts = graphene.List(ContactType,
                             search=graphene.String(),
                             first=graphene.Int(),
                             skip=graphene.Int(),
                             )

    def resolve_contact(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return ContactUs.objects.get(pk=id)
        return None

    def resolve_contacts(self, info, **kwargs):
        user = info.context.user
        print(f"users: {user}")
        # if user.is_anonymous:
        #     raise Exception( 'User not logged in!' )

        search = kwargs.get("search")
        first = kwargs.get( "first" )
        skip = kwargs.get( "skip" )
        if search:
            filter = (
                Q(name__icontains=search) | Q(subject__icontains=search)
            )
            data = ContactUs.objects.filter(filter)
            if skip:
                data = data[skip:]
            if first:
                data = data[:first]
            return data

        data = ContactUs.objects.all()
        if skip:
            data = data[skip:]
        if first:
            data = data[:first]
        return data


    all_games = graphene.List(GamesType)
    game = graphene.Field(GamesType, id=graphene.Int())


    def resolve_all_games(self, info, **kwargs):
        return Games.objects.all()

    def resolve_game(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Games.objects.get(pk=id)

    # all_contact_relay = DjangoFilterConnectionField(ContactType)