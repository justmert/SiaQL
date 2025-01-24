# siaql/graphql/schemas/hostd/__init__.py
import strawberry
from siaql.graphql.schemas.hostd.accounts import AccountQueries
from siaql.graphql.schemas.hostd.alerts import AlertQueries, AlertMutations
from siaql.graphql.schemas.hostd.consensus import ConsensusQueries
from siaql.graphql.schemas.hostd.contracts import ContractQueries, ContractMutations
from siaql.graphql.schemas.hostd.index import IndexQueries
from siaql.graphql.schemas.hostd.metrics import MetricsQueries
from siaql.graphql.schemas.hostd.sectors import SectorQueries, SectorMutations
from siaql.graphql.schemas.hostd.settings import SettingsQueries, SettingsMutations
from siaql.graphql.schemas.hostd.state import StateQueries
from siaql.graphql.schemas.hostd.syncer import SyncerQueries, SyncerMutations
from siaql.graphql.schemas.hostd.system import SystemQueries, SystemMutations
from siaql.graphql.schemas.hostd.tpool import TPoolQueries
from siaql.graphql.schemas.hostd.volumes import VolumeQueries, VolumeMutations
from siaql.graphql.schemas.hostd.wallet import WalletQueries, WalletMutations
from siaql.graphql.schemas.hostd.webhooks import WebhookQueries, WebhookMutations


@strawberry.type
class HostdQuery(
    AccountQueries,
    AlertQueries,
    ConsensusQueries,
    ContractQueries,
    IndexQueries,
    MetricsQueries,
    SectorQueries,
    SettingsQueries,
    StateQueries,
    SyncerQueries,
    SystemQueries,
    TPoolQueries,
    VolumeQueries,
    WalletQueries,
    WebhookQueries,
):
    pass


@strawberry.type
class HostdMutation(
    AlertMutations,
    ContractMutations,
    SectorMutations,
    SettingsMutations,
    SyncerMutations,
    SystemMutations,
    VolumeMutations,
    WalletMutations,
    WebhookMutations,
):
    pass
