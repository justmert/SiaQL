from typing import List, Optional, Union
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from strawberry.scalars import JSON
from typing import List, Optional, Dict, Any
from enum import Enum

# INTERFACES
# *******************************************

@strawberry.interface
class SiaType:
    """Base interface for types converted from Sia network API responses"""

    pass


@strawberry.interface
class SiaInput:
    """Base interface for types converted from Sia network API responses"""

    pass


strawberry.interface


class NewType:
    """Base interface for types converted from Sia network API responses"""

    pass


@strawberry.type
class Hash256(SiaType):
    # A Hash256 is a generic 256-bit cryptographic hash
    value: str = strawberry.field(description="hex-encoded 32-byte hash")


@strawberry.type
class AttestationID(SiaType):
    value: Hash256 = strawberry.field(description="uniquely identifies an attestation")


@strawberry.type
class FileContractID(SiaType):
    value: Hash256 = strawberry.field(description="uniquely identifies an attestation")


@strawberry.type
class PublicKey(SiaType):
    value: str = strawberry.field(description="hex-encoded 32-byte public key")


@strawberry.type
class PrivateKey(SiaType):
    value: str = strawberry.field(description="hex-encoded private key")


@strawberry.type
class Signature(SiaType):
    value: str = strawberry.field(description="hex-encoded 64-byte signature")


@strawberry.type
class Specifier(SiaType):
    value: str = strawberry.field(description="16-byte identifier")


@strawberry.type
class Address(SiaType):
    value: Hash256 = strawberry.field(description="uniquely identifies an attestation")


@strawberry.type
class BlockID(SiaType):
    value: Hash256 = strawberry.field(description="uniquely identifies a block")


@strawberry.type
class TransactionID(SiaType):
    value: Hash256 = strawberry.field(description="uniquely identifies a transaction")


@strawberry.type
class Balance(SiaType):
    siacoins: str  # Currency
    immature_siacoins: str = strawberry.field(name="immatureSiacoins")  # Currency
    siafunds: int


@strawberry.type
class AddressBalance(SiaType):
    address: Address = strawberry.field(name="address")
    balance: Balance = strawberry.field(name="balance")


@strawberry.type
class HardforkDevAddr(SiaType):
    height: int = strawberry.field()
    old_address: Address = strawberry.field(name="oldAddress")
    new_address: Address = strawberry.field(name="newAddress")


@strawberry.type
class HardforkTax(SiaType):
    height: int = strawberry.field(name="height")


@strawberry.type
class HardforkStorageProof(SiaType):
    height: int = strawberry.field(name="height")


@strawberry.type
class HardforkOak(SiaType):
    height: int = strawberry.field(name="height")
    fix_height: int = strawberry.field(name="fixHeight")
    genesis_timestamp: datetime = strawberry.field(name="genesisTimestamp")  # time.time


@strawberry.type
class HardforkASIC(SiaType):
    height: int = strawberry.field(name="height")
    oak_time: str = strawberry.field(name="oakTime")  # time.Duration
    oak_target: BlockID = strawberry.field(name="oakTarget")


@strawberry.type
class HardforkFoundation(SiaType):
    height: int = strawberry.field(name="height")
    primary_address: Address = strawberry.field(name="primaryAddress")
    failsafe_address: Address = strawberry.field(name="failsafeAddress")


@strawberry.type
class HardforkV2(SiaType):
    allow_height: int = strawberry.field(name="allowHeight")
    require_height: int = strawberry.field(name="requireHeight")


@strawberry.input
class NetworkInput(SiaInput):
    name: Optional[str] = strawberry.field(description="""The name of the network""", default=None)
    initial_coinbase: Optional[str] = strawberry.field(default=None, name="initialCoinbase")
    minimum_coinbase: Optional[str] = strawberry.field(default=None, name="minimumCoinbase")
    initial_target: Optional[BlockID] = strawberry.field(default=None, name="initialTarget")
    block_interval: Optional[int] = strawberry.field(
        description="""The block interval | Format: uint64""", default=600000000000, name="blockInterval"
    )
    maturity_delay: Optional[int] = strawberry.field(
        description="""The maturity delay | Format: uint64""", default=144, name="maturityDelay"
    )
    hardfork_dev_addr: Optional[HardforkDevAddr] = strawberry.field(default=None, name="hardforkDevAddr")
    hardfork_tax: Optional[HardforkTax] = strawberry.field(default=None, name="hardforkTax")
    hardfork_storage_proof: Optional[HardforkStorageProof] = strawberry.field(default=None, name="hardforkStorageProof")
    hardfork_oak: Optional[HardforkOak] = strawberry.field(default=None, name="hardforkOak")
    hardfork_asic: Optional[HardforkASIC] = strawberry.field(default=None, name="hardforkASIC")
    hardfork_foundation: Optional[HardforkFoundation] = strawberry.field(default=None, name="hardforkFoundation")
    hardfork_v2: Optional[HardforkV2] = strawberry.field(default=None, name="hardforkV2")
 

@strawberry.type
class MerkleProof:
    hashes: List[Hash256]


@strawberry.type
class BlockIndex:
    height: int
    id: str


@strawberry.input
class SiacoinRecipientInput:
    address: str
    value: str


@strawberry.input
class SiafundRecipientInput:
    address: str
    value: int


# Response Types
@strawberry.type
class BroadcastResponse:
    success: bool
    message: Optional[str] = None


@strawberry.type
class ReserveUTXOsResponse:
    success: bool
    message: Optional[str] = None


@strawberry.type
class ReleaseUTXOsResponse:
    success: bool
    message: Optional[str] = None


@strawberry.type
class AddWalletAddressResponse:
    success: bool
    message: Optional[str] = None


@strawberry.type
class DeleteWalletResponse:
    success: bool
    message: Optional[str] = None


@strawberry.type
class DeleteWalletAddressResponse:
    success: bool
    message: Optional[str] = None


@strawberry.type
class NetworkInfo:
    name: str
    initial_coinbase: str = strawberry.field(name="initialCoinbase")
    minimum_coinbase: str = strawberry.field(name="minimumCoinbase")
    initial_target: str = strawberry.field(name="initialTarget")
    hardfork_dev_addr: HardforkDevAddr = strawberry.field(name="hardforkDevAddr")
    hardfork_tax: HardforkTax = strawberry.field(name="hardforkTax")
    hardfork_storage_proof: HardforkStorageProof = strawberry.field(name="hardforkStorageProof")
    hardfork_oak: HardforkOak = strawberry.field(name="hardforkOak")
    hardfork_asic: HardforkASIC = strawberry.field(name="hardforkASIC")
    hardfork_foundation: HardforkFoundation = strawberry.field(name="hardforkFoundation")
    hardfork_v2: HardforkV2 = strawberry.field(name="hardforkV2")


@strawberry.type
class ElementsInfo:
    num_leaves: int = strawberry.field(name="numLeaves")
    trees: List[str]


@strawberry.type
class MinerEventData:
    siacoin_element: SiacoinElement = strawberry.field(name="siacoinElement")


@strawberry.type
class Peer:
    addr: str
    inbound: bool
    version: str
    first_seen: datetime = strawberry.field(name="firstSeen")
    connected_since: datetime = strawberry.field(name="connectedSince")
    synced_blocks: int = strawberry.field(name="syncedBlocks")
    sync_duration: int = strawberry.field(name="syncDuration")


@strawberry.type
class ConnectPeerResponse:
    success: bool
    message: Optional[str] = None


@strawberry.type
class RescanStatus:
    start_index: BlockIndex = strawberry.field(name="startIndex")
    index: BlockIndex
    start_time: datetime = strawberry.field(name="startTime")


@strawberry.type
class StartRescanResponse:
    success: bool
    message: Optional[str] = None


@strawberry.type
class SiacoinRecipient:
    address: str
    value: str


@strawberry.type
class SiafundRecipient:
    address: str
    value: int


@strawberry.type
class TransactionBasis:
    height: int
    id: str


@strawberry.type
class ConstructedTransaction:
    basis: TransactionBasis
    id: str
    transaction: Dict[str, Any] = strawberry.field(description="The constructed transaction")
    estimated_fee: str = strawberry.field(name="estimatedFee")


@strawberry.type
class Wallet:
    id: str
    name: str
    description: str
    date_created: datetime = strawberry.field(name="dateCreated")
    last_updated: datetime = strawberry.field(name="lastUpdated")
    metadata: Optional[Dict[str, Any]] = None


@strawberry.type
class WalletAddress:
    address: str
    description: str
    metadata: Optional[Dict[str, Any]] = None


@strawberry.input
class AddWalletInput:
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@strawberry.input
class AddWalletAddressInput:
    address: str
    description: Optional[str] = None
    spend_policy: Optional[Dict[str, Any]] = strawberry.field(name="spendPolicy", default=None)
    metadata: Optional[Dict[str, Any]] = None


@strawberry.type
class V1Transaction:
    siacoin_inputs: List[SiacoinInput] = strawberry.field(name="siacoinInputs")
    siacoin_outputs: List[SiacoinOutput] = strawberry.field(name="siacoinOutputs")
    miner_fees: List[str] = strawberry.field(name="minerFees")
    signatures: List[TransactionSignature]


@strawberry.type
class TransactionData:
    transaction: V1Transaction
    spent_siacoin_elements: Optional[List[Dict[str, Any]]] = strawberry.field(name="spentSiacoinElements", default=None)
    spent_siafund_elements: Optional[List[Dict[str, Any]]] = strawberry.field(name="spentSiafundElements", default=None)


@strawberry.type
class Currency:
    """Represents a quantity of hastings as an unsigned 128-bit number."""

    lo: int  # uint64
    hi: int  # uint64


@strawberry.type
class WalletEvent:
    id: str
    index: BlockIndex
    timestamp: datetime
    maturity_height: int = strawberry.field(name="maturityHeight")
    type: str
    data: TransactionData
    relevant: List[str]


@strawberry.type
class WalletBalance:
    siacoins: str
    immature_siacoins: str = strawberry.field(name="immatureSiacoins")
    siafunds: int


@strawberry.type
class SiacoinUTXO:
    id: str
    leaf_index: int = strawberry.field(name="leafIndex")
    merkle_proof: MerkleProof = strawberry.field(name="merkleProof")
    siacoin_output: SiacoinOutput = strawberry.field(name="siacoinOutput")
    maturity_height: int = strawberry.field(name="maturityHeight")


@strawberry.type
class SiafundUTXO:
    id: str
    leaf_index: int = strawberry.field(name="leafIndex")
    merkle_proof: MerkleProof = strawberry.field(name="merkleProof")
    siafund_output: SiafundOutput = strawberry.field(name="siafundOutput")
    claim_start: str = strawberry.field(name="claimStart")


@strawberry.type
class FundTransactionResponse:
    transaction: Transaction
    to_sign: List[str] = strawberry.field(name="toSign")
    depends_on: Optional[List[str]] = strawberry.field(name="dependsOn", default=None)


# ---


@strawberry.enum
class PolicyType(Enum):
    """Enumerates the different types of spend policies."""

    ABOVE = "above"
    AFTER = "after"
    PUBLIC_KEY = "publicKey"
    HASH = "hash"
    THRESHOLD = "threshold"
    OPAQUE = "opaque"
    UNLOCK_CONDITIONS = "unlockConditions"


@strawberry.type
class PolicyTypeAbove:
    """Policy requiring block height to be above a certain value."""

    height: int = strawberry.field()


@strawberry.type
class PolicyTypeAfter:
    """Policy requiring timestamp to be after a certain time."""

    timestamp: datetime = strawberry.field()


@strawberry.type
class PolicyTypePublicKey:
    """Policy requiring a valid signature from a specific public key."""

    public_key: str = strawberry.field(name="publicKey")


@strawberry.type
class PolicyTypeHash:
    """Policy requiring a preimage that hashes to a specific value."""

    hash: str = strawberry.field(description="32-byte hash in hex format")


@strawberry.type
class PolicyTypeThreshold:
    """Policy requiring M-of-N sub-policies to be satisfied."""

    minimum: int = strawberry.field()
    sub_policies: List["SpendPolicy"] = strawberry.field(name="subPolicies")


@strawberry.type
class PolicyTypeOpaque:
    """Policy representing an unknown/opaque set of conditions."""

    address: str = strawberry.field()


@strawberry.type
class PolicyTypeUnlockConditions:
    """Policy requiring standard unlock conditions to be satisfied."""

    conditions: UnlockConditions = strawberry.field()


@strawberry.type
class SpendPolicy:
    """
    A SpendPolicy describes the conditions under which an input may be spent.
    """

    policy_type: PolicyType = strawberry.field(name="type")
    above: Optional[PolicyTypeAbove] = strawberry.field(default=None)
    after: Optional[PolicyTypeAfter] = strawberry.field(default=None)
    public_key: Optional[PolicyTypePublicKey] = strawberry.field(name="publicKey", default=None)
    hash: Optional[PolicyTypeHash] = strawberry.field(default=None)
    threshold: Optional[PolicyTypeThreshold] = strawberry.field(default=None)
    opaque: Optional[PolicyTypeOpaque] = strawberry.field(default=None)
    unlock_conditions: Optional[PolicyTypeUnlockConditions] = strawberry.field(name="unlockConditions", default=None)


@strawberry.enum
class V2FileContractResolutionType(Enum):
    """Enumerates the types of file contract resolution."""

    RENEWAL = "renewal"
    STORAGE_PROOF = "storageProof"
    EXPIRATION = "expiration"


@strawberry.type
class V2FileContractRenewal:
    final_renter_output: SiacoinOutput = strawberry.field(name="finalRenterOutput")
    final_host_output: SiacoinOutput = strawberry.field(name="finalHostOutput")
    renter_rollover: str = strawberry.field(name="renterRollover", description="Currency amount")
    host_rollover: str = strawberry.field(name="hostRollover", description="Currency amount")
    new_contract: V2FileContract = strawberry.field(name="newContract")
    renter_signature: str = strawberry.field(name="renterSignature")
    host_signature: str = strawberry.field(name="hostSignature")


@strawberry.type
class V1TransactionEventData:
    transaction: Transaction  # Changed from dict to Transaction type
    spent_siacoin_elements: Optional[List[SiacoinElement]] = strawberry.field(
        name="spentSiacoinElements", description="Elements spent by this transaction"
    )
    spent_siafund_elements: Optional[List[SiafundElement]] = strawberry.field(
        name="spentSiafundElements", description="Siafund elements spent by this transaction"
    )


@strawberry.type
class V2TransactionEventData:
    transaction: V2Transaction
    spent_siacoin_elements: Optional[List[SiacoinElement]] = strawberry.field(name="spentSiacoinElements")
    spent_siafund_elements: Optional[List[SiafundElement]] = strawberry.field(name="spentSiafundElements")


@strawberry.type
class V2TransactionsMultiproof:
    """A slice of V2Transactions whose Merkle proofs are encoded as a single multiproof."""

    transactions: List[V2Transaction]


@strawberry.type
class ElementID:
    """A generic 32-byte identifier within the state accumulator."""

    value: str = strawberry.field(
        description="32-byte identifier for BlockID, SiacoinOutputID, SiafundOutputID, FileContractID, or AttestationID"
    )


@strawberry.type
class FileContractElement:
    id: FileContractID
    state_element: StateElement = strawberry.field(name="stateElement")
    file_contract: FileContract = strawberry.field(name="fileContract")


@strawberry.type
class ChainIndexElement:
    """A record of a ChainIndex within the state accumulator."""

    id: BlockID
    state_element: StateElement = strawberry.field(name="stateElement")
    chain_index: ChainIndex = strawberry.field(name="chainIndex")


@strawberry.type
class V2StorageProof:
    proof_index: ChainIndexElement = strawberry.field(name="proofIndex")
    leaf: str = strawberry.field(description="hex-encoded 64-byte leaf")
    proof: List[Hash256]


@strawberry.type
class TipState:
    index: ChainIndex
    prev_timestamps: List[datetime] = strawberry.field(name="prevTimestamps")
    depth: str
    child_target: str = strawberry.field(name="childTarget")
    siafund_pool: str = strawberry.field(name="siafundPool")
    oak_time: str = strawberry.field(name="oakTime")
    oak_target: str = strawberry.field(name="oakTarget")
    foundation_primary_address: str = strawberry.field(name="foundationPrimaryAddress")
    foundation_failsafe_address: str = strawberry.field(name="foundationFailsafeAddress")
    total_work: str = strawberry.field(name="totalWork")
    difficulty: str
    oak_work: str = strawberry.field(name="oakWork")
    elements: ElementsInfo
    attestations: int


@strawberry.type
class BlockHeader:
    """The preimage of a Block's ID."""

    parent_id: str = strawberry.field(name="parentID")
    nonce: int
    timestamp: datetime
    commitment: str


@strawberry.type
class V2FileContractExpiration:
    """
    A V2FileContractExpiration resolves an expired contract. A contract is
    considered expired when its proof window has elapsed. If the contract is not
    storing any data, it will resolve as valid; otherwise, it resolves as missed.
    """

    pass  # This type is empty in Go as well


@strawberry.type
class FoundationAddressUpdate:
    """Updates the primary and failsafe Foundation subsidy addresses."""

    new_primary: str = strawberry.field(name="newPrimary")
    new_failsafe: str = strawberry.field(name="newFailsafe")


@strawberry.type
class AttestationElement:
    """A record of an Attestation within the state accumulator."""

    id: AttestationID
    state_element: StateElement = strawberry.field(name="stateElement")
    attestation: Attestation


@strawberry.type
class TransactionWithoutSignatures:
    """Helper type for calculating transaction IDs without signature data."""

    siacoin_inputs: List[SiacoinInput] = strawberry.field(name="siacoinInputs")
    siacoin_outputs: List[SiacoinOutput] = strawberry.field(name="siacoinOutputs")
    file_contracts: List[FileContract] = strawberry.field(name="fileContracts")
    file_contract_revisions: List[FileContractRevision] = strawberry.field(name="fileContractRevisions")
    storage_proofs: List[StorageProof] = strawberry.field(name="storageProofs")
    siafund_inputs: List[SiafundInput] = strawberry.field(name="siafundInputs")
    siafund_outputs: List[SiafundOutput] = strawberry.field(name="siafundOutputs")
    miner_fees: List[Currency] = strawberry.field(name="minerFees")
    arbitrary_data: List[str] = strawberry.field(name="arbitraryData", description="hex-encoded arbitrary data")


@strawberry.type
class AlertData:
    account_id: str = strawberry.field(name="accountID")
    contract_id: str = strawberry.field(name="contractID")
    host_key: str = strawberry.field(name="hostKey")
    origin: str


@strawberry.input
class AlertsParams:
    offset: Optional[int] = 0
    limit: Optional[int] = -1


@strawberry.input
class AlertDataInput:
    account_id: str = strawberry.field(name="accountID")
    contract_id: str = strawberry.field(name="contractID")
    host_key: str = strawberry.field(name="hostKey")
    origin: str


