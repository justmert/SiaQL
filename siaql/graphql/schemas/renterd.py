# siaql/graphql/schemas/walletd/__init__.py
import strawberry
from siaql.graphql.schemas.renterd.bus import BusQueries, BusMutations
from siaql.graphql.schemas.renterd.autopilot import AutopilotQueries, AutopilotMutations
from siaql.graphql.schemas.renterd.worker import WorkerQueries, WorkerMutations

@strawberry.type
class Query(
    BusQueries,
    AutopilotQueries,
    WorkerQueries,
):
    @strawberry.field
    def hello(self) -> str:
        """Test query to verify GraphQL is working"""
        return "Welcome to SiaQL - Renterd API"

@strawberry.type
class Mutation(
    BusMutations,
    AutopilotMutations,
    WorkerMutations,
):
    pass

__all__ = [
    'Query',
    'Mutation',
    'BusQueries',
    'AutopilotQueries',
    'WorkerQueries',
]