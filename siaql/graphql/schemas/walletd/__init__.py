# siaql/graphql/schemas/walletd/__init__.py
import strawberry
from .addresses import AddressQueries
from .consensus import ConsensusQueries
from .events import EventQueries
from .syncer import SyncerQueries, SyncerMutations
from .txpool import TransactionPoolQueries, TransactionPoolMutations

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
class Mutation(
    SyncerMutations,
    TransactionPoolMutations
):
    pass

__all__ = [
    'Query',
    'Mutation',
    'AddressQueries',
    'ConsensusQueries',
    'EventQueries',
    'SyncerQueries',
    'SyncerMutations',
    'TransactionPoolQueries',
    'TransactionPoolMutations'
]