@strawberry.type
class ContractConfig:
    set: str
    amount: int
    allowance: str
    period: int
    renew_window: int = strawberry.field(name="renewWindow")
    download: int
    upload: int
    storage: int


@strawberry.type
class WalletConfig:
    defrag_threshold: int = strawberry.field(name="defragThreshold")


@strawberry.type
class Autopilot:
    id: str
    config: AutopilotConfig
    current_period: int = strawberry.field(name="currentPeriod")


@strawberry.type
class Contract:
    id: str
    host_ip: str = strawberry.field(name="hostIP")
    host_key: str = strawberry.field(name="hostKey")
    siamux_addr: str = strawberry.field(name="siamuxAddr")
    proof_height: int = strawberry.field(name="proofHeight")
    revision_height: int = strawberry.field(name="revisionHeight")
    revision_number: int = strawberry.field(name="revisionNumber")
    start_height: int = strawberry.field(name="startHeight")
    window_start: int = strawberry.field(name="windowStart")
    window_end: int = strawberry.field(name="windowEnd")
    renewed_from: str = strawberry.field(name="renewedFrom")
    spending: ContractSpending
    total_cost: str = strawberry.field(name="totalCost")
    size: Optional[int] = None
    state: Optional[str] = None
    contract_price: Optional[str] = strawberry.field(name="contractPrice", default=None)
    sets: Optional[List[str]] = None


@strawberry.type
class ContractPrunableInfo:
    id: str
    prunable: int
    size: int


@strawberry.type
class ContractsPrunableInfo:
    contracts: List[ContractPrunableInfo]
    total_prunable: int = strawberry.field(name="totalPrunable")
    total_size: int = strawberry.field(name="totalSize")


@strawberry.type
class ContractRoots:
    roots: List[str]


@strawberry.type
class ArchivedContract:
    id: str
    host_key: str = strawberry.field(name="hostKey")
    renewed_to: str = strawberry.field(name="renewedTo")
    spending: ContractSpending
    proof_height: int = strawberry.field(name="proofHeight")
    revision_height: int = strawberry.field(name="revisionHeight")
    revision_number: int = strawberry.field(name="revisionNumber")
    size: int
    start_height: int = strawberry.field(name="startHeight")
    state: str
    window_start: int = strawberry.field(name="windowStart")
    window_end: int = strawberry.field(name="windowEnd")


@strawberry.type
class ContractLock:
    lock_id: int = strawberry.field(name="lockID")


@strawberry.input
class ContractAcquireInput:
    duration: str
    priority: int


@strawberry.input
class ContractLockInput:
    lock_id: int = strawberry.field(name="lockID")


@strawberry.input
class HostAllowlistInput:
    add: List[str]
    remove: List[str]
    clear: bool


@strawberry.input
class HostBlocklistInput:
    add: List[str]
    remove: List[str]
    clear: bool


@strawberry.type
class ContractPrunable:
    contracts: List[ContractPrunableInfo]
    total_prunable: int = strawberry.field(name="totalPrunable")
    total_size: int = strawberry.field(name="totalSize")


@strawberry.type
class ScanningHost:
    public_key: str = strawberry.field(name="publicKey")
    net_address: str = strawberry.field(name="netAddress")


@strawberry.input
class HostListUpdateInput:
    add: List[str]
    remove: List[str]
    clear: bool


@strawberry.input
class HostRemoveInput:
    min_recent_scan_failures: int = strawberry.field(name="minRecentScanFailures")
    max_downtime_hours: str = strawberry.field(name="maxDowntimeHours")


@strawberry.input
class ScanningParams:
    offset: Optional[int] = 0
    limit: Optional[int] = -1
    last_scan: Optional[str] = strawberry.field(name="lastScan", default=None)


@strawberry.type
class ChurnMetric:
    direction: str
    contract_id: str = strawberry.field(name="contractID")
    name: str
    timestamp: str


@strawberry.type
class ContractSetMetric:
    contracts: int
    name: str
    timestamp: str

@strawberry.type
class Object:
    metadata: "ObjectUserMetadata"
    object_metadata: ObjectMetadata = strawberry.field(name="objectMetadata")


@strawberry.type
class ObjectUserMetadata:
    data: typing.Dict[str, str]

@strawberry.input
class MetricParams:
    start: str
    interval: int
    n: int
    contract_id: Optional[str] = strawberry.field(name="contractID", default=None)
    host_key: Optional[str] = strawberry.field(name="hostKey", default=None)
    name: Optional[str] = None
    direction: Optional[str] = None
    reason: Optional[str] = None
    host_version: Optional[str] = strawberry.field(name="hostVersion", default=None)


@strawberry.type
class PriceTable:
    uid: str
    validity: int
    host_block_height: int = strawberry.field(name="hostblockheight")
    update_pricetable_cost: str = strawberry.field(name="updatepricetablecost")
    account_balance_cost: str = strawberry.field(name="accountbalancecost")
    fund_account_cost: str = strawberry.field(name="fundaccountcost")
    latest_revision_cost: str = strawberry.field(name="latestrevisioncost")
    subscription_memory_cost: str = strawberry.field(name="subscriptionmemorycost")
    subscription_notification_cost: str = strawberry.field(name="subscriptionnotificationcost")
    init_base_cost: str = strawberry.field(name="initbasecost")
    memory_time_cost: str = strawberry.field(name="memorytimecost")
    download_bandwidth_cost: str = strawberry.field(name="downloadbandwidthcost")
    upload_bandwidth_cost: str = strawberry.field(name="uploadbandwidthcost")
    drop_sectors_base_cost: str = strawberry.field(name="dropsectorsbasecost")
    drop_sectors_unit_cost: str = strawberry.field(name="dropsectorsunitcost")
    has_sector_base_cost: str = strawberry.field(name="hassectorbasecost")
    read_base_cost: str = strawberry.field(name="readbasecost")
    read_length_cost: str = strawberry.field(name="readlengthcost")
    renew_contract_cost: str = strawberry.field(name="renewcontractcost")
    revision_base_cost: str = strawberry.field(name="revisionbasecost")
    swap_sector_cost: str = strawberry.field(name="swapsectorcost")
    write_base_cost: str = strawberry.field(name="writebasecost")
    write_length_cost: str = strawberry.field(name="writelengthcost")
    write_store_cost: str = strawberry.field(name="writestorecost")
    txn_fee_min_recommended: str = strawberry.field(name="txnfeeminrecommended")
    txn_fee_max_recommended: str = strawberry.field(name="txnfeemaxrecommended")
    contract_price: str = strawberry.field(name="contractprice")
    collateral_cost: str = strawberry.field(name="collateralcost")
    max_collateral: str = strawberry.field(name="maxcollateral")
    max_duration: int = strawberry.field(name="maxduration")
    window_size: int = strawberry.field(name="windowsize")
    registry_entries_left: int = strawberry.field(name="registryentriesleft")
    registry_entries_total: int = strawberry.field(name="registryentriestotal")


@strawberry.input
class HostInteractionInput:
    host: str
    result: Dict[str, Any]
    success: bool
    timestamp: str
    type: str


@strawberry.type
class ContractSet:
    name: str


@strawberry.input
class ContractSetInput:
    contract_ids: List[str]


@strawberry.input
class ContractSpendingUpdate:
    contract_id: str = strawberry.field(name="contractID")
    revision_number: int = strawberry.field(name="revisionNumber")
    size: int
    uploads: str
    deletions: str
    downloads: str
    fund_account: str = strawberry.field(name="fundAccount")
    sector_roots: str = strawberry.field(name="sectorRoots")


@strawberry.type
class ContractRenewedInfo:
    id: str
    host_ip: str = strawberry.field(name="hostIP")
    host_key: str = strawberry.field(name="hostKey")
    siamux_addr: str = strawberry.field(name="siamuxAddr")
    proof_height: int = strawberry.field(name="proofHeight")
    revision_height: int = strawberry.field(name="revisionHeight")
    revision_number: int = strawberry.field(name="revisionNumber")
    size: int
    start_height: int = strawberry.field(name="startHeight")
    window_start: int = strawberry.field(name="windowStart")
    window_end: int = strawberry.field(name="windowEnd")
    renewed_from: str = strawberry.field(name="renewedFrom")
    spending: ContractSpending
    total_cost: str = strawberry.field(name="totalCost")


@strawberry.type
class MultipartUploadInfo:
    upload_id: str = strawberry.field(name="uploadID")


@strawberry.type
class MultipartUploadsResponse:
    uploads: List[MultipartUpload]


@strawberry.type
class CompleteMultipartUploadResponse:
    e_tag: str = strawberry.field(name="eTag")


@strawberry.input
class PartInput:
    part_number: int = strawberry.field(name="partNumber")
    e_tag: str = strawberry.field(name="eTag")


@strawberry.input
class MultipartUploadAbortInput:
    bucket: str
    path: str
    upload_id: str = strawberry.field(name="uploadID")


@strawberry.input
class MultipartUploadCompleteInput:
    bucket: str
    path: str
    upload_id: str = strawberry.field(name="uploadID")
    parts: List[PartInput]


@strawberry.input
class MultipartUploadListPartsInput:
    bucket: str
    path: str
    upload_id: str = strawberry.field(name="uploadID")
    part_number_marker: int = strawberry.field(name="partNumberMarker", default=0)
    limit: int = 1000


@strawberry.input
class MultipartUploadListInput:
    bucket: str
    prefix: str = ""
    path_marker: str = strawberry.field(name="pathMarker", default="")
    upload_id_marker: str = strawberry.field(name="uploadIDMarker", default="")
    limit: int = 1000


# types.py - Object Types


@strawberry.type
class ShardContract:
    contracts: Dict[str, List[str]]
    latest_host: str = strawberry.field(name="latestHost")
    root: str


@strawberry.type
class SlabShard:
    health: float
    key: str
    min_shards: int = strawberry.field(name="minShards")
    shards: List[ShardContract]


@strawberry.type
class ObjectResponse:
    has_more: bool = strawberry.field(name="hasMore")
    object: ObjectInfo


@strawberry.type
class ObjectListEntry:
    name: str
    size: int
    health: float


@strawberry.type
class DownloadGougingSettings:
    min_max_collateral: str = strawberry.field(name="minMaxCollateral")
    max_rpc_price: str = strawberry.field(name="maxRPCPrice")
    max_contract_price: str = strawberry.field(name="maxContractPrice")
    max_download_price: str = strawberry.field(name="maxDownloadPrice")
    max_upload_price: str = strawberry.field(name="maxUploadPrice")
    max_storage_price: str = strawberry.field(name="maxStoragePrice")
    host_block_height_leeway: int = strawberry.field(name="hostBlockHeightLeeway")


@strawberry.type
class DownloadConsensusState:
    block_height: int = strawberry.field(name="BlockHeight")
    synced: bool = strawberry.field(name="Synced")


@strawberry.type
class DownloadParameters:
    contract_set: str = strawberry.field(name="ContractSet")
    consensus_state: ConsensusState = strawberry.field(name="ConsensusState")
    gouging_settings: GougingSettings = strawberry.field(name="GougingSettings")
    redundancy_settings: RedundancySettings = strawberry.field(name="RedundancySettings")
    transaction_fee: str = strawberry.field(name="TransactionFee")


@strawberry.type
class UploadParameters:
    current_height: int = strawberry.field(name="CurrentHeight")
    contract_set: str = strawberry.field(name="ContractSet")
    consensus_state: ConsensusState = strawberry.field(name="ConsensusState")
    gouging_settings: GougingSettings = strawberry.field(name="GougingSettings")
    redundancy_settings: RedundancySettings = strawberry.field(name="RedundancySettings")
    transaction_fee: str = strawberry.field(name="TransactionFee")


@strawberry.type
class BusState:
    start_time: str = strawberry.field(name="startTime")
    network: str
    version: str
    commit: str
    os: str = strawberry.field(name="OS")
    build_time: str = strawberry.field(name="buildTime")


@strawberry.type
class ObjectStats:
    num_objects: int = strawberry.field(name="numObjects")
    num_unfinished_objects: int = strawberry.field(name="numUnfinishedObjects")
    min_health: float = strawberry.field(name="minHealth")
    total_objects_size: int = strawberry.field(name="totalObjectsSize")
    total_unfinished_objects_size: int = strawberry.field(name="totalUnfinishedObjectsSize")
    total_sectors_size: int = strawberry.field(name="totalSectorsSize")
    total_uploaded_size: int = strawberry.field(name="totalUploadedSize")


@strawberry.input
class PinningValue:
    pinned: bool
    value: float


@strawberry.input
class AutopilotPinning:
    allowance: PinningValue


@strawberry.input
class PricePinningSettings:
    enabled: bool
    currency: str
    forex_endpoint_url: str = strawberry.field(name="forexEndpointURL")
    threshold: float
    autopilots: Dict[str, AutopilotPinning]
    gouging_settings_pins: GougingSettingsPins = strawberry.field(name="gougingSettingsPins")


@strawberry.input
class S3AuthenticationSettings:
    v4_keypairs: Dict[str, str] = strawberry.field(name="v4Keypairs")


# types.py - Part 3 - Stats Type


@strawberry.type
class SlabStats:
    total_slabs: int
    total_data: int
    total_healthy_slabs: int
    total_healthy_data: int
    min_health: float


@strawberry.type
class ContractStats:
    total_contracts: int
    total_active_contracts: int
    total_size: int
    total_spending: Dict[str, str]
    contract_set_stats: Dict[str, Dict[str, Any]]


# types.py - Part 4 - Slab and Object Types


@strawberry.type
class Shard:
    contracts: Dict[str, List[str]]
    latest_host: str = strawberry.field(name="latestHost")
    root: str


@strawberry.type
class SlabMigration:
    key: str
    health: float
    objects: List[str]
    slabs: List[SlabSlice]


@strawberry.type
class PartialSlab:
    key: str
    offset: int
    length: int


@strawberry.type
class AddPartialSlabResult:
    slabs: List[PartialSlab]
    slab_buffer_max_size_soft_reached: bool = strawberry.field(name="slabBufferMaxSizeSoftReached")


@strawberry.input
class ObjectInput:
    key: str
    slabs: List[SlabSlice]
    mime_type: str = strawberry.field(name="mimeType")
    e_tag: str = strawberry.field(name="eTag")


@strawberry.input
class CopyObjectInput:
    source_bucket: str = strawberry.field(name="sourceBucket")
    source_path: str = strawberry.field(name="sourcePath")
    destination_bucket: str = strawberry.field(name="destinationBucket")
    destination_path: str = strawberry.field(name="destinationPath")


@strawberry.input
class RenameObjectInput:
    bucket: str
    from_path: str = strawberry.field(name="from")
    to_path: str = strawberry.field(name="to")
    mode: str


@strawberry.input
class SlabMigrationInput:
    contract_set: str = strawberry.field(name="contractSet")
    health_cutoff: float = strawberry.field(name="healthCutoff")
    limit: int


# types.py - Multipart Types


# types.py - Wallet and Transaction Types


@strawberry.type
class WalletInfo:
    scan_height: int = strawberry.field(name="scanHeight")
    address: str
    spendable: str
    confirmed: str
    unconfirmed: str


@strawberry.type
class ScOutput:
    value: str = strawberry.field(name="Value")
    address: str = strawberry.field(name="Address")
    id: str = strawberry.field(name="ID")
    maturity_height: int = strawberry.field(name="MaturityHeight")


@strawberry.type
class WebhookQueue:
    url: str
    size: int


@strawberry.type
class WebhookInfo:
    webhooks: List[Webhook]
    queues: List[WebhookQueue]


@strawberry.input
class WebhookActionInput:
    module: str
    event: str
    payload: Any


@strawberry.type
class TxPoolTransaction:
    siacoin_inputs: List[Dict[str, Any]] = strawberry.field(name="SiacoinInputs")
    siacoin_outputs: List[Dict[str, Any]] = strawberry.field(name="SiacoinOutputs")
    file_contracts: List[Dict[str, Any]] = strawberry.field(name="FileContracts")
    file_contract_revisions: List[Dict[str, Any]] = strawberry.field(name="FileContractRevisions")
    storage_proofs: List[Dict[str, Any]] = strawberry.field(name="StorageProofs")
    siafund_inputs: List[Dict[str, Any]] = strawberry.field(name="SiafundInputs")
    siafund_outputs: List[Dict[str, Any]] = strawberry.field(name="SiafundOutputs")
    miner_fees: List[str] = strawberry.field(name="MinerFees")
    arbitrary_data: List[str] = strawberry.field(name="ArbitraryData")
    signatures: List[Dict[str, Any]] = strawberry.field(name="Signatures")


@strawberry.type
class WalletRedistributeResult:
    transaction_ids: List[str]


@strawberry.input
class RedistributeInput:
    amount: str
    outputs: int


@strawberry.input
class TransactionSignInput:
    transaction: Dict[str, Any]
    to_sign: List[str]
    covered_fields: Dict[str, Any]


@strawberry.input
class ContractPrepareInput:
    end_height: int = strawberry.field(name="endHeight")
    host_collateral: str = strawberry.field(name="hostCollateral")
    host_key: str = strawberry.field(name="hostKey")
    host_settings: Dict[str, Any] = strawberry.field(name="hostSettings")
    renter_address: str = strawberry.field(name="renterAddress")
    renter_funds: str = strawberry.field(name="renterFunds")
    renter_key: str = strawberry.field(name="renterKey")


@strawberry.input
class ContractRenewInput:
    contract: Dict[str, Any]
    end_height: int = strawberry.field(name="endHeight")
    host_settings: Dict[str, Any] = strawberry.field(name="hostSettings")
    new_collateral: str = strawberry.field(name="newCollateral")
    renter_address: str = strawberry.field(name="renterAddress")
    renter_funds: str = strawberry.field(name="renterFunds")
    renter_key: str = strawberry.field(name="renterKey")


@strawberry.input
class TransactionFundInput:
    transaction: Dict[str, Any]
    amount: str


@strawberry.type
class PreparedTransaction:
    transaction_set: List[Dict[str, Any]] = strawberry.field(name="transactionSet")
    final_payment: Optional[str] = strawberry.field(name="finalPayment")


@strawberry.type
class MultipartListPartsResponse:
    has_more: bool = strawberry.field(name="hasMore")
    next_marker: int = strawberry.field(name="nextMarker")
    parts: List[MultipartPart]


@strawberry.type
class MultipartCompleteResponse:
    etag: str = strawberry.field(name="eTag")


@strawberry.type
class MultipartCreateResponse:
    upload_id: str = strawberry.field(name="uploadID")


@strawberry.input
class MultipartAbortInput:
    bucket: str
    path: str
    upload_id: str = strawberry.field(name="uploadID")


@strawberry.input
class MultipartListPartsInput:
    bucket: str
    path: str
    upload_id: str = strawberry.field(name="uploadID")
    part_number_marker: int = strawberry.field(name="partNumberMarker", default=0)
    limit: int = -1


