# siaql/graphql/schema.py
import strawberry
from siaql.graphql.schemas.walletd import WalletdQuery, WalletdMutation
from siaql.graphql.schemas.renterd import RenterdQuery, RenterdMutation
from siaql.graphql.schemas.hostd import HostdQuery, HostdMutation

from typing import Optional, List
from siaql.graphql.resolvers.filter import FilterOperator, SortInput, PaginationInput
from strawberry.schema.config import StrawberryConfig
from strawberry.extensions import ValidationCache
from strawberry.extensions import ParserCache
from typing import Dict
from strawberry.types import Info
from typing import Any, Dict, List, Optional, Callable
from strawberry.extensions import SchemaExtension


@strawberry.type
class Query(WalletdQuery, RenterdQuery, HostdQuery):
    pass


@strawberry.type
class Mutation(WalletdMutation, RenterdMutation, HostdMutation):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        ValidationCache(),
        ParserCache(),
    ],
    config=StrawberryConfig(auto_camel_case=True),
)
