# siaql/graphql/schemas/walletd/__init__.py
import strawberry
from siaql.graphql.schemas.renterd.autopilot import AutopilotQueries, AutopilotMutations
from siaql.graphql.schemas.renterd.bus import BusQueries, BusMutations
from siaql.graphql.schemas.renterd.worker import WorkerQueries, WorkerMutations


@strawberry.type
class RenterdQuery(AutopilotQueries, BusQueries, WorkerQueries):
    pass


@strawberry.type
class RenterdMutation(AutopilotMutations, BusMutations, WorkerMutations):
    pass