@strawberry.input
class MultipartListUploadsInput:
    bucket: str
    prefix: str = ""
    path_marker: str = strawberry.field(name="pathMarker", default="")
    upload_id_marker: str = strawberry.field(name="uploadIDMarker", default="")
    limit: int = -1


@strawberry.input
class UploadSectorInput:
    contract_id: str = strawberry.field(name="contractID")
    root: str


# types.py - Object Types


@strawberry.type
class ObjectShard:
    contracts: Dict[str, List[str]]
    latest_host: str = strawberry.field(name="latestHost")
    root: str


@strawberry.type
class ObjectSlab:
    health: float
    key: str
    min_shards: int = strawberry.field(name="minShards")
    shards: List[ObjectShard]


@strawberry.type
class ObjectSlabSlice:
    slab: ObjectSlab
    offset: int
    length: int


@strawberry.type
class ObjectInfo:
    etag: str = strawberry.field(name="eTag")
    health: float
    mime_type: str = strawberry.field(name="mimeType")
    mod_time: str = strawberry.field(name="modTime")
    name: str
    size: int
    key: str
    slabs: List[ObjectSlabSlice]


@strawberry.type
class ObjectListResponse:
    has_more: bool = strawberry.field(name="hasMore")
    object: Optional[ObjectInfo] = None
    objects: Optional[List[ObjectInfo]] = None


@strawberry.input
class ObjectListInput:
    bucket: str = strawberry.field(name="bucket")
    prefix: Optional[str] = strawberry.field(name="prefix")
    marker: Optional[str] = strawberry.field(name="marker")
    offset: Optional[int] = strawberry.field(name="offset")
    limit: Optional[int] = strawberry.field(name="limit")


@strawberry.input
class ObjectStoreInput:
    bucket: str
    contract_set: str = strawberry.field(name="contractSet")
    object: Dict[str, Any]
    mime_type: str = strawberry.field(name="mimeType")
    etag: str = strawberry.field(name="eTag")


@strawberry.input
class ObjectCopyInput:
    source_bucket: str = strawberry.field(name="sourceBucket")
    source_path: str = strawberry.field(name="sourcePath")
    destination_bucket: str = strawberry.field(name="destinationBucket")
    destination_path: str = strawberry.field(name="destinationPath")


# types.py - Part 1 - Base Types


@strawberry.type
class WorkerState:
    configured: bool
    migrating: bool
    migrating_last_start: str = strawberry.field(name="migratingLastStart")
    scanning: bool
    scanning_last_start: str = strawberry.field(name="scanningLastStart")
    uptime_ms: int = strawberry.field(name="uptimeMS")
    start_time: str = strawberry.field(name="startTime")
    network: str
    version: str
    commit: str
    os: str = strawberry.field(name="OS")
    build_time: str = strawberry.field(name="buildTime")


@strawberry.type
class MemoryStats:
    available: int
    total: int


@strawberry.type
class WorkerMemory:
    upload: MemoryStats


@strawberry.type
class MultipartPart:
    part_number: int = strawberry.field(name="partNumber")
    last_modified: str = strawberry.field(name="lastModified")
    etag: str = strawberry.field(name="eTag")
    size: int


@strawberry.type
class MultipartPartsResponse:
    has_more: bool = strawberry.field(name="hasMore")
    next_marker: int = strawberry.field(name="nextMarker")
    parts: List[MultipartPart]


@strawberry.input
class MultipartCreateInput:
    bucket: str
    key: Optional[str] = None
    path: str
    generate_key: bool = strawberry.field(name="generateKey", default=False)


@strawberry.input
class MultipartPartInput:
    part_number: int = strawberry.field(name="partNumber")
    etag: str = strawberry.field(name="eTag")


@strawberry.input
class MultipartCompleteInput:
    bucket: str
    path: str
    upload_id: str = strawberry.field(name="uploadID")
    parts: List[MultipartPartInput]


@strawberry.input
class ObjectRenameInput:
    bucket: Optional[str] = None
    from_path: str = strawberry.field(name="from")
    to_path: str = strawberry.field(name="to")
    mode: str


@strawberry.type
class ContractRevisionUnlockConditions:
    timelock: int = strawberry.field(name="Timelock")
    public_keys: List["PublicKey"] = strawberry.field(name="PublicKeys")
    signatures_required: int = strawberry.field(name="SignaturesRequired")


@strawberry.type
class ContractOutput:
    value: str = strawberry.field(name="Value")
    address: str = strawberry.field(name="Address")


@strawberry.type
class ContractRevision(SiaType):
    """A ContractRevision pairs a file contract with its signatures."""
    revision: FileContractRevision = strawberry.field(description="The file contract revision")
    signatures: List[TransactionSignature] = strawberry.field(description="The signatures for the revision", max_length=2)



@strawberry.type
class ContractPruneResponse(SiaType):
    size: Optional[int] = strawberry.field(
        description="""Size of the contract. | Format: uint64""", default=None
    )
    pruned: Optional[int] = strawberry.field(
        description="""Amount of data pruned from the contract. | Format: uint64""", default=None
    ) 
    remaining: Optional[int] = strawberry.field(
        description="""Amount of data remaining in the contract. | Format: uint64""", default=None
    )
    error: Optional[str] = strawberry.field(default=None)
    


@strawberry.input
class HostScanRequest(SiaInput):
    timeout: datetime.datetime = strawberry.field(description="""The timeout duration in milliseconds""") # DurationMS

@strawberry.type
class HostScanResponse(SiaType):
    ping: str = strawberry.field(description="Duration in milliseconds", name="ping")
    scan_error: Optional[str] = strawberry.field(default=None, name="scanError") 
    settings: Optional[HostSettings] = strawberry.field(default=None) # rhpv2.HostSettings
    price_table: Optional[HostPriceTable] = strawberry.field(default=None, name="priceTable")
    v2_settings: Optional[HostV2Settings] = strawberry.field(default=None, name="v2Settings") # rhp4.HostSettings


@strawberry.type
class RHPFormResponse(SiaType):
    contract_id: FileContractID = strawberry.field(name="contractID")
    contract: ContractRevision = strawberry.field(name="contract")
    transaction_set: List[Transaction] = strawberry.field(name="transactionSet")


@strawberry.input
class RHPFundRequest(SiaType):
    contract_id: FileContractID = strawberry.field(name="contractID")
    host_key: PublicKey = strawberry.field(name="hostKey")
    siamux_addr: str = strawberry.field(name="siamuxAddr")
    balance: str = strawberry.field(name="balance")


@strawberry.input
class RHPSyncRequest(SiaType):
    contract_id: FileContractID = strawberry.field(name="contractID")
    host_key: PublicKey = strawberry.field(name="hostKey")
    siamux_addr: str = strawberry.field(name="siamuxAddr")


# ----------------------------------------------------------------------------


# from datetime import datetime, timedelta
# import typing
# from int import int
# import strawberry
# from enum import Enum
# import dataclasses

# # Constants
# BLOCKS_PER_DAY = 144

# S3_MIN_ACCESS_KEY_LEN = 16
# S3_MAX_ACCESS_KEY_LEN = 128
# S3_SECRET_KEY_LEN = 40


# Contract States
@strawberry.enum
class ContractState(str, Enum):
    INVALID = "invalid"
    UNKNOWN = "unknown"
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETE = "complete"
    FAILED = "failed"


# Contract Usability
@strawberry.enum
class ContractUsability(str, Enum):
    BAD = "bad"
    GOOD = "good"


# Contract Archival Reasons
@strawberry.enum
class ContractArchivalReason(str, Enum):
    HOST_PRUNED = "hostpruned"
    REMOVED = "removed"
    RENEWED = "renewed"


# Filter Modes
@strawberry.enum
class ContractFilterMode(str, Enum):
    ALL = "all"
    ACTIVE = "active"
    ARCHIVED = "archived"
    GOOD = "good"


@strawberry.enum
class HostFilterMode(str, Enum):
    ALL = "all"
    ALLOWED = "allowed"
    BLOCKED = "blocked"


@strawberry.enum
class UsabilityFilterMode(str, Enum):
    ALL = "all"
    USABLE = "usable"
    UNUSABLE = "unusable"


@strawberry.type
class AccountsAddBalanceRequest(SiaType):
    host_key: PublicKey = strawberry.field(name="hostKey")
    amount: int = strawberry.field(name="amount")


@strawberry.type
class AccountHandlerPOST(SiaType):
    host_key: PublicKey = strawberry.field(name="hostKey")


@strawberry.type
class AccountsRequiresSyncRequest(SiaType):
    host_key: PublicKey = strawberry.field(name="hostKey")


@strawberry.type
class AccountsUpdateBalanceRequest(SiaType):
    host_key: PublicKey = strawberry.field(name="hostKey")
    amount: int = strawberry.field(name="amount")


@strawberry.type
class AutopilotTriggerRequest(SiaType):
    force_scan: bool = strawberry.field(name="forceScan")


@strawberry.type
class AutopilotTriggerResponse(SiaType):
    triggered: bool = strawberry.field(name="triggered")


@strawberry.type
class AutopilotStateResponse(BuildState):
    enabled: bool = strawberry.field(name="enabled")
    migrating: bool = strawberry.field(name="migrating")
    migrating_last_start: datetime.datetime = strawberry.field(name="migratingLastStart")
    pruning: bool = strawberry.field(name="pruning")
    pruning_last_start: datetime.datetime = strawberry.field(name="pruningLastStart")
    scanning: bool = strawberry.field(name="scanning")
    scanning_last_start: datetime.datetime = strawberry.field(name="scanningLastStart")
    uptime_ms: int = strawberry.field(name="uptimeMs") # TimeRFC3339
    start_time: datetime.datetime = strawberry.field(name="startTime") # DurationMS


@strawberry.type
class BucketPolicy(SiaType):
    public_read_access: bool = strawberry.field(name="publicReadAccess")


@strawberry.type
class CreateBucketOptions(SiaType):
    policy: BucketPolicy = strawberry.field(name="policy")


@strawberry.type
class BucketCreateRequest(SiaType):
    name: str = strawberry.field(name="name")
    policy: BucketPolicy = strawberry.field(name="policy")


@strawberry.type
class BucketUpdatePolicyRequest(SiaType):
    policy: BucketPolicy = strawberry.field(name="policy")


# Upload Types
@strawberry.type
class UploadParams(GougingParams):
    current_height: int = strawberry.field(name="currentHeight")
    upload_packing: bool = strawberry.field(name="uploadPacking")

@strawberry.type
class ContractPrunableData(ContractSize):
    id: FileContractID = strawberry.field(name="ID")

@strawberry.type
class ContractsPrunableDataResponse(SiaType):
    contracts: typing.List[ContractPrunableData] = strawberry.field(name="contracts")
    total_prunable: int = strawberry.field(name="totalPrunable")
    total_size: int = strawberry.field(name="totalSize")


@strawberry.type
class UnhealthySlab(SiaType):
    encryption_key: EncryptionKey = strawberry.field(name="encryptionKey")
    health: float = strawberry.field(name="health")


@strawberry.type
class SlabsForMigrationResponse(SiaType):
    slabs: typing.List[UnhealthySlab] = strawberry.field(name="slabs")


@strawberry.type
class DownloaderStats(SiaType):
    avg_sector_download_speed_mbps: float = strawberry.field(name="avgSectorDownloadSpeedMbps")
    host_key: PublicKey = strawberry.field(name="hostKey")


@strawberry.type
class DownloadStatsResponse(SiaType):
    avg_download_speed_mbps: float = strawberry.field(name="avgDownloadSpeedMbps")
    avg_overdrive_pct: float = strawberry.field(name="avgOverdrivePct")
    healthy_downloaders: int = strawberry.field(name="healthyDownloaders")
    num_downloaders: int = strawberry.field(name="numDownloaders")
    downloaders_stats: typing.List[DownloaderStats] = strawberry.field(name="downloadersStats")



@strawberry.type
class UploaderStats(SiaType):
    host_key: PublicKey = strawberry.field(name="hostKey")
    avg_sector_upload_speed_mbps: float = strawberry.field(name="avgSectorUploadSpeedMbps")



@strawberry.type
class UploadStatsResponse(SiaType):
    avg_slab_upload_speed_mbps: float = strawberry.field(name="avgSlabUploadSpeedMbps")
    avg_overdrive_pct: float = strawberry.field(name="avgOverdrivePct")
    healthy_uploaders: int = strawberry.field(name="healthyUploaders")
    num_uploaders: int = strawberry.field(name="numUploaders")
    uploaders_stats: typing.List[UploaderStats] = strawberry.field(name="uploadersStats")


# ****************************************
# BELOW TYPES ARE GENERATED AUTOMATICALLY
# ****************************************


@strawberry.type
class Account(SiaType):
    id: Optional[str] = strawberry.field(default=None)
    clean_shutdown: Optional[bool] = strawberry.field(
        description="""Whether the account has been cleanly shutdown. If not, the account will require a sync with the host.""",
        default=None,
        name="cleanShutdown",
    )
    host_key: Optional[str] = strawberry.field(default=None, name="hostKey")
    balance: Optional[str] = strawberry.field(default=None)
    drift: Optional[str] = strawberry.field(default=None)
    owner: Optional[str] = strawberry.field(
        description="""The owner of the account that manages it. This is the id of the worker that maintains the account. | Min length: 1""",
        default=None,
    )
    requires_sync: Optional[bool] = strawberry.field(
        description="""Whether the account requires a sync with the host. This is usually the case when the host reports insufficient balance for an account that the worker still believes to be funded.""",
        default=None,
        name="requiresSync",
    )


@strawberry.input
class AccountInput(SiaInput):
    id: Optional[str] = strawberry.field(default=None)
    clean_shutdown: Optional[bool] = strawberry.field(
        description="""Whether the account has been cleanly shutdown. If not, the account will require a sync with the host.""",
        default=None,
        name="cleanShutdown",
    )
    host_key: Optional[str] = strawberry.field(default=None, name="hostKey")
    balance: Optional[str] = strawberry.field(default=None)
    drift: Optional[str] = strawberry.field(default=None)
    owner: Optional[str] = strawberry.field(
        description="""The owner of the account that manages it. This is the id of the worker that maintains the account. | Min length: 1""",
        default=None,
    )
    requires_sync: Optional[bool] = strawberry.field(
        description="""Whether the account requires a sync with the host. This is usually the case when the host reports insufficient balance for an account that the worker still believes to be funded.""",
        default=None,
        name="requiresSync",
    )


@strawberry.type
class Alert(SiaType):
    id: Optional[str] = strawberry.field(default=None)
    severity: Optional[str] = strawberry.field(
        description="""The severity of the alert | Allowed values: info, warning, error, critical""", default=None
    )
    message: Optional[str] = strawberry.field(description="""The alert's message""", default=None)
    date: Optional[JSON] = strawberry.field(
        description="""Arbitrary data providing additional context for the alert""", default=None
    )
    timestamp: Optional[datetime.datetime] = strawberry.field(
        description="""The time the alert was created | Format: date-time""", default=None
    )


@strawberry.input
class AlertInput(SiaInput):
    id: Optional[str] = strawberry.field(default=None)
    severity: Optional[str] = strawberry.field(
        description="""The severity of the alert | Allowed values: info, warning, error, critical""", default=None
    )
    message: Optional[str] = strawberry.field(description="""The alert's message""", default=None)
    date: Optional[JSON] = strawberry.field(
        description="""Arbitrary data providing additional context for the alert""", default=None
    )
    timestamp: Optional[datetime.datetime] = strawberry.field(
        description="""The time the alert was created | Format: date-time""", default=None
    )


@strawberry.type
class Attestation(SiaType):
    public_key: Optional[PublicKey] = strawberry.field(default=None, name="publicKey")
    key: Optional[str] = strawberry.field(default=None)
    value: Optional[str] = strawberry.field(description="""Format: byte""", default=None)
    signature: Optional[Signature] = strawberry.field(default=None)


@strawberry.input
class AttestationInput(SiaInput):
    public_key: Optional[PublicKey] = strawberry.field(default=None, name="publicKey")
    key: Optional[str] = strawberry.field(default=None)
    value: Optional[str] = strawberry.field(description="""Format: byte""", default=None)
    signature: Optional[Signature] = strawberry.field(default=None)


@strawberry.type
class Block(SiaType):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    nonce: Optional[int] = strawberry.field(
        description="""The nonce used to mine the block | Format: uint64""", default=None
    )
    timestamp: Optional[datetime.datetime] = strawberry.field(
        description="""The time the block was mined | Format: date-time""", default=None
    )
    miner_payouts: Optional[List[SiacoinOutput]] = strawberry.field(default=None, name="minerPayouts")
    transactions: Optional[List[Transaction]] = strawberry.field(default=None)
    v2: Optional[V2BlockData] = strawberry.field(default=None)


@strawberry.input
class BlockInput(SiaInput):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    nonce: Optional[int] = strawberry.field(
        description="""The nonce used to mine the block | Format: uint64""", default=None
    )
    timestamp: Optional[datetime.datetime] = strawberry.field(
        description="""The time the block was mined | Format: date-time""", default=None
    )
    miner_payouts: Optional[List[SiacoinOutput]] = strawberry.field(default=None, name="minerPayouts")
    transactions: Optional[List[Transaction]] = strawberry.field(default=None)
    v2: Optional[V2BlockData] = strawberry.field(default=None)


@strawberry.type
class ChainIndex(SiaType):
    height: Optional[str] = strawberry.field(default=None)
    id: Optional[str] = strawberry.field(default=None)


@strawberry.input
class ChainIndexInput(SiaInput):
    height: Optional[str] = strawberry.field(default=None)
    id: Optional[str] = strawberry.field(default=None)


@strawberry.type
class ContractMetadata(SiaType):
    id: Optional[str] = strawberry.field(default=None)
    host_key: Optional[str] = strawberry.field(default=None, name="hostKey")
    v2: Optional[bool] = strawberry.field(description="""Indicates if the contract is a V2 contract.""", default=None)
    proof_height: Optional[str] = strawberry.field(default=None, name="proofHeight")
    renewed_from: Optional[str] = strawberry.field(default=None, name="renewedFrom")
    revision_height: Optional[str] = strawberry.field(default=None, name="revisionHeight")
    revision_number: Optional[str] = strawberry.field(default=None, name="revisionNumber")
    size: Optional[int] = strawberry.field(
        description="""The size of the contract in bytes | Format: uint64""", default=None
    )
    start_height: Optional[str] = strawberry.field(default=None, name="startHeight")
    state: Optional[str] = strawberry.field(
        description="""The state of the contract | Allowed values: pending, active, complete, failed""", default=None
    )
    usability: Optional[str] = strawberry.field(
        description="""The usability status of the contract | Allowed values: good, bad""", default=None
    )
    window_start: Optional[str] = strawberry.field(default=None, name="windowStart")
    window_end: Optional[str] = strawberry.field(default=None, name="windowEnd")
    contract_price: Optional[str] = strawberry.field(default=None, name="contractPrice")
    initial_renter_funds: Optional[str] = strawberry.field(default=None, name="initialRenterFunds")
    spending: Optional[str] = strawberry.field(default=None)
    archival_reason: Optional[str] = strawberry.field(
        description="""The reason for archiving the contract, if applicable. | Allowed values: renewed, removed, hostpruned""",
        default=None,
        name="archivalReason",
    )
    renewed_to: Optional[str] = strawberry.field(default=None, name="renewedTo")


