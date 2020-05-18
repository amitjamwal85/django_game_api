import graphene
from Games.schema import Query as GameQuery
from User.schema import Query as UserQuery
from GraphQLTest.schema import Query as MoviesQuery
from GraphQLTest.schema import Mutation as MoviesMutation
from Games.schema import Mutation as GameMutation
import graphql_jwt


class Query(MoviesQuery, GameQuery, UserQuery, graphene.ObjectType):
    pass


class Mutation(MoviesMutation, GameMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)


