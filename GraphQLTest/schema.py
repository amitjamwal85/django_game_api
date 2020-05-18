import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from GraphQLTest.models import Actor, Movie


'''********************************** GraphQL Types **********************************'''


class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


'''********************************** Mutation **********************************'''


class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()


class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actors = []
        for actors_input in input.actors:
            actor = Actor.objects.get(pk=actors_input.id)
            if actor is None:
                return CreateMovie(ok=ok, movie=False)
            actors.append(actor)

        movie_instance = Movie(
            title=input.title,
            year=input.year
        )
        movie_instance.save()
        movie_instance.actors.set(actors)
        return CreateMovie(ok=ok, movie=movie_instance)


class CreateActor(graphene.Mutation):
    class Arguments:
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actor_instance = Actor(name=input.name)
        actor_instance.save()
        return CreateActor(ok=ok, actor=actor_instance)


class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        actor_instance = Actor.objects.get(pk=id)
        if actor_instance:
            ok = True
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(ok=ok, actor=actor_instance)
        return UpdateActor(ok=ok, actor=None)



class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        moive_instance = Movie.objects.get(pk=id)
        if moive_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
                actor = Actor.objects.get(pk=actor_input.id)
                if actor is None:
                    return UpdateMovie(ok=ok, movie=None)
                actors.append(actor)

            moive_instance.title = input.title
            moive_instance.year = input.year
            moive_instance.actors.set(actors)
            moive_instance.save()
            return UpdateMovie(ok=ok, movie=moive_instance)
        return UpdateMovie(ok=ok, movie=None)


'''********************************** MutationType **********************************'''


class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()


'''********************************** Query **********************************'''


class Query(ObjectType):
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)

    def resolve_actor(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Actor.objects.get(pk=id)
        return None


    def resolve_movie(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Movie.objects.get(pk=id)
        return None

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return  Movie.objects.all()