@strawberry.input
class ContractMetadataInput(SiaInput):
    id: Optional[str] = strawberry.field(default=None)
    host_key: Optional[str] = strawberry.field(default=None, name="hostKey")
    v2: Optional[bool] = strawberry.field(description="""Indicates if the contract is a V2 contract.""", default=None)
    proof_height: Optional[str] = strawberry.field(default=None, name="proofHeight")
    renewed_from: Optional[str] = strawberry.field(default=None, name="renewedFrom")
    revision_height: Optional[str] = strawberry.field(default=None, name="revisionHeight")
    revision_number: Optional[str] = strawberry.field(default=None, name="revisionNumber")
    size: Optional[int] = strawberry.field(
        description="""The size of the contract in bytes | Format: uint64""", default=None
    )
    start_height: Optional[str] = strawberry.field(default=None, name="startHeight")
    state: Optional[str] = strawberry.field(
        description="""The state of the contract | Allowed values: pending, active, complete, failed""", default=None
    )
    usability: Optional[str] = strawberry.field(
        description="""The usability status of the contract | Allowed values: good, bad""", default=None
    )
    window_start: Optional[str] = strawberry.field(default=None, name="windowStart")
    window_end: Optional[str] = strawberry.field(default=None, name="windowEnd")
    contract_price: Optional[str] = strawberry.field(default=None, name="contractPrice")
    initial_renter_funds: Optional[str] = strawberry.field(default=None, name="initialRenterFunds")
    spending: Optional[str] = strawberry.field(default=None)
    archival_reason: Optional[str] = strawberry.field(
        description="""The reason for archiving the contract, if applicable. | Allowed values: renewed, removed, hostpruned""",
        default=None,
        name="archivalReason",
    )
    renewed_to: Optional[str] = strawberry.field(default=None, name="renewedTo")


@strawberry.type
class ContractSpending(SiaType):
    deletions: Optional[str] = strawberry.field(default=None)
    fund_account: Optional[str] = strawberry.field(default=None, name="fundAccount")
    sector_roots: Optional[str] = strawberry.field(default=None, name="sectorRoots")
    uploads: Optional[str] = strawberry.field(default=None)


@strawberry.input
class ContractSpendingInput(SiaInput):
    deletions: Optional[str] = strawberry.field(default=None)
    fund_account: Optional[str] = strawberry.field(default=None, name="fundAccount")
    sector_roots: Optional[str] = strawberry.field(default=None, name="sectorRoots")
    uploads: Optional[str] = strawberry.field(default=None)


@strawberry.type
class CoveredFields(SiaType):
    whole_transaction: Optional[bool] = strawberry.field(
        description="""Whether the whole transaction is covered by the signature""",
        default=None,
        name="wholeTransaction",
    )
    siacoin_inputs: Optional[List[int]] = strawberry.field(default=None, name="siacoinInputs")
    siacoin_outputs: Optional[List[int]] = strawberry.field(default=None, name="siacoinOutputs")
    file_contracts: Optional[List[int]] = strawberry.field(default=None, name="fileContracts")
    file_contract_revisions: Optional[List[int]] = strawberry.field(default=None, name="fileContractRevisions")
    storage_proofs: Optional[List[int]] = strawberry.field(default=None, name="storageProofs")
    siafund_inputs: Optional[List[int]] = strawberry.field(default=None, name="siafundInputs")
    siafund_outputs: Optional[List[int]] = strawberry.field(default=None, name="siafundOutputs")
    miner_fees: Optional[List[int]] = strawberry.field(default=None, name="minerFees")
    arbitrary_data: Optional[List[int]] = strawberry.field(default=None, name="arbitraryData")
    signatures: Optional[List[int]] = strawberry.field(default=None)


@strawberry.input
class CoveredFieldsInput(SiaInput):
    whole_transaction: Optional[bool] = strawberry.field(
        description="""Whether the whole transaction is covered by the signature""",
        default=None,
        name="wholeTransaction",
    )
    siacoin_inputs: Optional[List[int]] = strawberry.field(default=None, name="siacoinInputs")
    siacoin_outputs: Optional[List[int]] = strawberry.field(default=None, name="siacoinOutputs")
    file_contracts: Optional[List[int]] = strawberry.field(default=None, name="fileContracts")
    file_contract_revisions: Optional[List[int]] = strawberry.field(default=None, name="fileContractRevisions")
    storage_proofs: Optional[List[int]] = strawberry.field(default=None, name="storageProofs")
    siafund_inputs: Optional[List[int]] = strawberry.field(default=None, name="siafundInputs")
    siafund_outputs: Optional[List[int]] = strawberry.field(default=None, name="siafundOutputs")
    miner_fees: Optional[List[int]] = strawberry.field(default=None, name="minerFees")
    arbitrary_data: Optional[List[int]] = strawberry.field(default=None, name="arbitraryData")
    signatures: Optional[List[int]] = strawberry.field(default=None)


@strawberry.type(description="""A storage agreement between a renter and a host.""")
class FileContract(SiaType):
    filesize: Optional[int] = strawberry.field(
        description="""The size of the contract in bytes. | Format: uint64""", default=None
    )
    file_merkle_root: Optional[str] = strawberry.field(default=None, name="fileMerkleRoot")
    window_start: Optional[str] = strawberry.field(default=None, name="windowStart")
    window_end: Optional[str] = strawberry.field(default=None, name="windowEnd")
    payout: Optional[str] = strawberry.field(default=None)
    valid_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""List of outputs created if the contract is successfully fulfilled.""",
        default=None,
        name="validProofOutputs",
    )
    missed_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""List of outputs created if the contract is not fulfilled.""",
        default=None,
        name="missedProofOutputs",
    )
    unlock_hash: Optional[Address] = strawberry.field(default=None, name="unlockHash")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")


@strawberry.input(description="""A storage agreement between a renter and a host.""")
class FileContractInput(SiaInput):
    filesize: Optional[int] = strawberry.field(
        description="""The size of the contract in bytes. | Format: uint64""", default=None
    )
    file_merkle_root: Optional[str] = strawberry.field(default=None, name="fileMerkleRoot")
    window_start: Optional[str] = strawberry.field(default=None, name="windowStart")
    window_end: Optional[str] = strawberry.field(default=None, name="windowEnd")
    payout: Optional[str] = strawberry.field(default=None)
    valid_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""List of outputs created if the contract is successfully fulfilled.""",
        default=None,
        name="validProofOutputs",
    )
    missed_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""List of outputs created if the contract is not fulfilled.""",
        default=None,
        name="missedProofOutputs",
    )
    unlock_hash: Optional[Address] = strawberry.field(default=None, name="unlockHash")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")


@strawberry.type(description="""Represents a revision to an existing file contract.""")
class FileContractRevision(SiaType):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    unlock_conditions: Optional[str] = strawberry.field(default=None, name="unlockConditions")
    filesize: Optional[int] = strawberry.field(
        description="""The size of the file in bytes after the revision. | Format: uint64""", default=None
    )
    file_merkle_root: Optional[str] = strawberry.field(default=None, name="fileMerkleRoot")
    window_start: Optional[str] = strawberry.field(default=None, name="windowStart")
    window_end: Optional[str] = strawberry.field(default=None, name="windowEnd")
    valid_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""Updated outputs if the revised contract is successfully fulfilled.""",
        default=None,
        name="validProofOutputs",
    )
    missed_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""Updated outputs if the revised contract is not fulfilled.""",
        default=None,
        name="missedProofOutputs",
    )
    unlock_hash: Optional[str] = strawberry.field(default=None, name="unlockHash")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")


@strawberry.input(description="""Represents a revision to an existing file contract.""")
class FileContractRevisionInput(SiaInput):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    unlock_conditions: Optional[str] = strawberry.field(default=None, name="unlockConditions")
    filesize: Optional[int] = strawberry.field(
        description="""The size of the file in bytes after the revision. | Format: uint64""", default=None
    )
    file_merkle_root: Optional[str] = strawberry.field(default=None, name="fileMerkleRoot")
    window_start: Optional[str] = strawberry.field(default=None, name="windowStart")
    window_end: Optional[str] = strawberry.field(default=None, name="windowEnd")
    valid_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""Updated outputs if the revised contract is successfully fulfilled.""",
        default=None,
        name="validProofOutputs",
    )
    missed_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""Updated outputs if the revised contract is not fulfilled.""",
        default=None,
        name="missedProofOutputs",
    )
    unlock_hash: Optional[str] = strawberry.field(default=None, name="unlockHash")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")


@strawberry.type
class HostPrices(SiaType):
    contract_price: Optional[Currency] = strawberry.field(default=None, name="contractPrice")
    collateral: Optional[Currency] = strawberry.field(default=None)
    storage_price: Optional[Currency] = strawberry.field(default=None, name="storagePrice")
    ingress_price: Optional[Currency] = strawberry.field(default=None, name="ingressPrice")
    egress_price: Optional[Currency] = strawberry.field(default=None, name="egressPrice")
    tip_height: Optional[int] = strawberry.field(
        description="""The height at which the prices were last updated | Format: uint64""",
        default=None,
        name="tipHeight",
    )
    valid_until: Optional[datetime.datetime] = strawberry.field(
        description="""Format: date-time""", default=None, name="validUntil"
    )
    signature: Optional[Signature] = strawberry.field(default=None)


@strawberry.input
class HostPricesInput(SiaInput):
    contract_price: Optional[Currency] = strawberry.field(default=None, name="contractPrice")
    collateral: Optional[Currency] = strawberry.field(default=None)
    storage_price: Optional[Currency] = strawberry.field(default=None, name="storagePrice")
    ingress_price: Optional[Currency] = strawberry.field(default=None, name="ingressPrice")
    egress_price: Optional[Currency] = strawberry.field(default=None, name="egressPrice")
    tip_height: Optional[int] = strawberry.field(
        description="""The height at which the prices were last updated | Format: uint64""",
        default=None,
        name="tipHeight",
    )
    valid_until: Optional[datetime.datetime] = strawberry.field(
        description="""Format: date-time""", default=None, name="validUntil"
    )
    signature: Optional[Signature] = strawberry.field(default=None)


@strawberry.type(description="""A detailed price table containing cost and configuration values for a host.""")
class HostPriceTable(SiaType):
    uid: Optional[str] = strawberry.field(default=None)
    validity: Optional[int] = strawberry.field(
        description="""Duration (in nanoseconds) for which the host guarantees these prices are valid. | Format: int64 | Example: 3600000000000""",
        default=None,
    )
    hostblockheight: Optional[str] = strawberry.field(default=None)
    updatepricetablecost: Optional[str] = strawberry.field(default=None)
    accountbalancecost: Optional[str] = strawberry.field(default=None)
    fundaccountcost: Optional[str] = strawberry.field(default=None)
    latestrevisioncost: Optional[str] = strawberry.field(default=None)
    subscriptionmemorycost: Optional[str] = strawberry.field(default=None)
    subscriptionnotificationcost: Optional[str] = strawberry.field(default=None)
    initbasecost: Optional[str] = strawberry.field(default=None)
    memorytimecost: Optional[str] = strawberry.field(default=None)
    downloadbandwidthcost: Optional[str] = strawberry.field(default=None)
    uploadbandwidthcost: Optional[str] = strawberry.field(default=None)
    dropsectorsbasecost: Optional[str] = strawberry.field(default=None)
    dropsectorsunitcost: Optional[str] = strawberry.field(default=None)
    hassectorbasecost: Optional[str] = strawberry.field(default=None)
    readbasecost: Optional[str] = strawberry.field(default=None)
    readlengthcost: Optional[str] = strawberry.field(default=None)
    renewcontractcost: Optional[str] = strawberry.field(default=None)
    revisionbasecost: Optional[str] = strawberry.field(default=None)
    swapsectorcost: Optional[str] = strawberry.field(default=None)
    writebasecost: Optional[str] = strawberry.field(default=None)
    writelengthcost: Optional[str] = strawberry.field(default=None)
    writestorecost: Optional[str] = strawberry.field(default=None)
    txnfeeminrecommended: Optional[str] = strawberry.field(default=None)
    txnfeemaxrecommended: Optional[str] = strawberry.field(default=None)
    contractprice: Optional[str] = strawberry.field(default=None)
    collateralcost: Optional[str] = strawberry.field(default=None)
    maxcollateral: Optional[str] = strawberry.field(default=None)
    maxduration: Optional[int] = strawberry.field(
        description="""Maximum duration (in blocks) for which the host is willing to form a contract. | Format: uint64 | Example: 14400""",
        default=None,
    )
    windowsize: Optional[int] = strawberry.field(
        description="""Minimum time (in blocks) requested for the renew window of a contract. | Format: uint64 | Example: 1000""",
        default=None,
    )
    registryentriesleft: Optional[int] = strawberry.field(
        description="""The remaining number of registry entries available on the host. | Format: uint64 | Example: 5000""",
        default=None,
    )
    registryentriestotal: Optional[int] = strawberry.field(
        description="""The total number of registry entries available on the host. | Format: uint64 | Example: 10000""",
        default=None,
    )


@strawberry.input(description="""A detailed price table containing cost and configuration values for a host.""")
class HostPriceTableInput(SiaInput):
    uid: Optional[str] = strawberry.field(default=None)
    validity: Optional[int] = strawberry.field(
        description="""Duration (in nanoseconds) for which the host guarantees these prices are valid. | Format: int64 | Example: 3600000000000""",
        default=None,
    )
    hostblockheight: Optional[str] = strawberry.field(default=None)
    updatepricetablecost: Optional[str] = strawberry.field(default=None)
    accountbalancecost: Optional[str] = strawberry.field(default=None)
    fundaccountcost: Optional[str] = strawberry.field(default=None)
    latestrevisioncost: Optional[str] = strawberry.field(default=None)
    subscriptionmemorycost: Optional[str] = strawberry.field(default=None)
    subscriptionnotificationcost: Optional[str] = strawberry.field(default=None)
    initbasecost: Optional[str] = strawberry.field(default=None)
    memorytimecost: Optional[str] = strawberry.field(default=None)
    downloadbandwidthcost: Optional[str] = strawberry.field(default=None)
    uploadbandwidthcost: Optional[str] = strawberry.field(default=None)
    dropsectorsbasecost: Optional[str] = strawberry.field(default=None)
    dropsectorsunitcost: Optional[str] = strawberry.field(default=None)
    hassectorbasecost: Optional[str] = strawberry.field(default=None)
    readbasecost: Optional[str] = strawberry.field(default=None)
    readlengthcost: Optional[str] = strawberry.field(default=None)
    renewcontractcost: Optional[str] = strawberry.field(default=None)
    revisionbasecost: Optional[str] = strawberry.field(default=None)
    swapsectorcost: Optional[str] = strawberry.field(default=None)
    writebasecost: Optional[str] = strawberry.field(default=None)
    writelengthcost: Optional[str] = strawberry.field(default=None)
    writestorecost: Optional[str] = strawberry.field(default=None)
    txnfeeminrecommended: Optional[str] = strawberry.field(default=None)
    txnfeemaxrecommended: Optional[str] = strawberry.field(default=None)
    contractprice: Optional[str] = strawberry.field(default=None)
    collateralcost: Optional[str] = strawberry.field(default=None)
    maxcollateral: Optional[str] = strawberry.field(default=None)
    maxduration: Optional[int] = strawberry.field(
        description="""Maximum duration (in blocks) for which the host is willing to form a contract. | Format: uint64 | Example: 14400""",
        default=None,
    )
    windowsize: Optional[int] = strawberry.field(
        description="""Minimum time (in blocks) requested for the renew window of a contract. | Format: uint64 | Example: 1000""",
        default=None,
    )
    registryentriesleft: Optional[int] = strawberry.field(
        description="""The remaining number of registry entries available on the host. | Format: uint64 | Example: 5000""",
        default=None,
    )
    registryentriestotal: Optional[int] = strawberry.field(
        description="""The total number of registry entries available on the host. | Format: uint64 | Example: 10000""",
        default=None,
    )


@strawberry.type
class HostSettings(SiaType):
    accepting_contracts: Optional[bool] = strawberry.field(
        description="""Whether the host is accepting new contracts""", default=None, name="acceptingContracts"
    )
    max_download_batch_size: Optional[int] = strawberry.field(
        description="""Maximum allowed download batch size | Format: uint64""",
        default=None,
        name="maxDownloadBatchSize",
    )
    max_duration: Optional[int] = strawberry.field(
        description="""Maximum allowed contract duration | Format: uint64""", default=None, name="maxDuration"
    )
    max_revise_batch_size: Optional[int] = strawberry.field(
        description="""Maximum allowed revision batch size | Format: uint64""", default=None, name="maxReviseBatchSize"
    )
    net_address: Optional[str] = strawberry.field(
        description="""Network address of the host""", default=None, name="netAddress"
    )
    remaining_storage: Optional[int] = strawberry.field(
        description="""Amount of storage the host has remaining | Format: uint64""",
        default=None,
        name="remainingStorage",
    )
    sector_size: Optional[int] = strawberry.field(
        description="""Size of a storage sector | Format: uint64""", default=None, name="sectorSize"
    )
    total_storage: Optional[int] = strawberry.field(
        description="""Total amount of storage space | Format: uint64""", default=None, name="totalStorage"
    )
    address: Optional[Address] = strawberry.field(default=None)
    window_size: Optional[int] = strawberry.field(
        description="""Size of the proof window | Format: uint64""", default=None, name="windowSize"
    )
    collateral: Optional[Currency] = strawberry.field(default=None)
    max_collateral: Optional[Currency] = strawberry.field(default=None, name="maxCollateral")
    base_rpc_price: Optional[Currency] = strawberry.field(default=None, name="baseRPCPrice")
    contract_price: Optional[Currency] = strawberry.field(default=None, name="contractPrice")
    download_bandwidth_price: Optional[Currency] = strawberry.field(default=None, name="downloadBandwidthPrice")
    sector_access_price: Optional[Currency] = strawberry.field(default=None, name="sectorAccessPrice")
    storage_price: Optional[Currency] = strawberry.field(default=None, name="storagePrice")
    upload_bandwidth_price: Optional[Currency] = strawberry.field(default=None, name="uploadBandwidthPrice")
    ephemeral_account_expiry: Optional[int] = strawberry.field(
        description="""Duration before an ephemeral account expires | Format: int64""",
        default=None,
        name="ephemeralAccountExpiry",
    )
    max_ephemeral_account_balance: Optional[Currency] = strawberry.field(
        default=None, name="maxEphemeralAccountBalance"
    )
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")
    version: Optional[str] = strawberry.field(description="""Version of the host software""", default=None)
    release: Optional[str] = strawberry.field(
        description="""Release tag of the host software | Example: hostd 1.0.0""", default=None
    )
    siamux_port: Optional[str] = strawberry.field(
        description="""Port used for siamux connections""", default=None, name="siamuxPort"
    )


