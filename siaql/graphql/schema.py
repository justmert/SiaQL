# siaql/graphql/schema.py
import strawberry
# from siaql.graphql.schemas.walletd import Query, Mutation
from siaql.graphql.schemas.walletd import Query, Mutation

# Create the schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)