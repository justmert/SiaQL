# siaql/graphql/schemas/walletd/__init__.py
import strawberry
from siaql.graphql.schemas.walletd.addresses import AddressQueries
from siaql.graphql.schemas.walletd.consensus import ConsensusQueries
from siaql.graphql.schemas.walletd.state import StateQueries
from siaql.graphql.schemas.walletd.syncer import SyncerQueries
from siaql.graphql.schemas.walletd.txpool import TxpoolQueries
from siaql.graphql.schemas.walletd.wallets import WalletQueries
from siaql.graphql.schemas.walletd.txpool import TxpoolMutations
from siaql.graphql.schemas.walletd.syncer import SyncerMutations
from siaql.graphql.schemas.walletd.wallets import WalletMutations
from siaql.graphql.schemas.walletd.rescan import RescanQueries
from siaql.graphql.schemas.walletd.rescan import RescanMutations
from siaql.graphql.schemas.walletd.events import EventQueries





@strawberry.type
class Query(
    AddressQueries,
    ConsensusQueries,
    EventQueries,
    RescanQueries,
    StateQueries,
    SyncerQueries,
    TxpoolQueries,
    WalletQueries,
):
    @strawberry.field
    def hello(self) -> str:
        """Test query to verify GraphQL is working"""
        return "Welcome to SiaQL - Walletd API"

@strawberry.type
class Mutation(
    RescanMutations,
    SyncerMutations,
    # TxpoolMutations,
    # WalletMutations,
):
    pass