@strawberry.input
class HostSettingsInput(SiaInput):
    accepting_contracts: Optional[bool] = strawberry.field(
        description="""Whether the host is accepting new contracts""", default=None, name="acceptingContracts"
    )
    max_download_batch_size: Optional[int] = strawberry.field(
        description="""Maximum allowed download batch size | Format: uint64""",
        default=None,
        name="maxDownloadBatchSize",
    )
    max_duration: Optional[int] = strawberry.field(
        description="""Maximum allowed contract duration | Format: uint64""", default=None, name="maxDuration"
    )
    max_revise_batch_size: Optional[int] = strawberry.field(
        description="""Maximum allowed revision batch size | Format: uint64""", default=None, name="maxReviseBatchSize"
    )
    net_address: Optional[str] = strawberry.field(
        description="""Network address of the host""", default=None, name="netAddress"
    )
    remaining_storage: Optional[int] = strawberry.field(
        description="""Amount of storage the host has remaining | Format: uint64""",
        default=None,
        name="remainingStorage",
    )
    sector_size: Optional[int] = strawberry.field(
        description="""Size of a storage sector | Format: uint64""", default=None, name="sectorSize"
    )
    total_storage: Optional[int] = strawberry.field(
        description="""Total amount of storage space | Format: uint64""", default=None, name="totalStorage"
    )
    address: Optional[Address] = strawberry.field(default=None)
    window_size: Optional[int] = strawberry.field(
        description="""Size of the proof window | Format: uint64""", default=None, name="windowSize"
    )
    collateral: Optional[Currency] = strawberry.field(default=None)
    max_collateral: Optional[Currency] = strawberry.field(default=None, name="maxCollateral")
    base_rpc_price: Optional[Currency] = strawberry.field(default=None, name="baseRPCPrice")
    contract_price: Optional[Currency] = strawberry.field(default=None, name="contractPrice")
    download_bandwidth_price: Optional[Currency] = strawberry.field(default=None, name="downloadBandwidthPrice")
    sector_access_price: Optional[Currency] = strawberry.field(default=None, name="sectorAccessPrice")
    storage_price: Optional[Currency] = strawberry.field(default=None, name="storagePrice")
    upload_bandwidth_price: Optional[Currency] = strawberry.field(default=None, name="uploadBandwidthPrice")
    ephemeral_account_expiry: Optional[int] = strawberry.field(
        description="""Duration before an ephemeral account expires | Format: int64""",
        default=None,
        name="ephemeralAccountExpiry",
    )
    max_ephemeral_account_balance: Optional[Currency] = strawberry.field(
        default=None, name="maxEphemeralAccountBalance"
    )
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")
    version: Optional[str] = strawberry.field(description="""Version of the host software""", default=None)
    release: Optional[str] = strawberry.field(
        description="""Release tag of the host software | Example: hostd 1.0.0""", default=None
    )
    siamux_port: Optional[str] = strawberry.field(
        description="""Port used for siamux connections""", default=None, name="siamuxPort"
    )


@strawberry.type
class HostV2Settings(SiaType):
    protocol_version: Optional[SemVer] = strawberry.field(default=None, name="protocolVersion")
    release: Optional[str] = strawberry.field(
        description="""Release tag of the host software | Example: hostd 1.0.0""", default=None
    )
    wallet_address: Optional[Address] = strawberry.field(default=None, name="walletAddress")
    accepting_contracts: Optional[bool] = strawberry.field(
        description="""Whether the host is accepting new contracts""", default=None, name="acceptingContracts"
    )
    max_collateral: Optional[Currency] = strawberry.field(default=None, name="maxCollateral")
    max_contract_duration: Optional[int] = strawberry.field(
        description="""Maximum allowed contract duration | Format: uint64""", default=None, name="maxContractDuration"
    )
    remaining_storage: Optional[int] = strawberry.field(
        description="""Amount of storage the host has remaining | Format: uint64""",
        default=None,
        name="remainingStorage",
    )
    total_storage: Optional[int] = strawberry.field(
        description="""Total amount of storage space | Format: uint64""", default=None, name="totalStorage"
    )
    prices: Optional[HostPrices] = strawberry.field(default=None)


@strawberry.input
class HostV2SettingsInput(SiaInput):
    protocol_version: Optional[SemVer] = strawberry.field(default=None, name="protocolVersion")
    release: Optional[str] = strawberry.field(
        description="""Release tag of the host software | Example: hostd 1.0.0""", default=None
    )
    wallet_address: Optional[Address] = strawberry.field(default=None, name="walletAddress")
    accepting_contracts: Optional[bool] = strawberry.field(
        description="""Whether the host is accepting new contracts""", default=None, name="acceptingContracts"
    )
    max_collateral: Optional[Currency] = strawberry.field(default=None, name="maxCollateral")
    max_contract_duration: Optional[int] = strawberry.field(
        description="""Maximum allowed contract duration | Format: uint64""", default=None, name="maxContractDuration"
    )
    remaining_storage: Optional[int] = strawberry.field(
        description="""Amount of storage the host has remaining | Format: uint64""",
        default=None,
        name="remainingStorage",
    )
    total_storage: Optional[int] = strawberry.field(
        description="""Total amount of storage space | Format: uint64""", default=None, name="totalStorage"
    )
    prices: Optional[HostPrices] = strawberry.field(default=None)


@strawberry.type
class SatisfiedPolicy(SiaType):
    policy: Optional[JSON] = strawberry.field(default=None)
    signature: Optional[List[Signature]] = strawberry.field(default=None)
    preimages: Optional[List[str]] = strawberry.field(default=None)


@strawberry.input
class SatisfiedPolicyInput(SiaInput):
    policy: Optional[JSON] = strawberry.field(default=None)
    signature: Optional[List[Signature]] = strawberry.field(default=None)
    preimages: Optional[List[str]] = strawberry.field(default=None)


@strawberry.type
class SiacoinElement(SiaType):
    id: Optional[str] = strawberry.field(default=None)
    state_element: Optional[str] = strawberry.field(default=None, name="stateElement")
    siafund_output: Optional[str] = strawberry.field(default=None, name="siafundOutput")
    maturity_height: Optional[str] = strawberry.field(default=None, name="maturityHeight")


@strawberry.input
class SiacoinElementInput(SiaInput):
    id: Optional[str] = strawberry.field(default=None)
    state_element: Optional[str] = strawberry.field(default=None, name="stateElement")
    siafund_output: Optional[str] = strawberry.field(default=None, name="siafundOutput")
    maturity_height: Optional[str] = strawberry.field(default=None, name="maturityHeight")


@strawberry.type
class SiacoinInput(SiaType):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    unlock_conditions: Optional[str] = strawberry.field(default=None, name="unlockConditions")


@strawberry.input
class SiacoinInputInput(SiaInput):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    unlock_conditions: Optional[str] = strawberry.field(default=None, name="unlockConditions")


@strawberry.type
class SiacoinOutput(SiaType):
    value: Optional[str] = strawberry.field(default=None)
    address: Optional[Address] = strawberry.field(default=None)


@strawberry.input
class SiacoinOutputInput(SiaInput):
    value: Optional[str] = strawberry.field(default=None)
    address: Optional[Address] = strawberry.field(default=None)


@strawberry.type
class SiafundElement(SiaType):
    id: Optional[str] = strawberry.field(default=None)
    state_element: Optional[str] = strawberry.field(default=None, name="stateElement")
    siafund_output: Optional[str] = strawberry.field(default=None, name="siafundOutput")
    claim_start: Optional[str] = strawberry.field(default=None, name="claimStart")


@strawberry.input
class SiafundElementInput(SiaInput):
    id: Optional[str] = strawberry.field(default=None)
    state_element: Optional[str] = strawberry.field(default=None, name="stateElement")
    siafund_output: Optional[str] = strawberry.field(default=None, name="siafundOutput")
    claim_start: Optional[str] = strawberry.field(default=None, name="claimStart")


@strawberry.type(description="""Represents an input used to spend an unspent Siafund output.""")
class SiafundInput(SiaType):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    unlock_conditions: Optional[str] = strawberry.field(default=None, name="unlockConditions")
    claim_address: Optional[str] = strawberry.field(default=None, name="claimAddress")


@strawberry.input(description="""Represents an input used to spend an unspent Siafund output.""")
class SiafundInputInput(SiaInput):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    unlock_conditions: Optional[str] = strawberry.field(default=None, name="unlockConditions")
    claim_address: Optional[str] = strawberry.field(default=None, name="claimAddress")


@strawberry.type(description="""Represents an output created to distribute Siafund.""")
class SiafundOutput(SiaType):
    value: Optional[int] = strawberry.field(
        description="""The amount of Siafund in the output. | Format: uint64""", default=None
    )
    address: Optional[str] = strawberry.field(default=None)


@strawberry.input(description="""Represents an output created to distribute Siafund.""")
class SiafundOutputInput(SiaInput):
    value: Optional[int] = strawberry.field(
        description="""The amount of Siafund in the output. | Format: uint64""", default=None
    )
    address: Optional[str] = strawberry.field(default=None)


@strawberry.type
class StateElement(SiaType):
    leaf_index: Optional[int] = strawberry.field(
        description="""The index of the element in the Merkle tree | Format: uint64""", default=None, name="leafIndex"
    )
    merkle_proof: Optional[List[Hash256]] = strawberry.field(
        description="""The Merkle proof demonstrating the inclusion of the leaf""", default=None, name="merkleProof"
    )


@strawberry.input
class StateElementInput(SiaInput):
    leaf_index: Optional[int] = strawberry.field(
        description="""The index of the element in the Merkle tree | Format: uint64""", default=None, name="leafIndex"
    )
    merkle_proof: Optional[List[Hash256]] = strawberry.field(
        description="""The Merkle proof demonstrating the inclusion of the leaf""", default=None, name="merkleProof"
    )


@strawberry.type(description="""Represents a proof of storage for a file contract.""")
class StorageProof(SiaType):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    leaf: Optional[str] = strawberry.field(
        description="""The selected leaf from the Merkle tree of the file's data. | Format: byte""", default=None
    )
    proof: Optional[List[Hash256]] = strawberry.field(
        description="""The Merkle proof demonstrating the inclusion of the leaf.""", default=None
    )


@strawberry.input(description="""Represents a proof of storage for a file contract.""")
class StorageProofInput(SiaInput):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    leaf: Optional[str] = strawberry.field(
        description="""The selected leaf from the Merkle tree of the file's data. | Format: byte""", default=None
    )
    proof: Optional[List[Hash256]] = strawberry.field(
        description="""The Merkle proof demonstrating the inclusion of the leaf.""", default=None
    )


@strawberry.type
class Transaction(SiaType):
    siacoin_inputs: Optional[List[SiacoinInput]] = strawberry.field(
        description="""List of Siacoin inputs used in the transaction.""", default=None, name="siacoinInputs"
    )
    siacoin_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""List of Siacoin outputs created by the transaction.""", default=None, name="siacoinOutputs"
    )
    file_contracts: Optional[List[FileContract]] = strawberry.field(
        description="""List of file contracts created by the transaction.""", default=None, name="fileContracts"
    )
    file_contract_revisions: Optional[List[FileContractRevision]] = strawberry.field(
        description="""List of revisions to existing file contracts included in the transaction.""",
        default=None,
        name="fileContractRevisions",
    )
    storage_proofs: Optional[List[StorageProof]] = strawberry.field(
        description="""List of storage proofs asserting the storage of data for file contracts.""",
        default=None,
        name="storageProofs",
    )
    siafund_inputs: Optional[List[SiafundInput]] = strawberry.field(
        description="""List of Siafund inputs spent in the transaction.""", default=None, name="siafundInputs"
    )
    siafund_outputs: Optional[List[SiafundOutput]] = strawberry.field(
        description="""List of Siafund outputs created by the transaction.""", default=None, name="siafundOutputs"
    )
    miner_fees: Optional[List[Currency]] = strawberry.field(
        description="""List of miner fees included in the transaction.""", default=None, name="minerFees"
    )
    arbitrary_data: Optional[List[str]] = strawberry.field(
        description="""Arbitrary binary data included in the transaction.""", default=None, name="arbitraryData"
    )
    signatures: Optional[List[TransactionSignature]] = strawberry.field(
        description="""List of cryptographic signatures verifying the transaction.""", default=None
    )


@strawberry.input
class TransactionInput(SiaInput):
    siacoin_inputs: Optional[List[SiacoinInput]] = strawberry.field(
        description="""List of Siacoin inputs used in the transaction.""", default=None, name="siacoinInputs"
    )
    siacoin_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="""List of Siacoin outputs created by the transaction.""", default=None, name="siacoinOutputs"
    )
    file_contracts: Optional[List[FileContract]] = strawberry.field(
        description="""List of file contracts created by the transaction.""", default=None, name="fileContracts"
    )
    file_contract_revisions: Optional[List[FileContractRevision]] = strawberry.field(
        description="""List of revisions to existing file contracts included in the transaction.""",
        default=None,
        name="fileContractRevisions",
    )
    storage_proofs: Optional[List[StorageProof]] = strawberry.field(
        description="""List of storage proofs asserting the storage of data for file contracts.""",
        default=None,
        name="storageProofs",
    )
    siafund_inputs: Optional[List[SiafundInput]] = strawberry.field(
        description="""List of Siafund inputs spent in the transaction.""", default=None, name="siafundInputs"
    )
    siafund_outputs: Optional[List[SiafundOutput]] = strawberry.field(
        description="""List of Siafund outputs created by the transaction.""", default=None, name="siafundOutputs"
    )
    miner_fees: Optional[List[Currency]] = strawberry.field(
        description="""List of miner fees included in the transaction.""", default=None, name="minerFees"
    )
    arbitrary_data: Optional[List[str]] = strawberry.field(
        description="""Arbitrary binary data included in the transaction.""", default=None, name="arbitraryData"
    )
    signatures: Optional[List[TransactionSignature]] = strawberry.field(
        description="""List of cryptographic signatures verifying the transaction.""", default=None
    )


@strawberry.type
class TransactionSignature(SiaType):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    public_key_index: Optional[int] = strawberry.field(
        description="""The index of the public key used to sign the transaction | Format: uint64""",
        default=None,
        name="publicKeyIndex",
    )
    timelock: Optional[str] = strawberry.field(default=None)
    covered_fields: Optional[str] = strawberry.field(default=None, name="coveredFields")
    signature: Optional[str] = strawberry.field(default=None)


@strawberry.input
class TransactionSignatureInput(SiaInput):
    parent_id: Optional[str] = strawberry.field(default=None, name="parentID")
    public_key_index: Optional[int] = strawberry.field(
        description="""The index of the public key used to sign the transaction | Format: uint64""",
        default=None,
        name="publicKeyIndex",
    )
    timelock: Optional[str] = strawberry.field(default=None)
    covered_fields: Optional[str] = strawberry.field(default=None, name="coveredFields")
    signature: Optional[str] = strawberry.field(default=None)


@strawberry.type
class UnlockConditions(SiaType):
    timelock: Optional[str] = strawberry.field(default=None)
    public_keys: Optional[List[UnlockKey]] = strawberry.field(default=None, name="publicKeys")
    signatures_required: Optional[int] = strawberry.field(
        description="""The number of signatures required to spend the output | Format: uint64""",
        default=None,
        name="signaturesRequired",
    )


@strawberry.input
class UnlockConditionsInput(SiaInput):
    timelock: Optional[str] = strawberry.field(default=None)
    public_keys: Optional[List[UnlockKey]] = strawberry.field(default=None, name="publicKeys")
    signatures_required: Optional[int] = strawberry.field(
        description="""The number of signatures required to spend the output | Format: uint64""",
        default=None,
        name="signaturesRequired",
    )


@strawberry.type
class UnlockKey(SiaType):
    algorithm: Optional[str] = strawberry.field(
        description="""A fixed 16-byte array that specifies the algorithm used to generate
the key
 | Format: bytes | Example: ed25519""",
        default=None,
    )
    key: Optional[str] = strawberry.field(
        description="""A 32-byte key represented as a hex-encoded string. Must be exactly
64 characters long, containing only hexadecimal digits
 | Pattern: ^[a-fA-F0-9]{64}$ | Format: bytes""",
        default=None,
    )


@strawberry.input
class UnlockKeyInput(SiaInput):
    algorithm: Optional[str] = strawberry.field(
        description="""A fixed 16-byte array that specifies the algorithm used to generate
the key
 | Format: bytes | Example: ed25519""",
        default=None,
    )
    key: Optional[str] = strawberry.field(
        description="""A 32-byte key represented as a hex-encoded string. Must be exactly
