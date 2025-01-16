# siaql/graphql/schemas/walletd/__init__.py
import strawberry
from siaql.graphql.schemas.walletd.addresses import AddressQueries
from siaql.graphql.schemas.walletd.events import EventQueries
from siaql.graphql.schemas.walletd.consensus import ConsensusQueries
from siaql.graphql.schemas.walletd.syncer import SyncerQueries, SyncerMutations
from siaql.graphql.schemas.walletd.txpool import (
    TransactionPoolQueries,
    TransactionPoolMutations
)

@strawberry.type
class Query(
    AddressQueries,
    EventQueries,
    ConsensusQueries,
    SyncerQueries,
    TransactionPoolQueries
):
    @strawberry.field
    def hello(self) -> str:
        """Test query to verify GraphQL is working"""
        return "Welcome to SiaQL - Walletd API"

@strawberry.type
class Mutation(SyncerMutations, TransactionPoolMutations):
    pass

__all__ = [
    'Query',
    'Mutation',
    'AddressQueries',
    'EventQueries',
    'ConsensusQueries',
    'SyncerQueries',
    'TransactionPoolQueries'
]