64 characters long, containing only hexadecimal digits
 | Pattern: ^[a-fA-F0-9]{64}$ | Format: bytes""",
        default=None,
    )


@strawberry.type
class V2BlockData(SiaType):
    height: Optional[str] = strawberry.field(default=None)
    commitment: Optional[Hash256] = strawberry.field(default=None)
    transactions: Optional[List[V2Transaction]] = strawberry.field(default=None)


@strawberry.input
class V2BlockDataInput(SiaInput):
    height: Optional[str] = strawberry.field(default=None)
    commitment: Optional[Hash256] = strawberry.field(default=None)
    transactions: Optional[List[V2Transaction]] = strawberry.field(default=None)


@strawberry.type
class V2FileContract(SiaType):
    capacity: Optional[int] = strawberry.field(description="""Format: uint64""", default=None)
    filesize: Optional[int] = strawberry.field(description="""Format: uint64""", default=None)
    file_merkle_root: Optional[Hash256] = strawberry.field(default=None, name="fileMerkleRoot")
    proof_height: Optional[int] = strawberry.field(description="""Format: uint64""", default=None, name="proofHeight")
    expiration_height: Optional[int] = strawberry.field(
        description="""Format: uint64""", default=None, name="expirationHeight"
    )
    renter_output: Optional[SiacoinOutput] = strawberry.field(default=None, name="renterOutput")
    host_output: Optional[SiacoinOutput] = strawberry.field(default=None, name="hostOutput")
    missed_host_value: Optional[Currency] = strawberry.field(default=None, name="missedHostValue")
    total_collateral: Optional[Currency] = strawberry.field(default=None, name="totalCollateral")
    renter_public_key: Optional[PublicKey] = strawberry.field(default=None, name="renterPublicKey")
    host_public_key: Optional[PublicKey] = strawberry.field(default=None, name="hostPublicKey")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")
    renter_signature: Optional[Signature] = strawberry.field(default=None, name="renterSignature")
    host_signature: Optional[Signature] = strawberry.field(default=None, name="hostSignature")


@strawberry.input
class V2FileContractInput(SiaInput):
    capacity: Optional[int] = strawberry.field(description="""Format: uint64""", default=None)
    filesize: Optional[int] = strawberry.field(description="""Format: uint64""", default=None)
    file_merkle_root: Optional[Hash256] = strawberry.field(default=None, name="fileMerkleRoot")
    proof_height: Optional[int] = strawberry.field(description="""Format: uint64""", default=None, name="proofHeight")
    expiration_height: Optional[int] = strawberry.field(
        description="""Format: uint64""", default=None, name="expirationHeight"
    )
    renter_output: Optional[SiacoinOutput] = strawberry.field(default=None, name="renterOutput")
    host_output: Optional[SiacoinOutput] = strawberry.field(default=None, name="hostOutput")
    missed_host_value: Optional[Currency] = strawberry.field(default=None, name="missedHostValue")
    total_collateral: Optional[Currency] = strawberry.field(default=None, name="totalCollateral")
    renter_public_key: Optional[PublicKey] = strawberry.field(default=None, name="renterPublicKey")
    host_public_key: Optional[PublicKey] = strawberry.field(default=None, name="hostPublicKey")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")
    renter_signature: Optional[Signature] = strawberry.field(default=None, name="renterSignature")
    host_signature: Optional[Signature] = strawberry.field(default=None, name="hostSignature")


@strawberry.type
class V2FileContractElement(SiaType):
    id: Optional[str] = strawberry.field(default=None)
    state_element: Optional[str] = strawberry.field(default=None, name="stateElement")
    v2_file_contract: Optional[V2FileContract] = strawberry.field(default=None, name="v2FileContract")


@strawberry.input
class V2FileContractElementInput(SiaInput):
    id: Optional[str] = strawberry.field(default=None)
    state_element: Optional[str] = strawberry.field(default=None, name="stateElement")
    v2_file_contract: Optional[V2FileContract] = strawberry.field(default=None, name="v2FileContract")


@strawberry.type
class V2FileContractResolution(SiaType):
    parent: Optional[V2FileContractElement] = strawberry.field(default=None)
    resolution: Optional[JSON] = strawberry.field(default=None)


@strawberry.input
class V2FileContractResolutionInput(SiaInput):
    parent: Optional[V2FileContractElement] = strawberry.field(default=None)
    resolution: Optional[JSON] = strawberry.field(default=None)


@strawberry.type
class V2FileContractRevision(SiaType):
    parent: Optional[V2FileContractElement] = strawberry.field(default=None)
    revision: Optional[V2FileContract] = strawberry.field(default=None)


@strawberry.input
class V2FileContractRevisionInput(SiaInput):
    parent: Optional[V2FileContractElement] = strawberry.field(default=None)
    revision: Optional[V2FileContract] = strawberry.field(default=None)


@strawberry.type
class V2SiacoinInput(SiaType):
    parent: Optional[SiacoinElement] = strawberry.field(default=None)
    satisfied_policy: Optional[SatisfiedPolicy] = strawberry.field(default=None, name="satisfiedPolicy")


@strawberry.input
class V2SiacoinInputInput(SiaInput):
    parent: Optional[SiacoinElement] = strawberry.field(default=None)
    satisfied_policy: Optional[SatisfiedPolicy] = strawberry.field(default=None, name="satisfiedPolicy")


@strawberry.type
class V2SiafundInput(SiaType):
    parent: Optional[SiafundElement] = strawberry.field(default=None)
    claim_address: Optional[Address] = strawberry.field(default=None, name="claimAddress")
    satisfied_policy: Optional[SatisfiedPolicy] = strawberry.field(default=None, name="satisfiedPolicy")


@strawberry.input
class V2SiafundInputInput(SiaInput):
    parent: Optional[SiafundElement] = strawberry.field(default=None)
    claim_address: Optional[Address] = strawberry.field(default=None, name="claimAddress")
    satisfied_policy: Optional[SatisfiedPolicy] = strawberry.field(default=None, name="satisfiedPolicy")


@strawberry.type
class V2Transaction(SiaType):
    siacoin_inputs: Optional[List[V2SiacoinInput]] = strawberry.field(default=None, name="siacoinInputs")
    siacoin_outputs: Optional[List[SiacoinOutput]] = strawberry.field(default=None, name="siacoinOutputs")
    siafund_inputs: Optional[List[V2SiafundInput]] = strawberry.field(default=None, name="siafundInputs")
    siafund_outputs: Optional[List[SiafundOutput]] = strawberry.field(default=None, name="siafundOutputs")
    file_contracts: Optional[List[V2FileContract]] = strawberry.field(default=None, name="fileContracts")
    file_contract_revisions: Optional[List[V2FileContractRevision]] = strawberry.field(
        default=None, name="fileContractRevisions"
    )
    file_contract_resolutions: Optional[List[V2FileContractResolution]] = strawberry.field(
        default=None, name="fileContractResolutions"
    )
    attestations: Optional[List[Attestation]] = strawberry.field(default=None)
    arbitrary_data: Optional[List[str]] = strawberry.field(default=None, name="arbitraryData")
    new_foundation_address: Optional[Address] = strawberry.field(default=None, name="newFoundationAddress")
    miner_fee: Optional[Currency] = strawberry.field(default=None, name="minerFee")


@strawberry.input
class V2TransactionInput(SiaInput):
    siacoin_inputs: Optional[List[V2SiacoinInput]] = strawberry.field(default=None, name="siacoinInputs")
    siacoin_outputs: Optional[List[SiacoinOutput]] = strawberry.field(default=None, name="siacoinOutputs")
    siafund_inputs: Optional[List[V2SiafundInput]] = strawberry.field(default=None, name="siafundInputs")
    siafund_outputs: Optional[List[SiafundOutput]] = strawberry.field(default=None, name="siafundOutputs")
    file_contracts: Optional[List[V2FileContract]] = strawberry.field(default=None, name="fileContracts")
    file_contract_revisions: Optional[List[V2FileContractRevision]] = strawberry.field(
        default=None, name="fileContractRevisions"
    )
    file_contract_resolutions: Optional[List[V2FileContractResolution]] = strawberry.field(
        default=None, name="fileContractResolutions"
    )
    attestations: Optional[List[Attestation]] = strawberry.field(default=None)
    arbitrary_data: Optional[List[str]] = strawberry.field(default=None, name="arbitraryData")
    new_foundation_address: Optional[Address] = strawberry.field(default=None, name="newFoundationAddress")
    miner_fee: Optional[Currency] = strawberry.field(default=None, name="minerFee")


@strawberry.type
class AutopilotConfig(SiaType):
    enabled: Optional[bool] = strawberry.field(description="""Whether the autopilot is enabled""", default=None)
    contracts: Optional[ContractsConfig] = strawberry.field(default=None)
    hosts: Optional[HostsConfig] = strawberry.field(default=None)


@strawberry.input
class AutopilotConfigInput(SiaInput):
    enabled: Optional[bool] = strawberry.field(description="""Whether the autopilot is enabled""", default=None)
    contracts: Optional[ContractsConfig] = strawberry.field(default=None)
    hosts: Optional[HostsConfig] = strawberry.field(default=None)


@strawberry.type
class Bucket(SiaType):
    name: Optional[BucketName] = strawberry.field(default=None)
    policy: Optional[JSON] = strawberry.field(default=None)
    created_at: Optional[datetime.datetime] = strawberry.field(
        description="""The time the bucket was created | Format: date-time""", default=None, name="createdAt"
    )


@strawberry.input
class BucketInput(SiaInput):
    name: Optional[BucketName] = strawberry.field(default=None)
    policy: Optional[JSON] = strawberry.field(default=None)
    created_at: Optional[datetime.datetime] = strawberry.field(
        description="""The time the bucket was created | Format: date-time""", default=None, name="createdAt"
    )


@strawberry.type
class BuildState(SiaType):
    build_time: Optional[datetime.datetime] = strawberry.field(
        description="""The build time of the build | Format: date-time""", default=None, name="buildTime"
    )
    commit: Optional[str] = strawberry.field(description="""The commit hash of the build""", default=None)
    version: Optional[str] = strawberry.field(description="""The version of the build""", default=None)
    os: Optional[str] = strawberry.field(description="""The operating system of the build""", default=None)


@strawberry.input
class BuildStateInput(SiaInput):
    build_time: Optional[datetime.datetime] = strawberry.field(
        description="""The build time of the build | Format: date-time""", default=None, name="buildTime"
    )
    commit: Optional[str] = strawberry.field(description="""The commit hash of the build""", default=None)
    version: Optional[str] = strawberry.field(description="""The version of the build""", default=None)
    os: Optional[str] = strawberry.field(description="""The operating system of the build""", default=None)


@strawberry.type
class ConfigRecommendation(SiaType):
    gouging_settings: Optional[GougingSettings] = strawberry.field(default=None, name="gougingSettings")


@strawberry.input
class ConfigRecommendationInput(SiaInput):
    gouging_settings: Optional[GougingSettings] = strawberry.field(default=None, name="gougingSettings")


@strawberry.type
class ConsensusState(SiaType):
    block_height: Optional[str] = strawberry.field(default=None, name="blockHeight")
    last_block_time: Optional[datetime.datetime] = strawberry.field(
        description="""The time of the last block | Format: date-time""", default=None, name="lastBlockTime"
    )
    synced: Optional[bool] = strawberry.field(
        description="""Whether the node is synced with the network""", default=None
    )


@strawberry.input
class ConsensusStateInput(SiaInput):
    block_height: Optional[str] = strawberry.field(default=None, name="blockHeight")
    last_block_time: Optional[datetime.datetime] = strawberry.field(
        description="""The time of the last block | Format: date-time""", default=None, name="lastBlockTime"
    )
    synced: Optional[bool] = strawberry.field(
        description="""Whether the node is synced with the network""", default=None
    )


@strawberry.type
class ContractLockID(SiaType):
    lock_id: Optional[int] = strawberry.field(
        description="""The ID of the lock | Format: uint64 | Example: 12""", default=None, name="lockID"
    )


@strawberry.input
class ContractLockIDInput(SiaInput):
    lock_id: Optional[int] = strawberry.field(
        description="""The ID of the lock | Format: uint64 | Example: 12""", default=None, name="lockID"
    )


@strawberry.type
class ContractMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="""Format: date-time""", default=None)
    contract_id: Optional[FileContractID] = strawberry.field(default=None, name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(default=None, name="hostKey")
    remaining_collateral: Optional[Currency] = strawberry.field(default=None, name="remainingCollateral")
    remaining_funds: Optional[Currency] = strawberry.field(default=None, name="remainingFunds")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")
    delete_spending: Optional[Currency] = strawberry.field(default=None, name="deleteSpending")
    fund_account_spending: Optional[Currency] = strawberry.field(default=None, name="fundAccountSpending")
    sector_roots_spending: Optional[Currency] = strawberry.field(default=None, name="sectorRootsSpending")
    upload_spending: Optional[Currency] = strawberry.field(default=None, name="uploadSpending")


@strawberry.input
class ContractMetricInput(SiaInput):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="""Format: date-time""", default=None)
    contract_id: Optional[FileContractID] = strawberry.field(default=None, name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(default=None, name="hostKey")
    remaining_collateral: Optional[Currency] = strawberry.field(default=None, name="remainingCollateral")
    remaining_funds: Optional[Currency] = strawberry.field(default=None, name="remainingFunds")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")
    delete_spending: Optional[Currency] = strawberry.field(default=None, name="deleteSpending")
    fund_account_spending: Optional[Currency] = strawberry.field(default=None, name="fundAccountSpending")
    sector_roots_spending: Optional[Currency] = strawberry.field(default=None, name="sectorRootsSpending")
    upload_spending: Optional[Currency] = strawberry.field(default=None, name="uploadSpending")


@strawberry.type
class ContractPruneMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="""Format: date-time""", default=None)
    contract_id: Optional[FileContractID] = strawberry.field(default=None, name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(default=None, name="hostKey")
    host_version: Optional[str] = strawberry.field(default=None, name="hostVersion")
    pruned: Optional[int] = strawberry.field(description="""Format: uint64""", default=None)
    remaining: Optional[int] = strawberry.field(description="""Format: uint64""", default=None)
    duration: Optional[int] = strawberry.field(description="""Duration in nanoseconds | Format: int64""", default=None)


@strawberry.input
class ContractPruneMetricInput(SiaInput):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="""Format: date-time""", default=None)
    contract_id: Optional[FileContractID] = strawberry.field(default=None, name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(default=None, name="hostKey")
    host_version: Optional[str] = strawberry.field(default=None, name="hostVersion")
    pruned: Optional[int] = strawberry.field(description="""Format: uint64""", default=None)
    remaining: Optional[int] = strawberry.field(description="""Format: uint64""", default=None)
    duration: Optional[int] = strawberry.field(description="""Duration in nanoseconds | Format: int64""", default=None)


@strawberry.type
class ContractsConfig(SiaType):
    amount: Optional[int] = strawberry.field(
        description="""The minimum number of contracts to form | Format: uint64""", default=0
    )
    period: Optional[int] = strawberry.field(
        description="""The length of a contract's period in blocks (1 block being 10 minutes on average) | Format: uint64""",
        default=0,
    )
    renew_window: Optional[int] = strawberry.field(
        description="""The number of blocks before the end of a contract that a contract should be renewed | Format: uint64""",
        default=0,
        name="renewWindow",
    )
    download: Optional[int] = strawberry.field(
        description="""Expected download bandwidth used per period in bytes | Format: uint64""", default=0
    )
    upload: Optional[int] = strawberry.field(
        description="""Expected upload bandwidth used per period in bytes | Format: uint64""", default=0
    )
    storage: Optional[int] = strawberry.field(
        description="""Expected amount of data stored in bytes | Format: uint64""", default=0
    )
    prune: Optional[bool] = strawberry.field(
        description="""Whether to automatically prune deleted data from contracts""", default=False
    )


@strawberry.input
class ContractsConfigInput(SiaInput):
    amount: Optional[int] = strawberry.field(
        description="""The minimum number of contracts to form | Format: uint64""", default=0
    )
    period: Optional[int] = strawberry.field(
        description="""The length of a contract's period in blocks (1 block being 10 minutes on average) | Format: uint64""",
        default=0,
    )
    renew_window: Optional[int] = strawberry.field(
        description="""The number of blocks before the end of a contract that a contract should be renewed | Format: uint64""",
        default=0,
        name="renewWindow",
    )
    download: Optional[int] = strawberry.field(
        description="""Expected download bandwidth used per period in bytes | Format: uint64""", default=0
    )
    upload: Optional[int] = strawberry.field(
        description="""Expected upload bandwidth used per period in bytes | Format: uint64""", default=0
    )
    storage: Optional[int] = strawberry.field(
        description="""Expected amount of data stored in bytes | Format: uint64""", default=0
    )
    prune: Optional[bool] = strawberry.field(
        description="""Whether to automatically prune deleted data from contracts""", default=False
    )


@strawberry.type
class ContractSize(SiaType):
    prunable: Optional[int] = strawberry.field(
        description="""The amount of data that can be pruned from a contract | Format: uint64""", default=None
    )
    size: Optional[int] = strawberry.field(
        description="""The total size of a contract | Format: uint64""", default=None
    )


@strawberry.input
class ContractSizeInput(SiaInput):
    prunable: Optional[int] = strawberry.field(
        description="""The amount of data that can be pruned from a contract | Format: uint64""", default=None
    )
    size: Optional[int] = strawberry.field(
        description="""The total size of a contract | Format: uint64""", default=None
    )


@strawberry.type(
    description="""A transaction or other event that affects the wallet including miner payouts, siafund claims, and file contract payouts."""
)
class Event(SiaType):
    id: Optional[str] = strawberry.field(default=None)
    index: Optional[str] = strawberry.field(default=None)
    confirmations: Optional[int] = strawberry.field(
        description="""The number of blocks on top of the block that triggered the creation of this event | Format: uint64""",
        default=None,
    )
    type: Optional[str] = strawberry.field(
        description="""The type of the event | Allowed values: miner, foundation, siafundClaim, v1Transaction, v1ContractResolution, v2Transaction, v2ContractResolution""",
        default=None,
    )
    data: Optional[JSON] = strawberry.field(default=None)
    maturity_height: Optional[str] = strawberry.field(default=None, name="maturityHeight")
    timestamp: Optional[datetime.datetime] = strawberry.field(
        description="""The time the event was created | Format: date-time""", default=None
    )
    relevant: Optional[List[Address]] = strawberry.field(default=None)


@strawberry.input(
    description="""A transaction or other event that affects the wallet including miner payouts, siafund claims, and file contract payouts."""
)
class EventInput(SiaInput):
    id: Optional[str] = strawberry.field(default=None)
    index: Optional[str] = strawberry.field(default=None)
    confirmations: Optional[int] = strawberry.field(
        description="""The number of blocks on top of the block that triggered the creation of this event | Format: uint64""",
        default=None,
    )
    type: Optional[str] = strawberry.field(
        description="""The type of the event | Allowed values: miner, foundation, siafundClaim, v1Transaction, v1ContractResolution, v2Transaction, v2ContractResolution""",
        default=None,
    )
    data: Optional[JSON] = strawberry.field(default=None)
    maturity_height: Optional[str] = strawberry.field(default=None, name="maturityHeight")
    timestamp: Optional[datetime.datetime] = strawberry.field(
        description="""The time the event was created | Format: date-time""", default=None
    )
    relevant: Optional[List[Address]] = strawberry.field(default=None)


@strawberry.type
class GougingParams(SiaType):
    consensus_state: Optional[ConsensusState] = strawberry.field(default=None, name="consensusState")
    gouging_settings: Optional[GougingSettings] = strawberry.field(default=None, name="gougingSettings")
    redundancy_settings: Optional[RedundancySettings] = strawberry.field(default=None, name="redundancySettings")


@strawberry.input
class GougingParamsInput(SiaInput):
    consensus_state: Optional[ConsensusState] = strawberry.field(default=None, name="consensusState")
    gouging_settings: Optional[GougingSettings] = strawberry.field(default=None, name="gougingSettings")
    redundancy_settings: Optional[RedundancySettings] = strawberry.field(default=None, name="redundancySettings")


@strawberry.type
class GougingSettings(SiaType):
    max_rpc_price: Optional[str] = strawberry.field(default=None, name="maxRPCPrice")
    max_contract_price: Optional[str] = strawberry.field(default=None, name="maxContractPrice")
    max_download_price: Optional[str] = strawberry.field(default=None, name="maxDownloadPrice")
    max_upload_price: Optional[str] = strawberry.field(default=None, name="maxUploadPrice")
    max_storage_price: Optional[str] = strawberry.field(default=None, name="maxStoragePrice")
    host_block_height_leeway: Optional[int] = strawberry.field(
        description="""The number of blocks a host's chain's height can diverge from our own before we stop using it | Format: uint32""",
        default=None,
        name="hostBlockHeightLeeway",
    )
    min_price_table_validity: Optional[int] = strawberry.field(
        description="""The time a host's price table should be valid after acquiring it in milliseconds | Format: uint64""",
        default=None,
        name="minPriceTableValidity",
    )
    min_account_expiry: Optional[int] = strawberry.field(
        description="""The minimum amount of time an account on a host can be idle for before expiring | Format: uint64""",
        default=None,
        name="minAccountExpiry",
    )
    min_max_ephemeral_account_balance: Optional[str] = strawberry.field(
        default=None, name="minMaxEphemeralAccountBalance"
    )


@strawberry.input
class GougingSettingsInput(SiaInput):
    max_rpc_price: Optional[str] = strawberry.field(default=None, name="maxRPCPrice")
    max_contract_price: Optional[str] = strawberry.field(default=None, name="maxContractPrice")
    max_download_price: Optional[str] = strawberry.field(default=None, name="maxDownloadPrice")
    max_upload_price: Optional[str] = strawberry.field(default=None, name="maxUploadPrice")
    max_storage_price: Optional[str] = strawberry.field(default=None, name="maxStoragePrice")
    host_block_height_leeway: Optional[int] = strawberry.field(
        description="""The number of blocks a host's chain's height can diverge from our own before we stop using it | Format: uint32""",
        default=None,
        name="hostBlockHeightLeeway",
    )
    min_price_table_validity: Optional[int] = strawberry.field(
        description="""The time a host's price table should be valid after acquiring it in milliseconds | Format: uint64""",
        default=None,
        name="minPriceTableValidity",
    )
    min_account_expiry: Optional[int] = strawberry.field(
        description="""The minimum amount of time an account on a host can be idle for before expiring | Format: uint64""",
        default=None,
        name="minAccountExpiry",
    )
    min_max_ephemeral_account_balance: Optional[str] = strawberry.field(
        default=None, name="minMaxEphemeralAccountBalance"
    )


@strawberry.type
class GougingSettingsPins(SiaType):
    max_download: Optional[Pin] = strawberry.field(default=None, name="maxDownload")
    max_storage: Optional[Pin] = strawberry.field(default=None, name="maxStorage")
    max_upload: Optional[Pin] = strawberry.field(default=None, name="maxUpload")


@strawberry.input
class GougingSettingsPinsInput(SiaInput):
    max_download: Optional[Pin] = strawberry.field(default=None, name="maxDownload")
    max_storage: Optional[Pin] = strawberry.field(default=None, name="maxStorage")
    max_upload: Optional[Pin] = strawberry.field(default=None, name="maxUpload")


@strawberry.type
class HostsConfig(SiaType):
    max_consecutive_scan_failures: Optional[int] = strawberry.field(
        description="""The maximum number of consecutive scan failures before a host is removed from the database | Format: uint64""",
        default=0,
        name="maxConsecutiveScanFailures",
    )
    max_downtime_hours: Optional[int] = strawberry.field(
        description="""The maximum number of hours a host can be offline before it is removed from the database | Format: uint64""",
        default=0,
        name="maxDowntimeHours",
    )
    min_protocol_version: Optional[str] = strawberry.field(
        description="""The minimum supported protocol version of a host to be considered good""",
        default=None,
        name="minProtocolVersion",
    )


@strawberry.input
class HostsConfigInput(SiaInput):
    max_consecutive_scan_failures: Optional[int] = strawberry.field(
        description="""The maximum number of consecutive scan failures before a host is removed from the database | Format: uint64""",
        default=0,
        name="maxConsecutiveScanFailures",
    )
    max_downtime_hours: Optional[int] = strawberry.field(
        description="""The maximum number of hours a host can be offline before it is removed from the database | Format: uint64""",
        default=0,
        name="maxDowntimeHours",
    )
    min_protocol_version: Optional[str] = strawberry.field(
        description="""The minimum supported protocol version of a host to be considered good""",
        default=None,
        name="minProtocolVersion",
    )


@strawberry.type
class Host(SiaType):
    known_since: Optional[datetime.datetime] = strawberry.field(
        description="""The time the host was first seen | Format: date-time""", default=None, name="knownSince"
    )
    last_announcement: Optional[datetime.datetime] = strawberry.field(
        description="""The time the host last announced itself | Format: date-time""",
        default=None,
        name="lastAnnouncement",
    )
    public_key: Optional[PublicKey] = strawberry.field(default=None, name="publicKey")
    net_address: Optional[str] = strawberry.field(
        description="""The address of the host | Example: foo.bar:1234""", default=None, name="netAddress"
    )
    price_table: Optional[HostPriceTable] = strawberry.field(default=None, name="priceTable")
    settings: Optional[HostSettings] = strawberry.field(default=None)
    v2_settings: Optional[HostV2Settings] = strawberry.field(default=None, name="v2Settings")
    interactions: Optional[HostInteractions] = strawberry.field(default=None)
    scanned: Optional[bool] = strawberry.field(description="""Whether the host has been scanned""", default=None)
    blocked: Optional[bool] = strawberry.field(description="""Whether the host is blocked""", default=None)
    checks: Optional[HostChecks] = strawberry.field(default=None)
    stored_data: Optional[int] = strawberry.field(
        description="""The amount of data stored on the host in bytes | Format: uint64""",
        default=None,
        name="storedData",
    )
    v2_siamux_addresses: Optional[List[str]] = strawberry.field(default=None, name="v2SiamuxAddresses")


@strawberry.input
class HostInput(SiaInput):
    known_since: Optional[datetime.datetime] = strawberry.field(
        description="""The time the host was first seen | Format: date-time""", default=None, name="knownSince"
    )
    last_announcement: Optional[datetime.datetime] = strawberry.field(
        description="""The time the host last announced itself | Format: date-time""",
        default=None,
        name="lastAnnouncement",
    )
    public_key: Optional[PublicKey] = strawberry.field(default=None, name="publicKey")
    net_address: Optional[str] = strawberry.field(
        description="""The address of the host | Example: foo.bar:1234""", default=None, name="netAddress"
    )
    price_table: Optional[HostPriceTable] = strawberry.field(default=None, name="priceTable")
    settings: Optional[HostSettings] = strawberry.field(default=None)
    v2_settings: Optional[HostV2Settings] = strawberry.field(default=None, name="v2Settings")
    interactions: Optional[HostInteractions] = strawberry.field(default=None)
    scanned: Optional[bool] = strawberry.field(description="""Whether the host has been scanned""", default=None)
    blocked: Optional[bool] = strawberry.field(description="""Whether the host is blocked""", default=None)
    checks: Optional[HostChecks] = strawberry.field(default=None)
    stored_data: Optional[int] = strawberry.field(
        description="""The amount of data stored on the host in bytes | Format: uint64""",
        default=None,
        name="storedData",
    )
    v2_siamux_addresses: Optional[List[str]] = strawberry.field(default=None, name="v2SiamuxAddresses")


@strawberry.type
class HostChecks(SiaType):
    gouging_breakdown: Optional[HostGougingBreakdown] = strawberry.field(default=None, name="gougingBreakdown")
    score_breakdown: Optional[HostScoreBreakdown] = strawberry.field(default=None, name="scoreBreakdown")
    usability_breakdown: Optional[HostUsabilityBreakdown] = strawberry.field(default=None, name="usabilityBreakdown")


@strawberry.input
class HostChecksInput(SiaInput):
    gouging_breakdown: Optional[HostGougingBreakdown] = strawberry.field(default=None, name="gougingBreakdown")
    score_breakdown: Optional[HostScoreBreakdown] = strawberry.field(default=None, name="scoreBreakdown")
    usability_breakdown: Optional[HostUsabilityBreakdown] = strawberry.field(default=None, name="usabilityBreakdown")


@strawberry.type
class HostGougingBreakdown(SiaType):
    download_err: Optional[str] = strawberry.field(
        description="""Error message related to download gouging checks.""", default=None, name="downloadErr"
    )
    gouging_err: Optional[str] = strawberry.field(
        description="""Error message related to general gouging checks.""", default=None, name="gougingErr"
    )
    prune_err: Optional[str] = strawberry.field(
        description="""Error message related to pruning checks.""", default=None, name="pruneErr"
    )
    upload_err: Optional[str] = strawberry.field(
        description="""Error message related to upload gouging checks.""", default=None, name="uploadErr"
    )


@strawberry.input
class HostGougingBreakdownInput(SiaInput):
    download_err: Optional[str] = strawberry.field(
        description="""Error message related to download gouging checks.""", default=None, name="downloadErr"
    )
    gouging_err: Optional[str] = strawberry.field(
        description="""Error message related to general gouging checks.""", default=None, name="gougingErr"
    )
    prune_err: Optional[str] = strawberry.field(
        description="""Error message related to pruning checks.""", default=None, name="pruneErr"
    )
    upload_err: Optional[str] = strawberry.field(
        description="""Error message related to upload gouging checks.""", default=None, name="uploadErr"
    )


@strawberry.type
class HostInfo(SiaType):
    public_key: Optional[PublicKey] = strawberry.field(default=None, name="publicKey")
    siamux_addr: Optional[str] = strawberry.field(
        description="""The address of the host | Example: foo.bar:1234""", default=None, name="siamuxAddr"
    )
    v2_siamux_addresses: Optional[List[str]] = strawberry.field(default=None, name="v2SiamuxAddresses")


@strawberry.input
class HostInfoInput(SiaInput):
    public_key: Optional[PublicKey] = strawberry.field(default=None, name="publicKey")
    siamux_addr: Optional[str] = strawberry.field(
        description="""The address of the host | Example: foo.bar:1234""", default=None, name="siamuxAddr"
    )
    v2_siamux_addresses: Optional[List[str]] = strawberry.field(default=None, name="v2SiamuxAddresses")


@strawberry.type
class HostInteractions(SiaType):
    total_scans: Optional[int] = strawberry.field(
        description="""The total number of scans performed on the host. | Format: uint64""",
        default=None,
        name="totalScans",
    )
    last_scan: Optional[datetime.datetime] = strawberry.field(
        description="""Timestamp of the last scan performed. | Format: date-time""", default=None, name="lastScan"
    )
    last_scan_success: Optional[bool] = strawberry.field(
        description="""Indicates whether the last scan was successful.""", default=None, name="lastScanSuccess"
    )
    lost_sectors: Optional[int] = strawberry.field(
        description="""Number of sectors lost since the last reporting period. | Format: uint64""",
        default=None,
        name="lostSectors",
    )
    second_to_last_scan_success: Optional[bool] = strawberry.field(
        description="""Indicates whether the second-to-last scan was successful.""",
        default=None,
        name="secondToLastScanSuccess",
    )
    uptime: Optional[str] = strawberry.field(
        description="""Total uptime duration of the host. | Format: duration""", default=None
    )
    downtime: Optional[str] = strawberry.field(
        description="""Total downtime duration of the host. | Format: duration""", default=None
    )
    successful_interactions: Optional[float] = strawberry.field(
        description="""The number of successful interactions with the host. | Format: float""",
        default=None,
        name="successfulInteractions",
    )
    failed_interactions: Optional[float] = strawberry.field(
        description="""The number of failed interactions with the host. | Format: float""",
        default=None,
        name="failedInteractions",
    )


@strawberry.input
class HostInteractionsInput(SiaInput):
    total_scans: Optional[int] = strawberry.field(
        description="""The total number of scans performed on the host. | Format: uint64""",
        default=None,
        name="totalScans",
    )
    last_scan: Optional[datetime.datetime] = strawberry.field(
        description="""Timestamp of the last scan performed. | Format: date-time""", default=None, name="lastScan"
    )
    last_scan_success: Optional[bool] = strawberry.field(
        description="""Indicates whether the last scan was successful.""", default=None, name="lastScanSuccess"
    )
    lost_sectors: Optional[int] = strawberry.field(
        description="""Number of sectors lost since the last reporting period. | Format: uint64""",
        default=None,
        name="lostSectors",
    )
    second_to_last_scan_success: Optional[bool] = strawberry.field(
        description="""Indicates whether the second-to-last scan was successful.""",
        default=None,
        name="secondToLastScanSuccess",
    )
    uptime: Optional[str] = strawberry.field(
        description="""Total uptime duration of the host. | Format: duration""", default=None
    )
    downtime: Optional[str] = strawberry.field(
        description="""Total downtime duration of the host. | Format: duration""", default=None
    )
    successful_interactions: Optional[float] = strawberry.field(
        description="""The number of successful interactions with the host. | Format: float""",
        default=None,
        name="successfulInteractions",
    )
    failed_interactions: Optional[float] = strawberry.field(
        description="""The number of failed interactions with the host. | Format: float""",
        default=None,
        name="failedInteractions",
    )


@strawberry.type
class HostScoreBreakdown(SiaType):
    age: Optional[float] = strawberry.field(
        description="""Score contribution based on the host's age. | Format: float""", default=None
    )
    collateral: Optional[float] = strawberry.field(
        description="""Score contribution based on the host's collateral amount. | Format: float""", default=None
    )
    interactions: Optional[float] = strawberry.field(
        description="""Score contribution based on successful interactions. | Format: float""", default=None
    )
    storage_remaining: Optional[float] = strawberry.field(
        description="""Score contribution based on remaining storage capacity. | Format: float""",
        default=None,
        name="storageRemaining",
    )
    uptime: Optional[float] = strawberry.field(
        description="""Score contribution based on host uptime. | Format: float""", default=None
    )
    version: Optional[float] = strawberry.field(
        description="""Score contribution based on the host's software version. | Format: float""", default=None
    )
    prices: Optional[float] = strawberry.field(
        description="""Score contribution based on pricing metrics. | Format: float""", default=None
    )


@strawberry.input
class HostScoreBreakdownInput(SiaInput):
    age: Optional[float] = strawberry.field(
        description="""Score contribution based on the host's age. | Format: float""", default=None
    )
    collateral: Optional[float] = strawberry.field(
        description="""Score contribution based on the host's collateral amount. | Format: float""", default=None
    )
    interactions: Optional[float] = strawberry.field(
        description="""Score contribution based on successful interactions. | Format: float""", default=None
    )
    storage_remaining: Optional[float] = strawberry.field(
        description="""Score contribution based on remaining storage capacity. | Format: float""",
        default=None,
        name="storageRemaining",
    )
    uptime: Optional[float] = strawberry.field(
        description="""Score contribution based on host uptime. | Format: float""", default=None
    )
    version: Optional[float] = strawberry.field(
        description="""Score contribution based on the host's software version. | Format: float""", default=None
    )
    prices: Optional[float] = strawberry.field(
        description="""Score contribution based on pricing metrics. | Format: float""", default=None
    )


@strawberry.type
class HostUsabilityBreakdown(SiaType):
    blocked: Optional[bool] = strawberry.field(description="""Indicates if the host is blocked.""", default=None)
    offline: Optional[bool] = strawberry.field(description="""Indicates if the host is offline.""", default=None)
    low_max_duration: Optional[bool] = strawberry.field(
        description="""Indicates if the host has a low maximum contract duration.""",
        default=None,
        name="lowMaxDuration",
    )
    low_score: Optional[bool] = strawberry.field(
        description="""Indicates if the host has a low score.""", default=None, name="lowScore"
    )
    redundant_ip: Optional[bool] = strawberry.field(
        description="""Indicates if the host's IP address is redundant.""", default=None, name="redundantIP"
    )
    gouging: Optional[bool] = strawberry.field(description="""Indicates if the host is gouging prices.""", default=None)
    not_accepting_contracts: Optional[bool] = strawberry.field(
        description="""Indicates if the host is not accepting new contracts.""",
        default=None,
        name="notAcceptingContracts",
    )
    not_announced: Optional[bool] = strawberry.field(
        description="""Indicates if the host has not been announced on the network.""",
        default=None,
        name="notAnnounced",
    )
    not_completing_scan: Optional[bool] = strawberry.field(
        description="""Indicates if the host is failing to complete scans.""", default=None, name="notCompletingScan"
    )


@strawberry.input
class HostUsabilityBreakdownInput(SiaInput):
    blocked: Optional[bool] = strawberry.field(description="""Indicates if the host is blocked.""", default=None)
    offline: Optional[bool] = strawberry.field(description="""Indicates if the host is offline.""", default=None)
    low_max_duration: Optional[bool] = strawberry.field(
        description="""Indicates if the host has a low maximum contract duration.""",
        default=None,
        name="lowMaxDuration",
    )
    low_score: Optional[bool] = strawberry.field(
        description="""Indicates if the host has a low score.""", default=None, name="lowScore"
    )
    redundant_ip: Optional[bool] = strawberry.field(
        description="""Indicates if the host's IP address is redundant.""", default=None, name="redundantIP"
    )
    gouging: Optional[bool] = strawberry.field(description="""Indicates if the host is gouging prices.""", default=None)
    not_accepting_contracts: Optional[bool] = strawberry.field(
        description="""Indicates if the host is not accepting new contracts.""",
        default=None,
        name="notAcceptingContracts",
    )
    not_announced: Optional[bool] = strawberry.field(
        description="""Indicates if the host has not been announced on the network.""",
        default=None,
        name="notAnnounced",
    )
    not_completing_scan: Optional[bool] = strawberry.field(
        description="""Indicates if the host is failing to complete scans.""", default=None, name="notCompletingScan"
    )


@strawberry.type
class MemoryStatus(SiaType):
    available: Optional[int] = strawberry.field(
        description="""The amount of remaining memory currently available in bytes | Format: uint64 | Example: 83886080""",
        default=None,
    )
    total: Optional[int] = strawberry.field(
        description="""The total amount of memory available in bytes | Minimum: 1 | Format: uint64 | Example: 1073741824""",
        default=None,
    )


@strawberry.input
class MemoryStatusInput(SiaInput):
    available: Optional[int] = strawberry.field(
        description="""The amount of remaining memory currently available in bytes | Format: uint64 | Example: 83886080""",
        default=None,
    )
    total: Optional[int] = strawberry.field(
        description="""The total amount of memory available in bytes | Minimum: 1 | Format: uint64 | Example: 1073741824""",
        default=None,
    )


@strawberry.type
class MultipartUpload(SiaType):
    bucket: Optional[str] = strawberry.field(description="""The name of the bucket""", default=None)
    encryption_key: Optional[EncryptionKey] = strawberry.field(default=None, name="encryptionKey")
    key: Optional[str] = strawberry.field(description="""The key of the object""", default=None)
    upload_id: Optional[str] = strawberry.field(default=None, name="uploadID")
    created_at: Optional[datetime.datetime] = strawberry.field(
        description="""When the upload was created | Format: date-time""", default=None, name="createdAt"
    )


@strawberry.input
class MultipartUploadInput(SiaInput):
    bucket: Optional[str] = strawberry.field(description="""The name of the bucket""", default=None)
    encryption_key: Optional[EncryptionKey] = strawberry.field(default=None, name="encryptionKey")
    key: Optional[str] = strawberry.field(description="""The key of the object""", default=None)
    upload_id: Optional[str] = strawberry.field(default=None, name="uploadID")
    created_at: Optional[datetime.datetime] = strawberry.field(
        description="""When the upload was created | Format: date-time""", default=None, name="createdAt"
    )


@strawberry.type
class MultipartListPartItem(SiaType):
    part_number: Optional[int] = strawberry.field(
        description="""The number of this part""", default=None, name="partNumber"
    )
    last_modified: Optional[datetime.datetime] = strawberry.field(
        description="""When this part was last modified | Format: date-time""", default=None, name="lastModified"
    )
    e_tag: Optional[ETag] = strawberry.field(default=None, name="eTag")
    size: Optional[int] = strawberry.field(
        description="""The size of this part in bytes | Format: int64""", default=None
    )


@strawberry.input
class MultipartListPartItemInput(SiaInput):
    part_number: Optional[int] = strawberry.field(
        description="""The number of this part""", default=None, name="partNumber"
    )
    last_modified: Optional[datetime.datetime] = strawberry.field(
        description="""When this part was last modified | Format: date-time""", default=None, name="lastModified"
    )
    e_tag: Optional[ETag] = strawberry.field(default=None, name="eTag")
    size: Optional[int] = strawberry.field(
        description="""The size of this part in bytes | Format: int64""", default=None
    )


@strawberry.type
class MultipartCompletedPart(SiaType):
    part_number: Optional[int] = strawberry.field(
        description="""The number of this part""", default=None, name="partNumber"
    )
    e_tag: Optional[ETag] = strawberry.field(default=None, name="eTag")


@strawberry.input
class MultipartCompletedPartInput(SiaInput):
    part_number: Optional[int] = strawberry.field(
        description="""The number of this part""", default=None, name="partNumber"
    )
    e_tag: Optional[ETag] = strawberry.field(default=None, name="eTag")


# @strawberry.type
# class Object(SiaType):
#     """

#     """
#     _dummy: Optional[str] = strawberry.field(default=None)


# @strawberry.input
# class ObjectInput(SiaInput):
#     """

#     """
#     _dummy: Optional[str] = strawberry.field(default=None)


@strawberry.type
class ObjectMetadata(SiaType):
    bucket: Optional[BucketName] = strawberry.field(default=None)
    etag: Optional[str] = strawberry.field(default=None)
    health: Optional[float] = strawberry.field(description="""The health of the object | Format: float""", default=None)
    mod_time: Optional[datetime.datetime] = strawberry.field(
        description="""When the object was last modified | Format: date-time""", default=None, name="modTime"
    )
    key: Optional[str] = strawberry.field(description="""The key of the object""", default=None)
    size: Optional[int] = strawberry.field(
        description="""The size of the object in bytes | Format: int64""", default=None
    )
    mime_type: Optional[str] = strawberry.field(
        description="""The MIME type of the object""", default=None, name="mimeType"
    )


@strawberry.input
class ObjectMetadataInput(SiaInput):
    bucket: Optional[BucketName] = strawberry.field(default=None)
    etag: Optional[str] = strawberry.field(default=None)
    health: Optional[float] = strawberry.field(description="""The health of the object | Format: float""", default=None)
    mod_time: Optional[datetime.datetime] = strawberry.field(
        description="""When the object was last modified | Format: date-time""", default=None, name="modTime"
    )
    key: Optional[str] = strawberry.field(description="""The key of the object""", default=None)
    size: Optional[int] = strawberry.field(
        description="""The size of the object in bytes | Format: int64""", default=None
    )
    mime_type: Optional[str] = strawberry.field(
        description="""The MIME type of the object""", default=None, name="mimeType"
    )


# @strawberry.type
# class ObjectUserMetadata(SiaType):
#     """
#     User-defined metadata about an object provided through X-Sia-Meta- headers
#     """
#     _dummy: Optional[str] = strawberry.field(default=None)


@strawberry.input
class ObjectUserMetadataInput(SiaInput):
    """
    User-defined metadata about an object provided through X-Sia-Meta- headers
    """

    _dummy: Optional[str] = strawberry.field(default=None)


@strawberry.type
class PackedSlab(SiaType):
    buffer_id: Optional[int] = strawberry.field(
        description="""ID of the buffer containing the slab | Format: uint""", default=None, name="bufferID"
    )
    data: Optional[str] = strawberry.field(description="""The slab data | Format: binary""", default=None)
    encryption_key: Optional[EncryptionKey] = strawberry.field(default=None, name="encryptionKey")


@strawberry.input
class PackedSlabInput(SiaInput):
    buffer_id: Optional[int] = strawberry.field(
        description="""ID of the buffer containing the slab | Format: uint""", default=None, name="bufferID"
    )
    data: Optional[str] = strawberry.field(description="""The slab data | Format: binary""", default=None)
    encryption_key: Optional[EncryptionKey] = strawberry.field(default=None, name="encryptionKey")


@strawberry.type
class Pin(SiaType):
    pinned: Optional[bool] = strawberry.field(description="""Whether pin is enabled""", default=None)
    value: Optional[float] = strawberry.field(
        description="""The value of the underlying currency to which the setting is pinned | Format: float64""",
        default=None,
    )


@strawberry.input
class PinInput(SiaInput):
    pinned: Optional[bool] = strawberry.field(description="""Whether pin is enabled""", default=None)
    value: Optional[float] = strawberry.field(
        description="""The value of the underlying currency to which the setting is pinned | Format: float64""",
        default=None,
    )


@strawberry.type
class PinnedSettings(SiaType):
    currency: Optional[Currency] = strawberry.field(default=None)
    threshold: Optional[float] = strawberry.field(
        description="""A percentage between 0 and 1 that determines when the pinned settings are updated based on the exchange rate at the time | Format: float64""",
        default=None,
    )
    gouging_settings_pins: Optional[GougingSettingsPins] = strawberry.field(default=None, name="gougingSettingsPins")


@strawberry.input
class PinnedSettingsInput(SiaInput):
    currency: Optional[Currency] = strawberry.field(default=None)
    threshold: Optional[float] = strawberry.field(
        description="""A percentage between 0 and 1 that determines when the pinned settings are updated based on the exchange rate at the time | Format: float64""",
        default=None,
    )
    gouging_settings_pins: Optional[GougingSettingsPins] = strawberry.field(default=None, name="gougingSettingsPins")


@strawberry.type
class Network(SiaType):
    name: Optional[str] = strawberry.field(description="""The name of the network""", default=None)
    initial_coinbase: Optional[str] = strawberry.field(default=None, name="initialCoinbase")
    minimum_coinbase: Optional[str] = strawberry.field(default=None, name="minimumCoinbase")
    initial_target: Optional[str] = strawberry.field(default=None, name="initialTarget")
    block_interval: Optional[int] = strawberry.field(
        description="""The block interval | Format: uint64""", default=600000000000, name="blockInterval"
    )
    maturity_delay: Optional[int] = strawberry.field(
        description="""The maturity delay | Format: uint64""", default=144, name="maturityDelay"
    )
    hardfork_dev_addr: Optional[JSON] = strawberry.field(default=None, name="hardforkDevAddr")
    hardfork_tax: Optional[JSON] = strawberry.field(default=None, name="hardforkTax")
    hardfork_storage_proof: Optional[JSON] = strawberry.field(default=None, name="hardforkStorageProof")
    hardfork_oak: Optional[JSON] = strawberry.field(default=None, name="hardforkOak")
    hardfork_asic: Optional[JSON] = strawberry.field(default=None, name="hardforkASIC")
    hardfork_foundation: Optional[JSON] = strawberry.field(default=None, name="hardforkFoundation")
    hardfork_v2: Optional[JSON] = strawberry.field(default=None, name="hardforkV2")


@strawberry.type
class RedundancySettings(SiaType):
    min_shards: Optional[int] = strawberry.field(
        description="""The number of data shards a piece of an object gets erasure-coded into | Minimum: 1 | Format: int32""",
        default=10,
        name="minShards",
    )
    total_shards: Optional[int] = strawberry.field(
        description="""The number of total data shards a piece of an object gets erasure-coded into | Minimum: 2 | Format: int32""",
        default=30,
        name="totalShards",
    )


@strawberry.input
class RedundancySettingsInput(SiaInput):
    min_shards: Optional[int] = strawberry.field(
        description="""The number of data shards a piece of an object gets erasure-coded into | Minimum: 1 | Format: int32""",
        default=10,
        name="minShards",
    )
    total_shards: Optional[int] = strawberry.field(
        description="""The number of total data shards a piece of an object gets erasure-coded into | Minimum: 2 | Format: int32""",
        default=30,
        name="totalShards",
    )


@strawberry.type
class Revision(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(default=None, name="contractID")
    missed_host_value: Optional[Currency] = strawberry.field(default=None, name="missedHostValue")
    renter_funds: Optional[Currency] = strawberry.field(default=None, name="renterFunds")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")
    size: Optional[int] = strawberry.field(
        description="""The size of the contract in bytes | Format: uint64""", default=None
    )


@strawberry.input
class RevisionInput(SiaInput):
    contract_id: Optional[FileContractID] = strawberry.field(default=None, name="contractID")
    missed_host_value: Optional[Currency] = strawberry.field(default=None, name="missedHostValue")
    renter_funds: Optional[Currency] = strawberry.field(default=None, name="renterFunds")
    revision_number: Optional[RevisionNumber] = strawberry.field(default=None, name="revisionNumber")
    size: Optional[int] = strawberry.field(
        description="""The size of the contract in bytes | Format: uint64""", default=None
    )


@strawberry.type
class SlabBuffer(SiaType):
    complete: Optional[bool] = strawberry.field(
        description="""Whether the slab buffer is complete and ready to upload""", default=None
    )
    filename: Optional[str] = strawberry.field(description="""Name of the buffer on disk""", default=None)
    size: Optional[int] = strawberry.field(description="""Size of the buffer | Format: int64""", default=None)
    max_size: Optional[int] = strawberry.field(
        description="""Maximum size of the buffer | Format: int64""", default=None, name="maxSize"
    )
    locked: Optional[bool] = strawberry.field(
        description="""Whether the slab buffer is locked for uploading""", default=None
    )


@strawberry.input
class SlabBufferInput(SiaInput):
    complete: Optional[bool] = strawberry.field(
        description="""Whether the slab buffer is complete and ready to upload""", default=None
    )
    filename: Optional[str] = strawberry.field(description="""Name of the buffer on disk""", default=None)
    size: Optional[int] = strawberry.field(description="""Size of the buffer | Format: int64""", default=None)
    max_size: Optional[int] = strawberry.field(
        description="""Maximum size of the buffer | Format: int64""", default=None, name="maxSize"
    )
    locked: Optional[bool] = strawberry.field(
        description="""Whether the slab buffer is locked for uploading""", default=None
    )


@strawberry.type(description="""A slab of data to migrate""")
class Slab(SiaType):
    health: Optional[float] = strawberry.field(description="""Minimum: 0 | Maximum: 1 | Format: float""", default=None)
    encryption_key: Optional[str] = strawberry.field(default=None, name="encryptionKey")
    min_shards: Optional[int] = strawberry.field(
        description="""The number of data shards the slab is split into | Minimum: 1 | Maximum: 255 | Format: uint8""",
        default=None,
        name="minShards",
    )


@strawberry.input(description="""A slab of data to migrate""")
class SlabInput(SiaInput):
    health: Optional[float] = strawberry.field(description="""Minimum: 0 | Maximum: 1 | Format: float""", default=None)
    encryption_key: Optional[str] = strawberry.field(default=None, name="encryptionKey")
    min_shards: Optional[int] = strawberry.field(
        description="""The number of data shards the slab is split into | Minimum: 1 | Maximum: 255 | Format: uint8""",
        default=None,
        name="minShards",
    )


@strawberry.type(description="""A contiguous region within a slab""")
class SlabSlice(SiaType):
    slab: Optional[Slab] = strawberry.field(default=None)
    offset: Optional[int] = strawberry.field(description="""Format: uint32""", default=None)
    limit: Optional[int] = strawberry.field(description="""Format: uint32""", default=None)


@strawberry.input(description="""A contiguous region within a slab""")
class SlabSliceInput(SiaInput):
    slab: Optional[Slab] = strawberry.field(default=None)
    offset: Optional[int] = strawberry.field(description="""Format: uint32""", default=None)
    limit: Optional[int] = strawberry.field(description="""Format: uint32""", default=None)


@strawberry.type
class S3Settings(SiaType):
    access_key_id: Optional[str] = strawberry.field(
        description="""S3 access key ID""", default=None, name="accessKeyID"
    )
    secret_access_key: Optional[str] = strawberry.field(
        description="""S3 secret access key""", default=None, name="secretAccessKey"
    )
    disable_auth: Optional[bool] = strawberry.field(
        description="""Whether to disable S3 authentication""", default=None, name="disableAuth"
    )


@strawberry.input
class S3SettingsInput(SiaInput):
    access_key_id: Optional[str] = strawberry.field(
        description="""S3 access key ID""", default=None, name="accessKeyID"
    )
    secret_access_key: Optional[str] = strawberry.field(
        description="""S3 secret access key""", default=None, name="secretAccessKey"
    )
    disable_auth: Optional[bool] = strawberry.field(
        description="""Whether to disable S3 authentication""", default=None, name="disableAuth"
    )


@strawberry.type
class UploadedPackedSlab(SiaType):
    buffer_id: Optional[int] = strawberry.field(
        description="""ID of the buffer containing the slab | Format: uint""", default=None, name="bufferID"
    )
    shards: Optional[List[UploadedSector]] = strawberry.field(default=None)


@strawberry.input
class UploadedPackedSlabInput(SiaInput):
    buffer_id: Optional[int] = strawberry.field(
        description="""ID of the buffer containing the slab | Format: uint""", default=None, name="bufferID"
    )
    shards: Optional[List[UploadedSector]] = strawberry.field(default=None)


@strawberry.type
class UploadedSector(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(default=None, name="contractID")
    root: Optional[Hash256] = strawberry.field(default=None)


@strawberry.input
class UploadedSectorInput(SiaInput):
    contract_id: Optional[FileContractID] = strawberry.field(default=None, name="contractID")
    root: Optional[Hash256] = strawberry.field(default=None)


@strawberry.type
class UploadSettings(SiaType):
    packing: Optional[UploadPackingSettings] = strawberry.field(default=None)
    redundancy: Optional[RedundancySettings] = strawberry.field(default=None)


@strawberry.input
class UploadSettingsInput(SiaInput):
    packing: Optional[UploadPackingSettings] = strawberry.field(default=None)
    redundancy: Optional[RedundancySettings] = strawberry.field(default=None)


@strawberry.type
class UploadPackingSettings(SiaType):
    enabled: Optional[bool] = strawberry.field(description="""Whether upload packing is enabled""", default=None)
    slab_buffer_max_size_soft: Optional[int] = strawberry.field(
        description="""Maximum size for slab buffers | Format: int64""", default=None, name="slabBufferMaxSizeSoft"
    )


@strawberry.input
class UploadPackingSettingsInput(SiaInput):
    enabled: Optional[bool] = strawberry.field(description="""Whether upload packing is enabled""", default=None)
    slab_buffer_max_size_soft: Optional[int] = strawberry.field(
        description="""Maximum size for slab buffers | Format: int64""", default=None, name="slabBufferMaxSizeSoft"
    )


@strawberry.type
class WalletMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="""Format: date-time""", default=None)
    confirmed: Optional[Currency] = strawberry.field(default=None)
    spendable: Optional[Currency] = strawberry.field(default=None)
    unconfirmed: Optional[Currency] = strawberry.field(default=None)
    immature: Optional[Currency] = strawberry.field(default=None)


@strawberry.input
class WalletMetricInput(SiaInput):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="""Format: date-time""", default=None)
    confirmed: Optional[Currency] = strawberry.field(default=None)
    spendable: Optional[Currency] = strawberry.field(default=None)
    unconfirmed: Optional[Currency] = strawberry.field(default=None)
    immature: Optional[Currency] = strawberry.field(default=None)


@strawberry.type
class Webhook(SiaType):
    module: Optional[str] = strawberry.field(
        description="""The module this webhook belongs to | Allowed values: alerts""", default=None
    )
    event: Optional[str] = strawberry.field(
        description="""The event type this webhook listens for | Allowed values: dismiss, register""", default=None
    )
    url: Optional[str] = strawberry.field(
        description="""The URL to send webhook events to | Example: https://foo.com:8000/api/events""", default=None
    )
    headers: Optional[JSON] = strawberry.field(
        description="""Custom headers to include in webhook requests""", default=None
    )


@strawberry.input
class WebhookInput(SiaInput):
    module: Optional[str] = strawberry.field(
        description="""The module this webhook belongs to | Allowed values: alerts""", default=None
    )
    event: Optional[str] = strawberry.field(
        description="""The event type this webhook listens for | Allowed values: dismiss, register""", default=None
    )
    url: Optional[str] = strawberry.field(
        description="""The URL to send webhook events to | Example: https://foo.com:8000/api/events""", default=None
    )
    headers: Optional[JSON] = strawberry.field(
        description="""Custom headers to include in webhook requests""", default=None
    )


@strawberry.type
class WebhookEvent(SiaType):
    module: Optional[str] = strawberry.field(
        description="""The module that triggered the event | Allowed values: alerts""", default=None
    )
    event: Optional[str] = strawberry.field(
        description="""The type of event that occurred | Allowed values: dismiss, register""", default=None
    )
    data: Optional[JSON] = strawberry.field(description="""Event-specific data payload""", default=None)


@strawberry.input
class WebhookEventInput(SiaInput):
    module: Optional[str] = strawberry.field(
        description="""The module that triggered the event | Allowed values: alerts""", default=None
    )
    event: Optional[str] = strawberry.field(
        description="""The type of event that occurred | Allowed values: dismiss, register""", default=None
    )
    data: Optional[JSON] = strawberry.field(description="""Event-specific data payload""", default=None)


@strawberry.type
class WebhookQueueInfo(SiaType):
    url: Optional[str] = strawberry.field(description="""The URL of the webhook""", default=None)
    num_pending: Optional[int] = strawberry.field(
        description="""Number of pending events in queue""", default=None, name="numPending"
    )
    last_success: Optional[datetime.datetime] = strawberry.field(
        description="""Timestamp of last successful delivery | Format: date-time""", default=None, name="lastSuccess"
    )
    last_error: Optional[datetime.datetime] = strawberry.field(
        description="""Timestamp of last failed delivery | Format: date-time""", default=None, name="lastError"
    )
    last_error_message: Optional[str] = strawberry.field(
        description="""Message from last failed delivery""", default=None, name="lastErrorMessage"
    )


@strawberry.input
class WebhookQueueInfoInput(SiaInput):
    url: Optional[str] = strawberry.field(description="""The URL of the webhook""", default=None)
    num_pending: Optional[int] = strawberry.field(
        description="""Number of pending events in queue""", default=None, name="numPending"
    )
    last_success: Optional[datetime.datetime] = strawberry.field(
        description="""Timestamp of last successful delivery | Format: date-time""", default=None, name="lastSuccess"
    )
    last_error: Optional[datetime.datetime] = strawberry.field(
        description="""Timestamp of last failed delivery | Format: date-time""", default=None, name="lastError"
    )
    last_error_message: Optional[str] = strawberry.field(
        description="""Message from last failed delivery""", default=None, name="lastErrorMessage"
    )
