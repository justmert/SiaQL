from typing import List, Optional, Union
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from strawberry.scalars import JSON
from typing import List, Optional, Dict, Any
from enum import Enum


# @strawberry.input
# class SiacoinRecipientInput:
#     address: str
#     value: str


# @strawberry.input
# class SiafundRecipientInput:
#     address: str
#     value: int


# # Response Types
# @strawberry.type
# class BroadcastResponse:
#     success: bool
#     message: Optional[str] = None


# @strawberry.type
# class ReserveUTXOsResponse:
#     success: bool
#     message: Optional[str] = None


# @strawberry.type
# class ReleaseUTXOsResponse:
#     success: bool
#     message: Optional[str] = None


# @strawberry.type
# class AddWalletAddressResponse:
#     success: bool
#     message: Optional[str] = None


# @strawberry.type
# class DeleteWalletResponse:
#     success: bool
#     message: Optional[str] = None


# @strawberry.type
# class DeleteWalletAddressResponse:
#     success: bool
#     message: Optional[str] = None


# @strawberry.type
# class NetworkInfo:
#     name: str
#     initial_coinbase: str = strawberry.field(name="initialCoinbase")
#     minimum_coinbase: str = strawberry.field(name="minimumCoinbase")
#     initial_target: str = strawberry.field(name="initialTarget")
#     hardfork_dev_addr: HardforkDevAddr = strawberry.field(name="hardforkDevAddr")
#     hardfork_tax: HardforkTax = strawberry.field(name="hardforkTax")
#     hardfork_storage_proof: HardforkStorageProof = strawberry.field(name="hardforkStorageProof")
#     hardfork_oak: HardforkOak = strawberry.field(name="hardforkOak")
#     hardfork_asic: HardforkASIC = strawberry.field(name="hardforkASIC")
#     hardfork_foundation: HardforkFoundation = strawberry.field(name="hardforkFoundation")
#     hardfork_v2: HardforkV2 = strawberry.field(name="hardforkV2")


# @strawberry.type
# class ElementsInfo:
#     num_leaves: int = strawberry.field(name="numLeaves")
#     trees: List[str]


# @strawberry.type
# class MinerEventData:
#     siacoin_element: SiacoinElement = strawberry.field(name="siacoinElement")


# @strawberry.type
# class Peer:
#     addr: str
#     inbound: bool
#     version: str
#     first_seen: datetime = strawberry.field(name="firstSeen")
#     connected_since: datetime = strawberry.field(name="connectedSince")
#     synced_blocks: int = strawberry.field(name="syncedBlocks")
#     sync_duration: int = strawberry.field(name="syncDuration")


# @strawberry.type
# class ConnectPeerResponse:
#     success: bool
#     message: Optional[str] = None


# @strawberry.type
# class RescanStatus:
#     start_index: BlockIndex = strawberry.field(name="startIndex")
#     index: BlockIndex
#     start_time: datetime = strawberry.field(name="startTime")


# @strawberry.type
# class StartRescanResponse:
#     success: bool
#     message: Optional[str] = None


# @strawberry.type
# class SiacoinRecipient:
#     address: str
#     value: str


# @strawberry.type
# class SiafundRecipient:
#     address: str
#     value: int


# @strawberry.type
# class TransactionBasis:
#     height: int
#     id: str


# @strawberry.type
# class ConstructedTransaction:
#     basis: TransactionBasis
#     id: str
#     transaction: Dict[str, Any] = strawberry.field(description="The constructed transaction")
#     estimated_fee: str = strawberry.field(name="estimatedFee")


# @strawberry.type
# class Wallet:
#     id: str
#     name: str
#     description: str
#     date_created: datetime = strawberry.field(name="dateCreated")
#     last_updated: datetime = strawberry.field(name="lastUpdated")
#     metadata: Optional[Dict[str, Any]] = None


# @strawberry.type
# class WalletAddress:
#     address: str
#     description: str
#     metadata: Optional[Dict[str, Any]] = None


# @strawberry.input
# class AddWalletInput:
#     name: Optional[str] = None
#     description: Optional[str] = None
#     metadata: Optional[Dict[str, Any]] = None


# @strawberry.input
# class AddWalletAddressInput:
#     address: str
#     description: Optional[str] = None
#     spend_policy: Optional[Dict[str, Any]] = strawberry.field(name="spendPolicy", default=None)
#     metadata: Optional[Dict[str, Any]] = None


# @strawberry.type
# class V1Transaction:
#     siacoin_inputs: List[SiacoinInput] = strawberry.field(name="siacoinInputs")
#     siacoin_outputs: List[SiacoinOutput] = strawberry.field(name="siacoinOutputs")
#     miner_fees: List[str] = strawberry.field(name="minerFees")
#     signatures: List[TransactionSignature]


# @strawberry.type
# class TransactionData:
#     transaction: V1Transaction
#     spent_siacoin_elements: Optional[List[Dict[str, Any]]] = strawberry.field(name="spentSiacoinElements", default=None)
#     spent_siafund_elements: Optional[List[Dict[str, Any]]] = strawberry.field(name="spentSiafundElements", default=None)


# @strawberry.type
# class Currency:
#     """Represents a quantity of hastings as an unsigned 128-bit number."""

#     lo: int  # uint64
#     hi: int  # uint64


# @strawberry.type
# class WalletEvent:
#     id: str
#     index: BlockIndex
#     timestamp: datetime
#     maturity_height: int = strawberry.field(name="maturityHeight")
#     type: str
#     data: TransactionData
#     relevant: List[str]


# @strawberry.type
# class WalletBalance:
#     siacoins: str
#     immature_siacoins: str = strawberry.field(name="immatureSiacoins")
#     siafunds: int


# @strawberry.type
# class SiacoinUTXO:
#     id: str
#     leaf_index: int = strawberry.field(name="leafIndex")
#     merkle_proof: MerkleProof = strawberry.field(name="merkleProof")
#     siacoin_output: SiacoinOutput = strawberry.field(name="siacoinOutput")
#     maturity_height: int = strawberry.field(name="maturityHeight")


# @strawberry.type
# class SiafundUTXO:
#     id: str
#     leaf_index: int = strawberry.field(name="leafIndex")
#     merkle_proof: MerkleProof = strawberry.field(name="merkleProof")
#     siafund_output: SiafundOutput = strawberry.field(name="siafundOutput")
#     claim_start: str = strawberry.field(name="claimStart")


# @strawberry.type
# class FundTransactionResponse:
#     transaction: Transaction
#     to_sign: List[str] = strawberry.field(name="toSign")
#     depends_on: Optional[List[str]] = strawberry.field(name="dependsOn", default=None)


# # ---


# @strawberry.enum
# class PolicyType(Enum):
#     """Enumerates the different types of spend policies."""

#     ABOVE = "above"
#     AFTER = "after"
#     PUBLIC_KEY = "publicKey"
#     HASH = "hash"
#     THRESHOLD = "threshold"
#     OPAQUE = "opaque"
#     UNLOCK_CONDITIONS = "unlockConditions"


# @strawberry.type
# class PolicyTypeAbove:
#     """Policy requiring block height to be above a certain value."""

#     height: int = strawberry.field()


# @strawberry.type
# class PolicyTypeAfter:
#     """Policy requiring timestamp to be after a certain time."""

#     timestamp: datetime = strawberry.field()


# @strawberry.type
# class PolicyTypePublicKey:
#     """Policy requiring a valid signature from a specific public key."""

#     public_key: str = strawberry.field(name="publicKey")


# @strawberry.type
# class PolicyTypeHash:
#     """Policy requiring a preimage that hashes to a specific value."""

#     hash: str = strawberry.field(description="32-byte hash in hex format")


# @strawberry.type
# class PolicyTypeThreshold:
#     """Policy requiring M-of-N sub-policies to be satisfied."""

#     minimum: int = strawberry.field()
#     sub_policies: List["SpendPolicy"] = strawberry.field(name="subPolicies")


# @strawberry.type
# class PolicyTypeOpaque:
#     """Policy representing an unknown/opaque set of conditions."""

#     address: str = strawberry.field()


# @strawberry.type
# class PolicyTypeUnlockConditions:
#     """Policy requiring standard unlock conditions to be satisfied."""

#     conditions: UnlockConditions = strawberry.field()


# @strawberry.enum
# class V2FileContractResolutionType(Enum):
#     """Enumerates the types of file contract resolution."""

#     RENEWAL = "renewal"
#     STORAGE_PROOF = "storageProof"
#     EXPIRATION = "expiration"


# @strawberry.type
# class V2FileContractRenewal:
#     final_renter_output: SiacoinOutput = strawberry.field(name="finalRenterOutput")
#     final_host_output: SiacoinOutput = strawberry.field(name="finalHostOutput")
#     renter_rollover: str = strawberry.field(name="renterRollover", description="Currency amount")
#     host_rollover: str = strawberry.field(name="hostRollover", description="Currency amount")
#     new_contract: V2FileContract = strawberry.field(name="newContract")
#     renter_signature: str = strawberry.field(name="renterSignature")
#     host_signature: str = strawberry.field(name="hostSignature")


# @strawberry.type
# class V1TransactionEventData:
#     transaction: Transaction  # Changed from dict to Transaction type
#     spent_siacoin_elements: Optional[List[SiacoinElement]] = strawberry.field(
#         name="spentSiacoinElements", description="Elements spent by this transaction"
#     )
#     spent_siafund_elements: Optional[List[SiafundElement]] = strawberry.field(
#         name="spentSiafundElements", description="Siafund elements spent by this transaction"
#     )


# @strawberry.type
# class V2TransactionEventData:
#     transaction: V2Transaction
#     spent_siacoin_elements: Optional[List[SiacoinElement]] = strawberry.field(name="spentSiacoinElements")
#     spent_siafund_elements: Optional[List[SiafundElement]] = strawberry.field(name="spentSiafundElements")


# @strawberry.type
# class V2TransactionsMultiproof:
#     """A slice of V2Transactions whose Merkle proofs are encoded as a single multiproof."""

#     transactions: List[V2Transaction]


# @strawberry.type
# class ElementID:
#     """A generic 32-byte identifier within the state accumulator."""

#     value: str = strawberry.field(
#         description="32-byte identifier for BlockID, SiacoinOutputID, SiafundOutputID, FileContractID, or AttestationID"
#     )


# @strawberry.type
# class FileContractElement:
#     id: FileContractID
#     state_element: StateElement = strawberry.field(name="stateElement")
#     file_contract: FileContract = strawberry.field(name="fileContract")


# @strawberry.type
# class ChainIndexElement:
#     """A record of a ChainIndex within the state accumulator."""

#     id: BlockID
#     state_element: StateElement = strawberry.field(name="stateElement")
#     chain_index: ChainIndex = strawberry.field(name="chainIndex")


# @strawberry.type
# class V2StorageProof:
#     proof_index: ChainIndexElement = strawberry.field(name="proofIndex")
#     leaf: str = strawberry.field(description="hex-encoded 64-byte leaf")
#     proof: List[Hash256]


# @strawberry.type
# class TipState:
#     index: ChainIndex
#     prev_timestamps: List[datetime] = strawberry.field(name="prevTimestamps")
#     depth: str
#     child_target: str = strawberry.field(name="childTarget")
#     siafund_pool: str = strawberry.field(name="siafundPool")
#     oak_time: str = strawberry.field(name="oakTime")
#     oak_target: str = strawberry.field(name="oakTarget")
#     foundation_primary_address: str = strawberry.field(name="foundationPrimaryAddress")
#     foundation_failsafe_address: str = strawberry.field(name="foundationFailsafeAddress")
#     total_work: str = strawberry.field(name="totalWork")
#     difficulty: str
#     oak_work: str = strawberry.field(name="oakWork")
#     elements: ElementsInfo
#     attestations: int


# @strawberry.type
# class BlockHeader:
#     """The preimage of a Block's ID."""

#     parent_id: str = strawberry.field(name="parentID")
#     nonce: int
#     timestamp: datetime
#     commitment: str


# @strawberry.type
# class V2FileContractExpiration:
#     """
#     A V2FileContractExpiration resolves an expired contract. A contract is
#     considered expired when its proof window has elapsed. If the contract is not
#     storing any data, it will resolve as valid; otherwise, it resolves as missed.
#     """

#     pass  # This type is empty in Go as well


# @strawberry.type
# class FoundationAddressUpdate:
#     """Updates the primary and failsafe Foundation subsidy addresses."""

#     new_primary: str = strawberry.field(name="newPrimary")
#     new_failsafe: str = strawberry.field(name="newFailsafe")


# @strawberry.type
# class AttestationElement:
#     """A record of an Attestation within the state accumulator."""

#     id: AttestationID
#     state_element: StateElement = strawberry.field(name="stateElement")
#     attestation: Attestation


# @strawberry.type
# class TransactionWithoutSignatures:
#     """Helper type for calculating transaction IDs without signature data."""

#     siacoin_inputs: List[SiacoinInput] = strawberry.field(name="siacoinInputs")
#     siacoin_outputs: List[SiacoinOutput] = strawberry.field(name="siacoinOutputs")
#     file_contracts: List[FileContract] = strawberry.field(name="fileContracts")
#     file_contract_revisions: List[FileContractRevision] = strawberry.field(name="fileContractRevisions")
#     storage_proofs: List[StorageProof] = strawberry.field(name="storageProofs")
#     siafund_inputs: List[SiafundInput] = strawberry.field(name="siafundInputs")
#     siafund_outputs: List[SiafundOutput] = strawberry.field(name="siafundOutputs")
#     miner_fees: List[Currency] = strawberry.field(name="minerFees")
#     arbitrary_data: List[str] = strawberry.field(name="arbitraryData", description="hex-encoded arbitrary data")


# @strawberry.type
# class AlertData:
#     account_id: str = strawberry.field(name="accountID")
#     contract_id: str = strawberry.field(name="contractID")
#     host_key: str = strawberry.field(name="hostKey")
#     origin: str


# @strawberry.input
# class AlertsParams:
#     offset: Optional[int] = 0
#     limit: Optional[int] = -1


# @strawberry.input
# class AlertDataInput:
#     account_id: str = strawberry.field(name="accountID")
#     contract_id: str = strawberry.field(name="contractID")
#     host_key: str = strawberry.field(name="hostKey")
#     origin: str


# @strawberry.type
# class ContractConfig:
#     set: str
#     amount: int
#     allowance: str
#     period: int
#     renew_window: int = strawberry.field(name="renewWindow")
#     download: int
#     upload: int
#     storage: int


# @strawberry.type
# class WalletConfig:
#     defrag_threshold: int = strawberry.field(name="defragThreshold")


# @strawberry.type
# class Autopilot:
#     id: str
#     config: AutopilotConfig
#     current_period: int = strawberry.field(name="currentPeriod")


# @strawberry.type
# class Contract:
#     id: str
#     host_ip: str = strawberry.field(name="hostIP")
#     host_key: str = strawberry.field(name="hostKey")
#     siamux_addr: str = strawberry.field(name="siamuxAddr")
#     proof_height: int = strawberry.field(name="proofHeight")
#     revision_height: int = strawberry.field(name="revisionHeight")
#     revision_number: int = strawberry.field(name="revisionNumber")
#     start_height: int = strawberry.field(name="startHeight")
#     window_start: int = strawberry.field(name="windowStart")
#     window_end: int = strawberry.field(name="windowEnd")
#     renewed_from: str = strawberry.field(name="renewedFrom")
#     spending: ContractSpending
#     total_cost: str = strawberry.field(name="totalCost")
#     size: Optional[int] = None
#     state: Optional[str] = None
#     contract_price: Optional[str] = strawberry.field(name="contractPrice", default=None)
#     sets: Optional[List[str]] = None


# @strawberry.type
# class ContractPrunableInfo:
#     id: str
#     prunable: int
#     size: int


# @strawberry.type
# class ContractsPrunableInfo:
#     contracts: List[ContractPrunableInfo]
#     total_prunable: int = strawberry.field(name="totalPrunable")
#     total_size: int = strawberry.field(name="totalSize")


# @strawberry.type
# class ContractRoots:
#     roots: List[str]


# @strawberry.type
# class ArchivedContract:
#     id: str
#     host_key: str = strawberry.field(name="hostKey")
#     renewed_to: str = strawberry.field(name="renewedTo")
#     spending: ContractSpending
#     proof_height: int = strawberry.field(name="proofHeight")
#     revision_height: int = strawberry.field(name="revisionHeight")
#     revision_number: int = strawberry.field(name="revisionNumber")
#     size: int
#     start_height: int = strawberry.field(name="startHeight")
#     state: str
#     window_start: int = strawberry.field(name="windowStart")
#     window_end: int = strawberry.field(name="windowEnd")


# @strawberry.type
# class ContractLock:
#     lock_id: int = strawberry.field(name="lockID")


# @strawberry.input
# class ContractAcquireInput:
#     duration: str
#     priority: int


# @strawberry.input
# class ContractLockInput:
#     lock_id: int = strawberry.field(name="lockID")


# @strawberry.input
# class HostAllowlistInput:
#     add: List[str]
#     remove: List[str]
#     clear: bool


# @strawberry.input
# class HostBlocklistInput:
#     add: List[str]
#     remove: List[str]
#     clear: bool


# @strawberry.type
# class ContractPrunable:
#     contracts: List[ContractPrunableInfo]
#     total_prunable: int = strawberry.field(name="totalPrunable")
#     total_size: int = strawberry.field(name="totalSize")


# @strawberry.type
# class ScanningHost:
#     public_key: str = strawberry.field(name="publicKey")
#     net_address: str = strawberry.field(name="netAddress")


# @strawberry.input
# class HostListUpdateInput:
#     add: List[str]
#     remove: List[str]
#     clear: bool


# @strawberry.input
# class HostRemoveInput:
#     min_recent_scan_failures: int = strawberry.field(name="minRecentScanFailures")
#     max_downtime_hours: str = strawberry.field(name="maxDowntimeHours")


# @strawberry.input
# class ScanningParams:
#     offset: Optional[int] = 0
#     limit: Optional[int] = -1
#     last_scan: Optional[str] = strawberry.field(name="lastScan", default=None)


# @strawberry.type
# class ChurnMetric:
#     direction: str
#     contract_id: str = strawberry.field(name="contractID")
#     name: str
#     timestamp: str


# @strawberry.type
# class ContractSetMetric:
#     contracts: int
#     name: str
#     timestamp: str


# @strawberry.type
# class Object:
#     metadata: "ObjectUserMetadata"
#     object_metadata: ObjectMetadata = strawberry.field(name="objectMetadata")


# @strawberry.type
# class ObjectUserMetadata:
#     data: typing.Dict[str, str]


# @strawberry.input
# class MetricParams:
#     start: str
#     interval: int
#     n: int
#     contract_id: Optional[str] = strawberry.field(name="contractID", default=None)
#     host_key: Optional[str] = strawberry.field(name="hostKey", default=None)
#     name: Optional[str] = None
#     direction: Optional[str] = None
#     reason: Optional[str] = None
#     host_version: Optional[str] = strawberry.field(name="hostVersion", default=None)


# @strawberry.type
# class PriceTable:
#     uid: str
#     validity: int
#     host_block_height: int = strawberry.field(name="hostblockheight")
#     update_pricetable_cost: str = strawberry.field(name="updatepricetablecost")
#     account_balance_cost: str = strawberry.field(name="accountbalancecost")
#     fund_account_cost: str = strawberry.field(name="fundaccountcost")
#     latest_revision_cost: str = strawberry.field(name="latestrevisioncost")
#     subscription_memory_cost: str = strawberry.field(name="subscriptionmemorycost")
#     subscription_notification_cost: str = strawberry.field(name="subscriptionnotificationcost")
#     init_base_cost: str = strawberry.field(name="initbasecost")
#     memory_time_cost: str = strawberry.field(name="memorytimecost")
#     download_bandwidth_cost: str = strawberry.field(name="downloadbandwidthcost")
#     upload_bandwidth_cost: str = strawberry.field(name="uploadbandwidthcost")
#     drop_sectors_base_cost: str = strawberry.field(name="dropsectorsbasecost")
#     drop_sectors_unit_cost: str = strawberry.field(name="dropsectorsunitcost")
#     has_sector_base_cost: str = strawberry.field(name="hassectorbasecost")
#     read_base_cost: str = strawberry.field(name="readbasecost")
#     read_length_cost: str = strawberry.field(name="readlengthcost")
#     renew_contract_cost: str = strawberry.field(name="renewcontractcost")
#     revision_base_cost: str = strawberry.field(name="revisionbasecost")
#     swap_sector_cost: str = strawberry.field(name="swapsectorcost")
#     write_base_cost: str = strawberry.field(name="writebasecost")
#     write_length_cost: str = strawberry.field(name="writelengthcost")
#     write_store_cost: str = strawberry.field(name="writestorecost")
#     txn_fee_min_recommended: str = strawberry.field(name="txnfeeminrecommended")
#     txn_fee_max_recommended: str = strawberry.field(name="txnfeemaxrecommended")
#     contract_price: str = strawberry.field(name="contractprice")
#     collateral_cost: str = strawberry.field(name="collateralcost")
#     max_collateral: str = strawberry.field(name="maxcollateral")
#     max_duration: int = strawberry.field(name="maxduration")
#     window_size: int = strawberry.field(name="windowsize")
#     registry_entries_left: int = strawberry.field(name="registryentriesleft")
#     registry_entries_total: int = strawberry.field(name="registryentriestotal")


# @strawberry.input
# class HostInteractionInput:
#     host: str
#     result: Dict[str, Any]
#     success: bool
#     timestamp: str
#     type: str


# @strawberry.type
# class ContractSet:
#     name: str


# @strawberry.input
# class ContractSetInput:
#     contract_ids: List[str]


# @strawberry.input
# class ContractSpendingUpdate:
#     contract_id: str = strawberry.field(name="contractID")
#     revision_number: int = strawberry.field(name="revisionNumber")
#     size: int
#     uploads: str
#     deletions: str
#     downloads: str
#     fund_account: str = strawberry.field(name="fundAccount")
#     sector_roots: str = strawberry.field(name="sectorRoots")


# @strawberry.type
# class ContractRenewedInfo:
#     id: str
#     host_ip: str = strawberry.field(name="hostIP")
#     host_key: str = strawberry.field(name="hostKey")
#     siamux_addr: str = strawberry.field(name="siamuxAddr")
#     proof_height: int = strawberry.field(name="proofHeight")
#     revision_height: int = strawberry.field(name="revisionHeight")
#     revision_number: int = strawberry.field(name="revisionNumber")
#     size: int
#     start_height: int = strawberry.field(name="startHeight")
#     window_start: int = strawberry.field(name="windowStart")
#     window_end: int = strawberry.field(name="windowEnd")
#     renewed_from: str = strawberry.field(name="renewedFrom")
#     spending: ContractSpending
#     total_cost: str = strawberry.field(name="totalCost")


# @strawberry.type
# class MultipartUploadInfo:
#     upload_id: str = strawberry.field(name="uploadID")


# @strawberry.type
# class MultipartUploadsResponse:
#     uploads: List[MultipartUpload]


# @strawberry.type
# class CompleteMultipartUploadResponse:
#     e_tag: str = strawberry.field(name="eTag")


# @strawberry.input
# class PartInput:
#     part_number: int = strawberry.field(name="partNumber")
#     e_tag: str = strawberry.field(name="eTag")


# @strawberry.input
# class MultipartUploadAbortInput:
#     bucket: str
#     path: str
#     upload_id: str = strawberry.field(name="uploadID")


# @strawberry.input
# class MultipartUploadCompleteInput:
#     bucket: str
#     path: str
#     upload_id: str = strawberry.field(name="uploadID")
#     parts: List[PartInput]


# @strawberry.input
# class MultipartUploadListPartsInput:
#     bucket: str
#     path: str
#     upload_id: str = strawberry.field(name="uploadID")
#     part_number_marker: int = strawberry.field(name="partNumberMarker", default=0)
#     limit: int = 1000


# @strawberry.input
# class MultipartUploadListInput:
#     bucket: str
#     prefix: str = ""
#     path_marker: str = strawberry.field(name="pathMarker", default="")
#     upload_id_marker: str = strawberry.field(name="uploadIDMarker", default="")
#     limit: int = 1000


# # types.py - Object Types


# @strawberry.type
# class ShardContract:
#     contracts: Dict[str, List[str]]
#     latest_host: str = strawberry.field(name="latestHost")
#     root: str


# @strawberry.type
# class SlabShard:
#     health: float
#     key: str
#     min_shards: int = strawberry.field(name="minShards")
#     shards: List[ShardContract]


# @strawberry.type
# class ObjectResponse:
#     has_more: bool = strawberry.field(name="hasMore")
#     object: ObjectInfo


# @strawberry.type
# class ObjectListEntry:
#     name: str
#     size: int
#     health: float


# @strawberry.type
# class DownloadGougingSettings:
#     min_max_collateral: str = strawberry.field(name="minMaxCollateral")
#     max_rpc_price: str = strawberry.field(name="maxRPCPrice")
#     max_contract_price: str = strawberry.field(name="maxContractPrice")
#     max_download_price: str = strawberry.field(name="maxDownloadPrice")
#     max_upload_price: str = strawberry.field(name="maxUploadPrice")
#     max_storage_price: str = strawberry.field(name="maxStoragePrice")
#     host_block_height_leeway: int = strawberry.field(name="hostBlockHeightLeeway")


# @strawberry.type
# class DownloadConsensusState:
#     block_height: int = strawberry.field(name="BlockHeight")
#     synced: bool = strawberry.field(name="Synced")


# @strawberry.type
# class DownloadParameters:
#     contract_set: str = strawberry.field(name="ContractSet")
#     consensus_state: ConsensusState = strawberry.field(name="ConsensusState")
#     gouging_settings: GougingSettings = strawberry.field(name="GougingSettings")
#     redundancy_settings: RedundancySettings = strawberry.field(name="RedundancySettings")
#     transaction_fee: str = strawberry.field(name="TransactionFee")


# @strawberry.type
# class UploadParameters:
#     current_height: int = strawberry.field(name="CurrentHeight")
#     contract_set: str = strawberry.field(name="ContractSet")
#     consensus_state: ConsensusState = strawberry.field(name="ConsensusState")
#     gouging_settings: GougingSettings = strawberry.field(name="GougingSettings")
#     redundancy_settings: RedundancySettings = strawberry.field(name="RedundancySettings")
#     transaction_fee: str = strawberry.field(name="TransactionFee")


# @strawberry.type
# class BusState:
#     start_time: str = strawberry.field(name="startTime")
#     network: str
#     version: str
#     commit: str
#     os: str = strawberry.field(name="OS")
#     build_time: str = strawberry.field(name="buildTime")


# @strawberry.type
# class ObjectStats:
#     num_objects: int = strawberry.field(name="numObjects")
#     num_unfinished_objects: int = strawberry.field(name="numUnfinishedObjects")
#     min_health: float = strawberry.field(name="minHealth")
#     total_objects_size: int = strawberry.field(name="totalObjectsSize")
#     total_unfinished_objects_size: int = strawberry.field(name="totalUnfinishedObjectsSize")
#     total_sectors_size: int = strawberry.field(name="totalSectorsSize")
#     total_uploaded_size: int = strawberry.field(name="totalUploadedSize")


# @strawberry.input
# class PinningValue:
#     pinned: bool
#     value: float


# @strawberry.input
# class AutopilotPinning:
#     allowance: PinningValue


# @strawberry.input
# class PricePinningSettings:
#     enabled: bool
#     currency: str
#     forex_endpoint_url: str = strawberry.field(name="forexEndpointURL")
#     threshold: float
#     autopilots: Dict[str, AutopilotPinning]
#     gouging_settings_pins: GougingSettingsPins = strawberry.field(name="gougingSettingsPins")


# @strawberry.input
# class S3AuthenticationSettings:
#     v4_keypairs: Dict[str, str] = strawberry.field(name="v4Keypairs")


# # types.py - Part 3 - Stats Type


# @strawberry.type
# class SlabStats:
#     total_slabs: int
#     total_data: int
#     total_healthy_slabs: int
#     total_healthy_data: int
#     min_health: float


# @strawberry.type
# class ContractStats:
#     total_contracts: int
#     total_active_contracts: int
#     total_size: int
#     total_spending: Dict[str, str]
#     contract_set_stats: Dict[str, Dict[str, Any]]


# # types.py - Part 4 - Slab and Object Types


# @strawberry.type
# class Shard:
#     contracts: Dict[str, List[str]]
#     latest_host: str = strawberry.field(name="latestHost")
#     root: str


# @strawberry.type
# class SlabMigration:
#     key: str
#     health: float
#     objects: List[str]
#     slabs: List[SlabSlice]


# @strawberry.type
# class PartialSlab:
#     key: str
#     offset: int
#     length: int


# @strawberry.type
# class AddPartialSlabResult:
#     slabs: List[PartialSlab]
#     slab_buffer_max_size_soft_reached: bool = strawberry.field(name="slabBufferMaxSizeSoftReached")


# @strawberry.input
# class ObjectInput:
#     key: str
#     slabs: List[SlabSlice]
#     mime_type: str = strawberry.field(name="mimeType")
#     e_tag: str = strawberry.field(name="eTag")


# @strawberry.input
# class CopyObjectInput:
#     source_bucket: str = strawberry.field(name="sourceBucket")
#     source_path: str = strawberry.field(name="sourcePath")
#     destination_bucket: str = strawberry.field(name="destinationBucket")
#     destination_path: str = strawberry.field(name="destinationPath")


# @strawberry.input
# class RenameObjectInput:
#     bucket: str
#     from_path: str = strawberry.field(name="from")
#     to_path: str = strawberry.field(name="to")
#     mode: str


# @strawberry.input
# class SlabMigrationInput:
#     contract_set: str = strawberry.field(name="contractSet")
#     health_cutoff: float = strawberry.field(name="healthCutoff")
#     limit: int


# # types.py - Multipart Types


# # types.py - Wallet and Transaction Types


# @strawberry.type
# class WalletInfo:
#     scan_height: int = strawberry.field(name="scanHeight")
#     address: str
#     spendable: str
#     confirmed: str
#     unconfirmed: str


# @strawberry.type
# class ScOutput:
#     value: str = strawberry.field(name="Value")
#     address: str = strawberry.field(name="Address")
#     id: str = strawberry.field(name="ID")
#     maturity_height: int = strawberry.field(name="MaturityHeight")


# @strawberry.type
# class WebhookQueue:
#     url: str
#     size: int


# @strawberry.type
# class WebhookInfo:
#     webhooks: List[Webhook]
#     queues: List[WebhookQueue]


# @strawberry.input
# class WebhookActionInput:
#     module: str
#     event: str
#     payload: Any


# @strawberry.type
# class TxPoolTransaction:
#     siacoin_inputs: List[Dict[str, Any]] = strawberry.field(name="SiacoinInputs")
#     siacoin_outputs: List[Dict[str, Any]] = strawberry.field(name="SiacoinOutputs")
#     file_contracts: List[Dict[str, Any]] = strawberry.field(name="FileContracts")
#     file_contract_revisions: List[Dict[str, Any]] = strawberry.field(name="FileContractRevisions")
#     storage_proofs: List[Dict[str, Any]] = strawberry.field(name="StorageProofs")
#     siafund_inputs: List[Dict[str, Any]] = strawberry.field(name="SiafundInputs")
#     siafund_outputs: List[Dict[str, Any]] = strawberry.field(name="SiafundOutputs")
#     miner_fees: List[str] = strawberry.field(name="MinerFees")
#     arbitrary_data: List[str] = strawberry.field(name="ArbitraryData")
#     signatures: List[Dict[str, Any]] = strawberry.field(name="Signatures")


# @strawberry.type
# class WalletRedistributeResult:
#     transaction_ids: List[str]


# @strawberry.input
# class RedistributeInput:
#     amount: str
#     outputs: int


# @strawberry.input
# class TransactionSignInput:
#     transaction: Dict[str, Any]
#     to_sign: List[str]
#     covered_fields: Dict[str, Any]


# @strawberry.input
# class ContractPrepareInput:
#     end_height: int = strawberry.field(name="endHeight")
#     host_collateral: str = strawberry.field(name="hostCollateral")
#     host_key: str = strawberry.field(name="hostKey")
#     host_settings: Dict[str, Any] = strawberry.field(name="hostSettings")
#     renter_address: str = strawberry.field(name="renterAddress")
#     renter_funds: str = strawberry.field(name="renterFunds")
#     renter_key: str = strawberry.field(name="renterKey")


# @strawberry.input
# class ContractRenewInput:
#     contract: Dict[str, Any]
#     end_height: int = strawberry.field(name="endHeight")
#     host_settings: Dict[str, Any] = strawberry.field(name="hostSettings")
#     new_collateral: str = strawberry.field(name="newCollateral")
#     renter_address: str = strawberry.field(name="renterAddress")
#     renter_funds: str = strawberry.field(name="renterFunds")
#     renter_key: str = strawberry.field(name="renterKey")


# @strawberry.input
# class TransactionFundInput:
#     transaction: Dict[str, Any]
#     amount: str


# @strawberry.type
# class PreparedTransaction:
#     transaction_set: List[Dict[str, Any]] = strawberry.field(name="transactionSet")
#     final_payment: Optional[str] = strawberry.field(name="finalPayment")


# @strawberry.type
# class MultipartListPartsResponse:
#     has_more: bool = strawberry.field(name="hasMore")
#     next_marker: int = strawberry.field(name="nextMarker")
#     parts: List[MultipartPart]


# @strawberry.type
# class MultipartCompleteResponse:
#     etag: str = strawberry.field(name="eTag")


# @strawberry.type
# class MultipartCreateResponse:
#     upload_id: str = strawberry.field(name="uploadID")


# @strawberry.input
# class MultipartAbortInput:
#     bucket: str
#     path: str
#     upload_id: str = strawberry.field(name="uploadID")


# @strawberry.input
# class MultipartListPartsInput:
#     bucket: str
#     path: str
#     upload_id: str = strawberry.field(name="uploadID")
#     part_number_marker: int = strawberry.field(name="partNumberMarker", default=0)
#     limit: int = -1


# @strawberry.input
# class MultipartListUploadsInput:
#     bucket: str
#     prefix: str = ""
#     path_marker: str = strawberry.field(name="pathMarker", default="")
#     upload_id_marker: str = strawberry.field(name="uploadIDMarker", default="")
#     limit: int = -1


# @strawberry.input
# class UploadSectorInput:
#     contract_id: str = strawberry.field(name="contractID")
#     root: str


# # types.py - Object Types


# @strawberry.type
# class ObjectShard:
#     contracts: Dict[str, List[str]]
#     latest_host: str = strawberry.field(name="latestHost")
#     root: str


# @strawberry.type
# class ObjectSlab:
#     health: float
#     key: str
#     min_shards: int = strawberry.field(name="minShards")
#     shards: List[ObjectShard]


# @strawberry.type
# class ObjectSlabSlice:
#     slab: ObjectSlab
#     offset: int
#     length: int


# @strawberry.type
# class ObjectInfo:
#     etag: str = strawberry.field(name="eTag")
#     health: float
#     mime_type: str = strawberry.field(name="mimeType")
#     mod_time: str = strawberry.field(name="modTime")
#     name: str
#     size: int
#     key: str
#     slabs: List[ObjectSlabSlice]


# @strawberry.type
# class ObjectListResponse:
#     has_more: bool = strawberry.field(name="hasMore")
#     object: Optional[ObjectInfo] = None
#     objects: Optional[List[ObjectInfo]] = None


# @strawberry.input
# class ObjectListInput:
#     bucket: str = strawberry.field(name="bucket")
#     prefix: Optional[str] = strawberry.field(name="prefix")
#     marker: Optional[str] = strawberry.field(name="marker")
#     offset: Optional[int] = strawberry.field(name="offset")
#     limit: Optional[int] = strawberry.field(name="limit")


# @strawberry.input
# class ObjectStoreInput:
#     bucket: str
#     contract_set: str = strawberry.field(name="contractSet")
#     object: Dict[str, Any]
#     mime_type: str = strawberry.field(name="mimeType")
#     etag: str = strawberry.field(name="eTag")


# @strawberry.input
# class ObjectCopyInput:
#     source_bucket: str = strawberry.field(name="sourceBucket")
#     source_path: str = strawberry.field(name="sourcePath")
#     destination_bucket: str = strawberry.field(name="destinationBucket")
#     destination_path: str = strawberry.field(name="destinationPath")


# # types.py - Part 1 - Base Types


# @strawberry.type
# class WorkerState:
#     configured: bool
#     migrating: bool
#     migrating_last_start: str = strawberry.field(name="migratingLastStart")
#     scanning: bool
#     scanning_last_start: str = strawberry.field(name="scanningLastStart")
#     uptime_ms: int = strawberry.field(name="uptimeMS")
#     start_time: str = strawberry.field(name="startTime")
#     network: str
#     version: str
#     commit: str
#     os: str = strawberry.field(name="OS")
#     build_time: str = strawberry.field(name="buildTime")


# @strawberry.type
# class MemoryStats:
#     available: int
#     total: int


# @strawberry.type
# class WorkerMemory:
#     upload: MemoryStats


# @strawberry.type
# class MultipartPart:
#     part_number: int = strawberry.field(name="partNumber")
#     last_modified: str = strawberry.field(name="lastModified")
#     etag: str = strawberry.field(name="eTag")
#     size: int


# # STARTS

# # INTERFACES
# # *******************************************




# @strawberry.type
# class Hash256(SiaType):
#     # A Hash256 is a generic 256-bit cryptographic hash
#     value: str = strawberry.field(description="hex-encoded 32-byte hash")


# @strawberry.type
# class AttestationID(SiaType):
#     value: Hash256 = strawberry.field(description="uniquely identifies an attestation")


# @strawberry.type
# class FileContractID(SiaType):
#     value: Hash256 = strawberry.field(description="uniquely identifies an attestation")


# @strawberry.type
# class PublicKey(SiaType):
#     value: str = strawberry.field(description="hex-encoded 32-byte public key")


# @strawberry.type
# class PrivateKey(SiaType):
#     value: str = strawberry.field(description="hex-encoded private key")


# @strawberry.type
# class Signature(SiaType):
#     value: str = strawberry.field(description="hex-encoded 64-byte signature")


# @strawberry.type
# class Specifier(SiaType):
#     value: str = strawberry.field(description="16-byte identifier")


# @strawberry.type
# class Address(SiaType):
#     value: Hash256 = strawberry.field(description="uniquely identifies an attestation")


# @strawberry.type
# class BlockID(SiaType):
#     value: Hash256 = strawberry.field(description="uniquely identifies a block")


# @strawberry.type
# class TransactionID(SiaType):
#     value: Hash256 = strawberry.field(description="uniquely identifies a transaction")


# @strawberry.type
# class Balance(SiaType):
#     siacoins: str  # Currency
#     immature_siacoins: str = strawberry.field(name="immatureSiacoins")  # Currency
#     siafunds: int


# @strawberry.type
# class AddressBalance(SiaType):
#     address: Address = strawberry.field(name="address")
#     balance: Balance = strawberry.field(name="balance")


# @strawberry.type
# class HardforkDevAddr(SiaType):
#     height: int = strawberry.field()
#     old_address: Address = strawberry.field(name="oldAddress")
#     new_address: Address = strawberry.field(name="newAddress")


# @strawberry.type
# class HardforkTax(SiaType):
#     height: int = strawberry.field(name="height")


# @strawberry.type
# class HardforkStorageProof(SiaType):
#     height: int = strawberry.field(name="height")


# @strawberry.type
# class HardforkOak(SiaType):
#     height: int = strawberry.field(name="height")
#     fix_height: int = strawberry.field(name="fixHeight")
#     genesis_timestamp: datetime = strawberry.field(name="genesisTimestamp")  # time.time


# @strawberry.type
# class HardforkASIC(SiaType):
#     height: int = strawberry.field(name="height")
#     oak_time: str = strawberry.field(name="oakTime")  # time.Duration
#     oak_target: BlockID = strawberry.field(name="oakTarget")


# @strawberry.type
# class HardforkFoundation(SiaType):
#     height: int = strawberry.field(name="height")
#     primary_address: Address = strawberry.field(name="primaryAddress")
#     failsafe_address: Address = strawberry.field(name="failsafeAddress")


# @strawberry.type
# class HardforkV2(SiaType):
#     allow_height: int = strawberry.field(name="allowHeight")
#     require_height: int = strawberry.field(name="requireHeight")


# @strawberry.input
# class Network(SiaType):
#     name: Optional[str] = strawberry.field(description="""The name of the network""", default=None)
#     initial_coinbase: Optional[str] = strawberry.field(default=None, name="initialCoinbase")
#     minimum_coinbase: Optional[str] = strawberry.field(default=None, name="minimumCoinbase")
#     initial_target: Optional[BlockID] = strawberry.field(default=None, name="initialTarget")
#     block_interval: Optional[int] = strawberry.field(
#         description="""The block interval | Format: uint64""", default=600000000000, name="blockInterval"
#     )
#     maturity_delay: Optional[int] = strawberry.field(
#         description="""The maturity delay | Format: uint64""", default=144, name="maturityDelay"
#     )
#     hardfork_dev_addr: Optional[HardforkDevAddr] = strawberry.field(default=None, name="hardforkDevAddr")
#     hardfork_tax: Optional[HardforkTax] = strawberry.field(default=None, name="hardforkTax")
#     hardfork_storage_proof: Optional[HardforkStorageProof] = strawberry.field(default=None, name="hardforkStorageProof")
#     hardfork_oak: Optional[HardforkOak] = strawberry.field(default=None, name="hardforkOak")
#     hardfork_asic: Optional[HardforkASIC] = strawberry.field(default=None, name="hardforkASIC")
#     hardfork_foundation: Optional[HardforkFoundation] = strawberry.field(default=None, name="hardforkFoundation")
#     hardfork_v2: Optional[HardforkV2] = strawberry.field(default=None, name="hardforkV2")


# @strawberry.type
# class ContractRevision(SiaType):
#     """A ContractRevision pairs a file contract with its signatures."""

#     revision: FileContractRevision = strawberry.field(description="The file contract revision")
#     signatures: List[TransactionSignature] = strawberry.field(
#         description="The signatures for the revision", max_length=2
#     )


# @strawberry.type
# class ContractPruneResponse(SiaType):
#     size: Optional[int] = strawberry.field(description="""Size of the contract. | Format: uint64""", default=None)
#     pruned: Optional[int] = strawberry.field(
#         description="""Amount of data pruned from the contract. | Format: uint64""", default=None
#     )
#     remaining: Optional[int] = strawberry.field(
#         description="""Amount of data remaining in the contract. | Format: uint64""", default=None
#     )
#     error: Optional[str] = strawberry.field(default=None)


# @strawberry.input
# class HostScanRequest(SiaType):
#     timeout: datetime.datetime = strawberry.field(description="""The timeout duration in milliseconds""")  # DurationMS


# @strawberry.type
# class HostScanResponse(SiaType):
#     ping: str = strawberry.field(description="Duration in milliseconds", name="ping")
#     scan_error: Optional[str] = strawberry.field(default=None, name="scanError")
#     settings: Optional[HostSettings] = strawberry.field(default=None)  # rhpv2.HostSettings
#     price_table: Optional[HostPriceTable] = strawberry.field(default=None, name="priceTable")
#     v2_settings: Optional[HostV2Settings] = strawberry.field(default=None, name="v2Settings")  # rhp4.HostSettings


# @strawberry.type
# class RHPFormResponse(SiaType):
#     contract_id: FileContractID = strawberry.field(name="contractID")
#     contract: ContractRevision = strawberry.field(name="contract")
#     transaction_set: List[Transaction] = strawberry.field(name="transactionSet")


# @strawberry.input
# class RHPFundRequest(SiaType):
#     contract_id: FileContractID = strawberry.field(name="contractID")
#     host_key: PublicKey = strawberry.field(name="hostKey")
#     siamux_addr: str = strawberry.field(name="siamuxAddr")
#     balance: str = strawberry.field(name="balance")


# @strawberry.input
# class RHPSyncRequest(SiaType):
#     contract_id: FileContractID = strawberry.field(name="contractID")
#     host_key: PublicKey = strawberry.field(name="hostKey")
#     siamux_addr: str = strawberry.field(name="siamuxAddr")


# # ----------------------------------------------------------------------------


# # from datetime import datetime, timedelta
# # import typing
# # from int import int
# # import strawberry
# # from enum import Enum
# # import dataclasses

# # # Constants
# # BLOCKS_PER_DAY = 144

# # S3_MIN_ACCESS_KEY_LEN = 16
# # S3_MAX_ACCESS_KEY_LEN = 128
# # S3_SECRET_KEY_LEN = 40


# # Contract States
# @strawberry.enum
# class ContractState(str, Enum):
#     INVALID = "invalid"
#     UNKNOWN = "unknown"
#     PENDING = "pending"
#     ACTIVE = "active"
#     COMPLETE = "complete"
#     FAILED = "failed"


# # Contract Usability
# @strawberry.enum
# class ContractUsability(str, Enum):
#     BAD = "bad"
#     GOOD = "good"


# # Contract Archival Reasons
# @strawberry.enum
# class ContractArchivalReason(str, Enum):
#     HOST_PRUNED = "hostpruned"
#     REMOVED = "removed"
#     RENEWED = "renewed"


# # Filter Modes
# @strawberry.enum
# class ContractFilterMode(str, Enum):
#     ALL = "all"
#     ACTIVE = "active"
#     ARCHIVED = "archived"
#     GOOD = "good"


# @strawberry.enum
# class HostFilterMode(str, Enum):
#     ALL = "all"
#     ALLOWED = "allowed"
#     BLOCKED = "blocked"


# @strawberry.enum
# class UsabilityFilterMode(str, Enum):
#     ALL = "all"
#     USABLE = "usable"
#     UNUSABLE = "unusable"


# @strawberry.type
# class AccountsAddBalanceRequest(SiaType):
#     host_key: PublicKey = strawberry.field(name="hostKey")
#     amount: int = strawberry.field(name="amount")


# @strawberry.type
# class AccountHandlerPOST(SiaType):
#     host_key: PublicKey = strawberry.field(name="hostKey")


# @strawberry.type
# class AccountsRequiresSyncRequest(SiaType):
#     host_key: PublicKey = strawberry.field(name="hostKey")


# @strawberry.type
# class AccountsUpdateBalanceRequest(SiaType):
#     host_key: PublicKey = strawberry.field(name="hostKey")
#     amount: int = strawberry.field(name="amount")


# @strawberry.type
# class AutopilotTriggerRequest(SiaType):
#     force_scan: bool = strawberry.field(name="forceScan")


# @strawberry.type
# class AutopilotTriggerResponse(SiaType):
#     triggered: bool = strawberry.field(name="triggered")


# @strawberry.type
# class AutopilotStateResponse(BuildState):
#     enabled: bool = strawberry.field(name="enabled")
#     migrating: bool = strawberry.field(name="migrating")
#     migrating_last_start: datetime.datetime = strawberry.field(name="migratingLastStart")
#     pruning: bool = strawberry.field(name="pruning")
#     pruning_last_start: datetime.datetime = strawberry.field(name="pruningLastStart")
#     scanning: bool = strawberry.field(name="scanning")
#     scanning_last_start: datetime.datetime = strawberry.field(name="scanningLastStart")
#     uptime_ms: int = strawberry.field(name="uptimeMs")  # TimeRFC3339
#     start_time: datetime.datetime = strawberry.field(name="startTime")  # DurationMS


# @strawberry.type
# class BucketPolicy(SiaType):
#     public_read_access: bool = strawberry.field(name="publicReadAccess")


# @strawberry.type
# class CreateBucketOptions(SiaType):
#     policy: BucketPolicy = strawberry.field(name="policy")


# @strawberry.type
# class BucketCreateRequest(SiaType):
#     name: str = strawberry.field(name="name")
#     policy: BucketPolicy = strawberry.field(name="policy")


# @strawberry.type
# class BucketUpdatePolicyRequest(SiaType):
#     policy: BucketPolicy = strawberry.field(name="policy")


# # Upload Types
# @strawberry.type
# class UploadParams(GougingParams):
#     current_height: int = strawberry.field(name="currentHeight")
#     upload_packing: bool = strawberry.field(name="uploadPacking")


# @strawberry.type
# class ContractPrunableData(ContractSize):
#     id: FileContractID = strawberry.field(name="ID")


# @strawberry.type
# class ContractsPrunableDataResponse(SiaType):
#     contracts: typing.List[ContractPrunableData] = strawberry.field(name="contracts")
#     total_prunable: int = strawberry.field(name="totalPrunable")
#     total_size: int = strawberry.field(name="totalSize")


# @strawberry.type
# class UnhealthySlab(SiaType):
#     encryption_key: EncryptionKey = strawberry.field(name="encryptionKey")
#     health: float = strawberry.field(name="health")


# @strawberry.type
# class SlabsForMigrationResponse(SiaType):
#     slabs: typing.List[UnhealthySlab] = strawberry.field(name="slabs")


# @strawberry.type
# class DownloaderStats(SiaType):
#     avg_sector_download_speed_mbps: float = strawberry.field(name="avgSectorDownloadSpeedMbps")
#     host_key: PublicKey = strawberry.field(name="hostKey")


# @strawberry.type
# class DownloadStatsResponse(SiaType):
#     avg_download_speed_mbps: float = strawberry.field(name="avgDownloadSpeedMbps")
#     avg_overdrive_pct: float = strawberry.field(name="avgOverdrivePct")
#     healthy_downloaders: int = strawberry.field(name="healthyDownloaders")
#     num_downloaders: int = strawberry.field(name="numDownloaders")
#     downloaders_stats: typing.List[DownloaderStats] = strawberry.field(name="downloadersStats")


# @strawberry.type
# class UploaderStats(SiaType):
#     host_key: PublicKey = strawberry.field(name="hostKey")
#     avg_sector_upload_speed_mbps: float = strawberry.field(name="avgSectorUploadSpeedMbps")


# @strawberry.type
# class UploadStatsResponse(SiaType):
#     avg_slab_upload_speed_mbps: float = strawberry.field(name="avgSlabUploadSpeedMbps")
#     avg_overdrive_pct: float = strawberry.field(name="avgOverdrivePct")
#     healthy_uploaders: int = strawberry.field(name="healthyUploaders")
#     num_uploaders: int = strawberry.field(name="numUploaders")
#     uploaders_stats: typing.List[UploaderStats] = strawberry.field(name="uploadersStats")


# ****************************************
# BELOW TYPES ARE GENERATED AUTOMATICALLY
# ****************************************

@strawberry.interface
class SiaType:
    """Base interface for types converted from Sia network API responses"""
    pass


@strawberry.interface
class NewType:
    """Base interface for types converted from Sia network API responses"""
    pass


@strawberry.scalar(description="An unsigned amount of Hastings, the smallest unit of currency in Sia. 1 Siacoin (SC) equals 10^24 Hastings (H). | Pattern: ^\d+$ | Max length: 39")
class Currency(str):
    pass


@strawberry.scalar(description="A unique identifier for a file contract | Pattern: ^fcid:[0-9a-fA-F]{64}$")
class FileContractID(str):
    pass


@strawberry.scalar(description="A 256-bit blake2b hash | Pattern: ^[0-9a-fA-F]{64}$")
class Hash256(str):
    pass


@strawberry.scalar(description="A ed25519 public key | Pattern: ^ed25519:[0-9a-fA-F]{64}$")
class PublicKey(str):
    pass


@strawberry.scalar(description="A ed25519 signature | Pattern: [0-9a-fA-F]{64} | Format: byte")
class Signature(str):
    pass


@strawberry.scalar(description="A signed amount of Hastings, the smallest unit of currency in Sia. 1 Siacoin (SC) equals 10^24 Hastings (H). | Pattern: ^-?\d+$ | Max length: 39")
class SignedCurrency(str):
    pass


@strawberry.scalar(description="The height of a block | Format: uint64 | Example: 92813")
class BlockHeight(int):
    pass


@strawberry.scalar(description="The name of the bucket. | Pattern: (?!(^xn--|.+-s3alias$))^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$ | Example: default")
class BucketName(str):
    pass


@strawberry.scalar(description="A duration in milliseconds | Format: int64 | Example: 30000")
class DurationMS(int):
    pass



@strawberry.scalar(description="A duration in hours | Format: int64 | Example: 3")
class DurationH(int):
    pass



@strawberry.scalar(description="A key used to encrypt and decrypt data. The key is either a regular key (key) or a salted key (skey). The latter requires a seed to be used for encryption and decryption. | Pattern: ^(key|skey):[0-9a-fA-F]{64}$")
class EncryptionKey(str):
    pass


@strawberry.scalar(description="An ETag representing a resource | Pattern: ^(W/)?""$ | Example: W")
class ETag(str):
    pass


@strawberry.scalar(description="A unique identifier for a multipart upload | Pattern: ^[0-9a-fA-F]{64}$")
class MultipartUploadID(str):
    pass


@strawberry.scalar(description="The revision number of the contract | Format: uint64 | Example: 246")
class RevisionNumber(int):
    pass


@strawberry.scalar(description="Represents a semantic version as an array of three unsigned 8-bit integers: [major, minor, patch] | Example: [1, 2, 3]")
class SemVer(List[int]):
    pass


@strawberry.scalar(description="A 16-byte unique identifier represented as a hex string. | Format: byte | Example: 4d3b2a1c9f8e7d6c5b4a3f2e1d0c9b8a")
class SettingsID(str):
    pass


@strawberry.scalar(description="A 32-byte unique identifier represented as a hex string. | Format: byte | Example: f1e2d3c4b5a697887776665544332211ffeeddccbbaa99887766554433221100")
class UploadID(str):
    pass


@strawberry.scalar(description="The address of the syncer | Example: 118.92.232.145:9981")
class SyncerAddress(str):
    pass


@strawberry.type(description="Unique identifier for a Siacoin output.")
class SiacoinOutputID(Hash256):
    pass


@strawberry.type(description="Unique identifier for a Siafund output.")
class SiafundOutputID(Hash256):
    pass



@strawberry.type
class StateElement(SiaType):
    leaf_index: Optional[int] = strawberry.field(description="The index of the element in the Merkle tree | Format: uint64", name="leafIndex")
    merkle_proof: Optional[List[Hash256]] = strawberry.field(description="The Merkle proof demonstrating the inclusion of the leaf", name="merkleProof")


@strawberry.type(description="Unique identifier for a transaction.")
class TransactionID(Hash256):
    pass


@strawberry.type
class CoveredFields(SiaType):
    whole_transaction: Optional[bool] = strawberry.field(description="Whether the whole transaction is covered by the signature", name="wholeTransaction")
    siacoin_inputs: Optional[List[int]] = strawberry.field(name="siacoinInputs")
    siacoin_outputs: Optional[List[int]] = strawberry.field(name="siacoinOutputs")
    file_contracts: Optional[List[int]] = strawberry.field(name="fileContracts")
    file_contract_revisions: Optional[List[int]] = strawberry.field(name="fileContractRevisions")
    storage_proofs: Optional[List[int]] = strawberry.field(name="storageProofs")
    siafund_inputs: Optional[List[int]] = strawberry.field(name="siafundInputs")
    siafund_outputs: Optional[List[int]] = strawberry.field(name="siafundOutputs")
    miner_fees: Optional[List[int]] = strawberry.field(name="minerFees")
    arbitrary_data: Optional[List[int]] = strawberry.field(name="arbitraryData")
    signatures: Optional[List[int]] = strawberry.field(name="signatures")


@strawberry.type
class UnlockKey(SiaType):
    algorithm: Optional[str] = strawberry.field(description="A fixed 16-byte array that specifies the algorithm used to generatethe key | Format: bytes | Example: ed25519", name="algorithm")
    key: Optional[str] = strawberry.field(description="A 32-byte key represented as a hex-encoded string. Must be exactly64 characters long, containing only hexadecimal digits | Pattern: ^[a-fA-F0-9]{64}$ | Format: bytes", name="key")


@strawberry.type
class UnlockConditions(SiaType):
    timelock: Optional[BlockHeight] = strawberry.field(description="The block height at which the outputs can be spent", name="timelock")
    public_keys: Optional[List[UnlockKey]] = strawberry.field(name="publicKeys")
    signatures_required: Optional[int] = strawberry.field(description="The number of signatures required to spend the output | Format: uint64", name="signaturesRequired")


@strawberry.type
class Account(SiaType):
    id: Optional[PublicKey] = strawberry.field(description="The account's ID", name="id")
    clean_shutdown: Optional[bool] = strawberry.field(description="Whether the account has been cleanly shutdown. If not, the account will require a sync with the host.", name="cleanShutdown")
    host_key: Optional[PublicKey] = strawberry.field(description="The host's public key", name="hostKey")
    balance: Optional[Currency] = strawberry.field(description="The account's balance as expected by the worker", name="balance")
    drift: Optional[SignedCurrency] = strawberry.field(description="The accumulated drift between the worker's expected balance and the host's actual balance. Used to track if a host is trying to cheat the renter over time.", name="drift")
    owner: Optional[str] = strawberry.field(description="The owner of the account that manages it. This is the id of the worker that maintains the account. | Min length: 1", name="owner")
    requires_sync: Optional[bool] = strawberry.field(description="Whether the account requires a sync with the host. This is usually the case when the host reports insufficient balance for an account that the worker still believes to be funded.", name="requiresSync")


@strawberry.type(description="The hash of a set of UnlockConditions")
class Address(Hash256):
    pass


# @strawberry.type
# class Alert(SiaType):
#     id: Optional[Hash256] = strawberry.field(description="The alert's ID", name="id")
#     severity: Optional[str] = strawberry.field(description="The severity of the alert | Allowed values: info, warning, error, critical", name="severity")
#     message: Optional[str] = strawberry.field(description="The alert's message", name="message")
#     date: Optional[JSON] = strawberry.field(description="Arbitrary data providing additional context for the alert", name="date")
#     timestamp: Optional[datetime.datetime] = strawberry.field(description="The time the alert was created | Format: date-time", name="timestamp")


@strawberry.type
class Attestation(SiaType):
    public_key: Optional[PublicKey] = strawberry.field(name="publicKey")
    key: Optional[str] = strawberry.field(name="key")
    value: Optional[str] = strawberry.field(description="Format: byte", name="value")
    signature: Optional[Signature] = strawberry.field(name="signature")


@strawberry.type
class ContractsConfig(SiaType):
    amount: Optional[int] = strawberry.field(description="The minimum number of contracts to form | Format: uint64", default=0, name="amount")
    period: Optional[int] = strawberry.field(description="The length of a contract's period in blocks (1 block being 10 minutes on average) | Format: uint64", default=0, name="period")
    renew_window: Optional[int] = strawberry.field(description="The number of blocks before the end of a contract that a contract should be renewed | Format: uint64", default=0, name="renewWindow")
    download: Optional[int] = strawberry.field(description="Expected download bandwidth used per period in bytes | Format: uint64", default=0, name="download")
    upload: Optional[int] = strawberry.field(description="Expected upload bandwidth used per period in bytes | Format: uint64", default=0, name="upload")
    storage: Optional[int] = strawberry.field(description="Expected amount of data stored in bytes | Format: uint64", default=0, name="storage")
    prune: Optional[bool] = strawberry.field(description="Whether to automatically prune deleted data from contracts", default=False, name="prune")


@strawberry.type
class HostsConfig(SiaType):
    max_consecutive_scan_failures: Optional[int] = strawberry.field(description="The maximum number of consecutive scan failures before a host is removed from the database | Format: uint64", default=0, name="maxConsecutiveScanFailures")
    max_downtime_hours: Optional[int] = strawberry.field(description="The maximum number of hours a host can be offline before it is removed from the database | Format: uint64", default=0, name="maxDowntimeHours")
    min_protocol_version: Optional[str] = strawberry.field(description="The minimum supported protocol version of a host to be considered good", name="minProtocolVersion")


@strawberry.type
class AutopilotConfig(SiaType):
    enabled: Optional[bool] = strawberry.field(description="Whether the autopilot is enabled", name="enabled")
    contracts: Optional[ContractsConfig] = strawberry.field(name="contracts")
    hosts: Optional[HostsConfig] = strawberry.field(name="hosts")


@strawberry.type
class SiacoinOutput(SiaType):
    value: Optional[Currency] = strawberry.field(description="The amount of Siacoins in the output", name="value")
    address: Optional[Address] = strawberry.field(name="address")


@strawberry.type(description="A storage agreement between a renter and a host.")
class FileContract(SiaType):
    filesize: Optional[int] = strawberry.field(description="The size of the contract in bytes. | Format: uint64", name="filesize")
    file_merkle_root: Optional[Hash256] = strawberry.field(description="The Merkle root of the contract's data.", name="fileMerkleRoot")
    window_start: Optional[BlockHeight] = strawberry.field(description="The block height when the contract's proof window starts.", name="windowStart")
    window_end: Optional[BlockHeight] = strawberry.field(description="The block height when the contract's proof window ends.", name="windowEnd")
    payout: Optional[Currency] = strawberry.field(description="The total payout for the contract.", name="payout")
    valid_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(description="List of outputs created if the contract is successfully fulfilled.", name="validProofOutputs")
    missed_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(description="List of outputs created if the contract is not fulfilled.", name="missedProofOutputs")
    unlock_hash: Optional[Address] = strawberry.field(name="unlockHash")
    revision_number: Optional[RevisionNumber] = strawberry.field(name="revisionNumber")


@strawberry.type(description="Represents a revision to an existing file contract.")
class FileContractRevision(SiaType):
    parent_id: Optional[FileContractID] = strawberry.field(description="The ID of the parent file contract being revised.", name="parentID")
    unlock_conditions: Optional[UnlockConditions] = strawberry.field(description="The conditions required to unlock the contract for revision.", name="unlockConditions")
    filesize: Optional[int] = strawberry.field(description="The size of the file in bytes after the revision. | Format: uint64", name="filesize")
    file_merkle_root: Optional[Hash256] = strawberry.field(description="The updated Merkle root of the file's data.", name="fileMerkleRoot")
    window_start: Optional[BlockHeight] = strawberry.field(description="The block height when the revised proof window starts.", name="windowStart")
    window_end: Optional[BlockHeight] = strawberry.field(description="The block height when the revised proof window ends.", name="windowEnd")
    valid_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(description="Updated outputs if the revised contract is successfully fulfilled.", name="validProofOutputs")
    missed_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(description="Updated outputs if the revised contract is not fulfilled.", name="missedProofOutputs")
    unlock_hash: Optional[Address] = strawberry.field(description="The updated hash of the conditions required to unlock the contract funds.", name="unlockHash")
    revision_number: Optional[RevisionNumber] = strawberry.field(name="revisionNumber")


@strawberry.type
class SiacoinInput(SiaType):
    parent_id: Optional[SiacoinOutputID] = strawberry.field(description="The ID of the output being spent", name="parentID")
    unlock_conditions: Optional[UnlockConditions] = strawberry.field(description="The unlock conditions required to spend the output", name="unlockConditions")


@strawberry.type(description="Represents an input used to spend an unspent Siafund output.")
class SiafundInput(SiaType):
    parent_id: Optional[SiafundOutputID] = strawberry.field(description="The ID of the parent Siafund output being spent.", name="parentID")
    unlock_conditions: Optional[UnlockConditions] = strawberry.field(description="The conditions required to unlock the parent Siafund output.", name="unlockConditions")
    claim_address: Optional[Address] = strawberry.field(description="The address receiving the Siacoin claim generated by the Siafund output.", name="claimAddress")


@strawberry.type(description="Represents an output created to distribute Siafund.")
class SiafundOutput(SiaType):
    value: Optional[int] = strawberry.field(description="The amount of Siafund in the output. | Format: uint64", name="value")
    address: Optional[Address] = strawberry.field(description="The address receiving the Siafund.", name="address")


@strawberry.type(description="Represents a proof of storage for a file contract.")
class StorageProof(SiaType):
    parent_id: Optional[FileContractID] = strawberry.field(description="The ID of the file contract being proven.", name="parentID")
    leaf: Optional[str] = strawberry.field(description="The selected leaf from the Merkle tree of the file's data. | Format: byte", name="leaf")
    proof: Optional[List[Hash256]] = strawberry.field(description="The Merkle proof demonstrating the inclusion of the leaf.", name="proof")


@strawberry.type
class TransactionSignature(SiaType):
    parent_id: Optional[Hash256] = strawberry.field(description="The ID of the transaction being signed", name="parentID")
    public_key_index: Optional[int] = strawberry.field(description="The index of the public key used to sign the transaction | Format: uint64", name="publicKeyIndex")
    timelock: Optional[BlockHeight] = strawberry.field(description="The block height at which the outputs in the transaction can be spent", name="timelock")
    covered_fields: Optional[CoveredFields] = strawberry.field(description="Indicates which fields of the transaction are covered by the signature", name="coveredFields")
    signature: Optional[Signature] = strawberry.field(description="The signature of the transaction", name="signature")


@strawberry.type
class Transaction(SiaType):
    siacoin_inputs: Optional[List[SiacoinInput]] = strawberry.field(description="List of Siacoin inputs used in the transaction.", name="siacoinInputs")
    siacoin_outputs: Optional[List[SiacoinOutput]] = strawberry.field(description="List of Siacoin outputs created by the transaction.", name="siacoinOutputs")
    file_contracts: Optional[List[FileContract]] = strawberry.field(description="List of file contracts created by the transaction.", name="fileContracts")
    file_contract_revisions: Optional[List[FileContractRevision]] = strawberry.field(description="List of revisions to existing file contracts included in the transaction.", name="fileContractRevisions")
    storage_proofs: Optional[List[StorageProof]] = strawberry.field(description="List of storage proofs asserting the storage of data for file contracts.", name="storageProofs")
    siafund_inputs: Optional[List[SiafundInput]] = strawberry.field(description="List of Siafund inputs spent in the transaction.", name="siafundInputs")
    siafund_outputs: Optional[List[SiafundOutput]] = strawberry.field(description="List of Siafund outputs created by the transaction.", name="siafundOutputs")
    miner_fees: Optional[List[Currency]] = strawberry.field(description="List of miner fees included in the transaction.", name="minerFees")
    arbitrary_data: Optional[List[str]] = strawberry.field(description="Arbitrary binary data included in the transaction.", name="arbitraryData")
    signatures: Optional[List[TransactionSignature]] = strawberry.field(description="List of cryptographic signatures verifying the transaction.", name="signatures")


@strawberry.type
class V2FileContract(SiaType):
    capacity: Optional[int] = strawberry.field(description="Format: uint64", name="capacity")
    filesize: Optional[int] = strawberry.field(description="Format: uint64", name="filesize")
    file_merkle_root: Optional[Hash256] = strawberry.field(name="fileMerkleRoot")
    proof_height: Optional[int] = strawberry.field(description="Format: uint64", name="proofHeight")
    expiration_height: Optional[int] = strawberry.field(description="Format: uint64", name="expirationHeight")
    renter_output: Optional[SiacoinOutput] = strawberry.field(name="renterOutput")
    host_output: Optional[SiacoinOutput] = strawberry.field(name="hostOutput")
    missed_host_value: Optional[Currency] = strawberry.field(name="missedHostValue")
    total_collateral: Optional[Currency] = strawberry.field(name="totalCollateral")
    renter_public_key: Optional[PublicKey] = strawberry.field(name="renterPublicKey")
    host_public_key: Optional[PublicKey] = strawberry.field(name="hostPublicKey")
    revision_number: Optional[RevisionNumber] = strawberry.field(name="revisionNumber")
    renter_signature: Optional[Signature] = strawberry.field(name="renterSignature")
    host_signature: Optional[Signature] = strawberry.field(name="hostSignature")


@strawberry.type
class V2FileContractElement(SiaType):
    id: Optional[FileContractID] = strawberry.field(description="The ID of the element", name="id")
    state_element: Optional[StateElement] = strawberry.field(description="The state of the element", name="stateElement")
    v2_file_contract: Optional[V2FileContract] = strawberry.field(name="v2FileContract")


@strawberry.type
class V2FileContractResolution(SiaType):
    parent: Optional[V2FileContractElement] = strawberry.field(name="parent")
    resolution: Optional[JSON] = strawberry.field(name="resolution")


@strawberry.type
class V2FileContractRevision(SiaType):
    parent: Optional[V2FileContractElement] = strawberry.field(name="parent")
    revision: Optional[V2FileContract] = strawberry.field(name="revision")


@strawberry.type
class SatisfiedPolicy(SiaType):
    policy: Optional[JSON] = strawberry.field(name="policy")
    signature: Optional[List[Signature]] = strawberry.field(name="signature")
    preimages: Optional[List[str]] = strawberry.field(name="preimages")


@strawberry.type
class SiacoinElement(SiaType):
    id: Optional[SiacoinOutputID] = strawberry.field(description="The ID of the element", name="id")
    state_element: Optional[StateElement] = strawberry.field(description="The state of the element", name="stateElement")
    siafund_output: Optional[SiacoinOutput] = strawberry.field(description="The output of the element", name="siafundOutput")
    maturity_height: Optional[BlockHeight] = strawberry.field(description="The block height when the output matures", name="maturityHeight")


@strawberry.type
class V2SiacoinInput(SiaType):
    parent: Optional[SiacoinElement] = strawberry.field(name="parent")
    satisfied_policy: Optional[SatisfiedPolicy] = strawberry.field(name="satisfiedPolicy")


@strawberry.type
class SiafundElement(SiaType):
    id: Optional[SiafundOutputID] = strawberry.field(description="The ID of the element", name="id")
    state_element: Optional[StateElement] = strawberry.field(description="The state of the element", name="stateElement")
    siafund_output: Optional[SiafundOutput] = strawberry.field(description="The output of the element", name="siafundOutput")
    claim_start: Optional[Currency] = strawberry.field(description="value of SiafundTaxRevenue when element was created", name="claimStart")


@strawberry.type
class V2SiafundInput(SiaType):
    parent: Optional[SiafundElement] = strawberry.field(name="parent")
    claim_address: Optional[Address] = strawberry.field(name="claimAddress")
    satisfied_policy: Optional[SatisfiedPolicy] = strawberry.field(name="satisfiedPolicy")


@strawberry.type
class V2Transaction(SiaType):
    siacoin_inputs: Optional[List[V2SiacoinInput]] = strawberry.field(name="siacoinInputs")
    siacoin_outputs: Optional[List[SiacoinOutput]] = strawberry.field(name="siacoinOutputs")
    siafund_inputs: Optional[List[V2SiafundInput]] = strawberry.field(name="siafundInputs")
    siafund_outputs: Optional[List[SiafundOutput]] = strawberry.field(name="siafundOutputs")
    file_contracts: Optional[List[V2FileContract]] = strawberry.field(name="fileContracts")
    file_contract_revisions: Optional[List[V2FileContractRevision]] = strawberry.field(name="fileContractRevisions")
    file_contract_resolutions: Optional[List[V2FileContractResolution]] = strawberry.field(name="fileContractResolutions")
    attestations: Optional[List[Attestation]] = strawberry.field(name="attestations")
    arbitrary_data: Optional[List[str]] = strawberry.field(name="arbitraryData")
    new_foundation_address: Optional[Address] = strawberry.field(name="newFoundationAddress")
    miner_fee: Optional[Currency] = strawberry.field(name="minerFee")


@strawberry.type
class V2BlockData(SiaType):
    height: Optional[BlockHeight] = strawberry.field(description="The height of the block", name="height")
    commitment: Optional[Hash256] = strawberry.field(name="commitment")
    transactions: Optional[List[V2Transaction]] = strawberry.field(name="transactions")



@strawberry.type(description="A unique identifier for a block")
class BlockID(Hash256):
    pass

@strawberry.type
class Block(SiaType):
    parent_id: Optional[BlockID] = strawberry.field(description="The ID of the parent block", name="parentID")
    nonce: Optional[int] = strawberry.field(description="The nonce used to mine the block | Format: uint64", name="nonce")
    timestamp: Optional[datetime.datetime] = strawberry.field(description="The time the block was mined | Format: date-time", name="timestamp")
    miner_payouts: Optional[List[SiacoinOutput]] = strawberry.field(name="minerPayouts")
    transactions: Optional[List[Transaction]] = strawberry.field(name="transactions")
    v2: Optional[V2BlockData] = strawberry.field(name="v2")


@strawberry.type
class BucketPolicy(SiaType):
    public_read_access: Optional[bool] = strawberry.field(description="Indicates if the bucket is publicly readable", name="publicReadAccess")

@strawberry.type
class Bucket(SiaType):
    name: Optional[BucketName] = strawberry.field(name="name")
    policy: Optional[BucketPolicy] = strawberry.field(name="policy") # change to JSON if it creates problem
    created_at: Optional[datetime.datetime] = strawberry.field(description="The time the bucket was created | Format: date-time", name="createdAt")


@strawberry.type
class BuildState(SiaType):
    build_time: Optional[datetime.datetime] = strawberry.field(description="The build time of the build | Format: date-time", name="buildTime")
    commit: Optional[str] = strawberry.field(description="The commit hash of the build", name="commit")
    version: Optional[str] = strawberry.field(description="The version of the build", name="version")
    os: Optional[str] = strawberry.field(description="The operating system of the build", name="os")


@strawberry.type
class ChainIndex(SiaType):
    height: Optional[BlockHeight] = strawberry.field(description="The height of the block in the blockchain", name="height")
    id: Optional[BlockID] = strawberry.field(description="The ID of the block", name="id")


@strawberry.type
class GougingSettings(SiaType):
    max_rpc_price: Optional[Currency] = strawberry.field(description="The maximum base price a host can charge per RPC", name="maxRPCPrice")
    max_contract_price: Optional[Currency] = strawberry.field(description="The maximum price a host can charge for a contract formation", name="maxContractPrice")
    max_download_price: Optional[Currency] = strawberry.field(description="The maximum price a host can charge for downloading in hastings / byte", name="maxDownloadPrice")
    max_upload_price: Optional[Currency] = strawberry.field(description="The maximum price a host can charge for uploading in hastings / byte", name="maxUploadPrice")
    max_storage_price: Optional[Currency] = strawberry.field(description="The maximum price a host can charge for storage in hastings / byte / block", name="maxStoragePrice")
    host_block_height_leeway: Optional[int] = strawberry.field(description="The number of blocks a host's chain's height can diverge from our own before we stop using it | Format: uint32", name="hostBlockHeightLeeway")
    min_price_table_validity: Optional[int] = strawberry.field(description="The time a host's price table should be valid after acquiring it in milliseconds | Format: uint64", name="minPriceTableValidity")
    min_account_expiry: Optional[int] = strawberry.field(description="The minimum amount of time an account on a host can be idle for before expiring | Format: uint64", name="minAccountExpiry")
    min_max_ephemeral_account_balance: Optional[Currency] = strawberry.field(description="The minimum max balance a host should allow us to fund an account with", name="minMaxEphemeralAccountBalance")


@strawberry.type
class ConfigRecommendation(SiaType):
    gouging_settings: Optional[GougingSettings] = strawberry.field(name="gougingSettings")


@strawberry.type
class ConsensusState(SiaType):
    block_height: Optional[BlockHeight] = strawberry.field(description="The current block height", name="blockHeight")
    last_block_time: Optional[datetime.datetime] = strawberry.field(description="The time of the last block | Format: date-time", name="lastBlockTime")
    synced: Optional[bool] = strawberry.field(description="Whether the node is synced with the network", name="synced")


@strawberry.type
class ContractLockID(SiaType):
    lock_id: Optional[int] = strawberry.field(description="The ID of the lock | Format: uint64 | Example: 12", name="lockID")


@strawberry.type
class ContractSpending(SiaType):
    deletions: Optional[Currency] = strawberry.field(description="Total amount spent on sector deletions", name="deletions")
    fund_account: Optional[Currency] = strawberry.field(description="Total amount spent on funding ephemeral accounts", name="fundAccount")
    sector_roots: Optional[Currency] = strawberry.field(description="Total amount spent on listing sector roots", name="sectorRoots")
    uploads: Optional[Currency] = strawberry.field(description="Total amount spent on storing sectors", name="uploads")




@strawberry.type
class ContractMetadata(SiaType):
    id: Optional[FileContractID] = strawberry.field(description="The unique identifier for the file contract.", name="id")
    host_key: Optional[PublicKey] = strawberry.field(description="The public key of the host.", name="hostKey")
    v2: Optional[bool] = strawberry.field(description="Indicates if the contract is a V2 contract.", name="v2")
    proof_height: Optional[BlockHeight] = strawberry.field(description="The height at which the storage proof needs to be submitted", name="proofHeight")
    renewed_from: Optional[FileContractID] = strawberry.field(description="The ID of the contract this one was renewed from", name="renewedFrom")
    revision_height: Optional[BlockHeight] = strawberry.field(description="The block height of the latest revision", name="revisionHeight")
    revision_number: Optional[RevisionNumber] = strawberry.field(description="The current revision number of the contract", name="revisionNumber")
    size: Optional[int] = strawberry.field(description="The size of the contract in bytes | Format: uint64", name="size")
    start_height: Optional[BlockHeight] = strawberry.field(description="The block height at which the contract created", name="startHeight")
    state: Optional[str] = strawberry.field(description="The state of the contract | Allowed values: pending, active, complete, failed", name="state")
    usability: Optional[str] = strawberry.field(description="The usability status of the contract | Allowed values: good, bad", name="usability")
    window_start: Optional[BlockHeight] = strawberry.field(description="The block height when the contract's proof window starts.", name="windowStart")
    window_end: Optional[BlockHeight] = strawberry.field(description="The block height when the contract's proof window ends.", name="windowEnd")
    contract_price: Optional[Currency] = strawberry.field(description="The price of forming the contract.", name="contractPrice")
    initial_renter_funds: Optional[Currency] = strawberry.field(description="The initial funds provided by the renter.", name="initialRenterFunds")
    spending: Optional[ContractSpending] = strawberry.field(description="Costs and spending details of the contract.", name="spending")
    archival_reason: Optional[str] = strawberry.field(description="The reason for archiving the contract, if applicable. | Allowed values: renewed, removed, hostpruned", name="archivalReason")
    renewed_to: Optional[FileContractID] = strawberry.field(description="The ID of the contract this one was renewed to, if applicable.", name="renewedTo")


@strawberry.type
class Revision(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    missed_host_value: Optional[Currency] = strawberry.field(name="missedHostValue")
    renter_funds: Optional[Currency] = strawberry.field(name="renterFunds")
    revision_number: Optional[RevisionNumber] = strawberry.field(name="revisionNumber")
    size: Optional[int] = strawberry.field(description="The size of the contract in bytes | Format: uint64", name="size")


@strawberry.type
class Contract(ContractMetadata):
    revision: Optional[Revision] = strawberry.field(name="revision")

@strawberry.type
class ContractMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="Format: date-time", name="timestamp")
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    remaining_collateral: Optional[Currency] = strawberry.field(name="remainingCollateral")
    remaining_funds: Optional[Currency] = strawberry.field(name="remainingFunds")
    revision_number: Optional[RevisionNumber] = strawberry.field(name="revisionNumber")
    delete_spending: Optional[Currency] = strawberry.field(name="deleteSpending")
    fund_account_spending: Optional[Currency] = strawberry.field(name="fundAccountSpending")
    sector_roots_spending: Optional[Currency] = strawberry.field(name="sectorRootsSpending")
    upload_spending: Optional[Currency] = strawberry.field(name="uploadSpending")


@strawberry.type
class ContractPruneMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="Format: date-time", name="timestamp")
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    host_version: Optional[str] = strawberry.field(name="hostVersion")
    pruned: Optional[int] = strawberry.field(description="Format: uint64", name="pruned")
    remaining: Optional[int] = strawberry.field(description="Format: uint64", name="remaining")
    duration: Optional[int] = strawberry.field(description="Duration in nanoseconds | Format: int64", name="duration")


@strawberry.type
class ContractSize(SiaType):
    prunable: Optional[int] = strawberry.field(description="The amount of data that can be pruned from a contract | Format: uint64", name="prunable")
    size: Optional[int] = strawberry.field(description="The total size of a contract | Format: uint64", name="size")



@strawberry.type(description="A transaction or other event that affects the wallet including miner payouts, siafund claims, and file contract payouts.")
class Event(SiaType):
    id: Optional[Hash256] = strawberry.field(description="The event's ID", name="id")
    index: Optional[ChainIndex] = strawberry.field(description="Information about the block that triggered the creation of this event", name="index")
    confirmations: Optional[int] = strawberry.field(description="The number of blocks on top of the block that triggered the creation of this event | Format: uint64", name="confirmations")
    type: Optional[str] = strawberry.field(description="The type of the event | Allowed values: miner, foundation, siafundClaim, v1Transaction, v1ContractResolution, v2Transaction, v2ContractResolution", name="type")
    data: Optional[JSON] = strawberry.field(name="data")
    maturity_height: Optional[BlockHeight] = strawberry.field(description="The block height at which the payout matures.", name="maturityHeight")
    timestamp: Optional[datetime.datetime] = strawberry.field(description="The time the event was created | Format: date-time", name="timestamp")
    relevant: Optional[List[Address]] = strawberry.field(name="relevant")


@strawberry.type
class RedundancySettings(SiaType):
    min_shards: Optional[int] = strawberry.field(description="The number of data shards a piece of an object gets erasure-coded into | Minimum: 1 | Format: int32", default=10, name="minShards")
    total_shards: Optional[int] = strawberry.field(description="The number of total data shards a piece of an object gets erasure-coded into | Minimum: 2 | Format: int32", default=30, name="totalShards")


@strawberry.type
class GougingParams(SiaType):
    consensus_state: Optional[ConsensusState] = strawberry.field(name="consensusState")
    gouging_settings: Optional[GougingSettings] = strawberry.field(name="gougingSettings")
    redundancy_settings: Optional[RedundancySettings] = strawberry.field(name="redundancySettings")


@strawberry.type
class Pin(SiaType):
    pinned: Optional[bool] = strawberry.field(description="Whether pin is enabled", name="pinned")
    value: Optional[float] = strawberry.field(description="The value of the underlying currency to which the setting is pinned | Format: float64", name="value")


@strawberry.type
class GougingSettingsPins(SiaType):
    max_download: Optional[Pin] = strawberry.field(name="maxDownload")
    max_storage: Optional[Pin] = strawberry.field(name="maxStorage")
    max_upload: Optional[Pin] = strawberry.field(name="maxUpload")


@strawberry.type
class HostGougingBreakdown(SiaType):
    download_err: Optional[str] = strawberry.field(description="Error message related to download gouging checks.", name="downloadErr")
    gouging_err: Optional[str] = strawberry.field(description="Error message related to general gouging checks.", name="gougingErr")
    prune_err: Optional[str] = strawberry.field(description="Error message related to pruning checks.", name="pruneErr")
    upload_err: Optional[str] = strawberry.field(description="Error message related to upload gouging checks.", name="uploadErr")


@strawberry.type
class HostScoreBreakdown(SiaType):
    age: Optional[float] = strawberry.field(description="Score contribution based on the host's age. | Format: float", name="age")
    collateral: Optional[float] = strawberry.field(description="Score contribution based on the host's collateral amount. | Format: float", name="collateral")
    interactions: Optional[float] = strawberry.field(description="Score contribution based on successful interactions. | Format: float", name="interactions")
    storage_remaining: Optional[float] = strawberry.field(description="Score contribution based on remaining storage capacity. | Format: float", name="storageRemaining")
    uptime: Optional[float] = strawberry.field(description="Score contribution based on host uptime. | Format: float", name="uptime")
    version: Optional[float] = strawberry.field(description="Score contribution based on the host's software version. | Format: float", name="version")
    prices: Optional[float] = strawberry.field(description="Score contribution based on pricing metrics. | Format: float", name="prices")


@strawberry.type
class HostUsabilityBreakdown(SiaType):
    blocked: Optional[bool] = strawberry.field(description="Indicates if the host is blocked.", name="blocked")
    offline: Optional[bool] = strawberry.field(description="Indicates if the host is offline.", name="offline")
    low_max_duration: Optional[bool] = strawberry.field(description="Indicates if the host has a low maximum contract duration.", name="lowMaxDuration")
    low_score: Optional[bool] = strawberry.field(description="Indicates if the host has a low score.", name="lowScore")
    redundant_ip: Optional[bool] = strawberry.field(description="Indicates if the host's IP address is redundant.", name="redundantIP")
    gouging: Optional[bool] = strawberry.field(description="Indicates if the host is gouging prices.", name="gouging")
    not_accepting_contracts: Optional[bool] = strawberry.field(description="Indicates if the host is not accepting new contracts.", name="notAcceptingContracts")
    not_announced: Optional[bool] = strawberry.field(description="Indicates if the host has not been announced on the network.", name="notAnnounced")
    not_completing_scan: Optional[bool] = strawberry.field(description="Indicates if the host is failing to complete scans.", name="notCompletingScan")


@strawberry.type
class HostInteractions(SiaType):
    total_scans: Optional[int] = strawberry.field(description="The total number of scans performed on the host. | Format: uint64", name="totalScans")
    last_scan: Optional[datetime.datetime] = strawberry.field(description="Timestamp of the last scan performed. | Format: date-time", name="lastScan")
    last_scan_success: Optional[bool] = strawberry.field(description="Indicates whether the last scan was successful.", name="lastScanSuccess")
    lost_sectors: Optional[int] = strawberry.field(description="Number of sectors lost since the last reporting period. | Format: uint64", name="lostSectors")
    second_to_last_scan_success: Optional[bool] = strawberry.field(description="Indicates whether the second-to-last scan was successful.", name="secondToLastScanSuccess")
    uptime: Optional[str] = strawberry.field(description="Total uptime duration of the host. | Format: duration", name="uptime")
    downtime: Optional[str] = strawberry.field(description="Total downtime duration of the host. | Format: duration", name="downtime")
    successful_interactions: Optional[float] = strawberry.field(description="The number of successful interactions with the host. | Format: float", name="successfulInteractions")
    failed_interactions: Optional[float] = strawberry.field(description="The number of failed interactions with the host. | Format: float", name="failedInteractions")


@strawberry.type(description="A detailed price table containing cost and configuration values for a host.")
class HostPriceTable(SiaType):
    uid: Optional[SettingsID] = strawberry.field(description="Unique specifier that identifies this price table.", name="uid")
    validity: Optional[int] = strawberry.field(description="Duration (in nanoseconds) for which the host guarantees these prices are valid. | Format: int64 | Example: 3600000000000", name="validity")
    hostblockheight: Optional[BlockHeight] = strawberry.field(description="The host's current block height.", name="hostblockheight")
    updatepricetablecost: Optional[Currency] = strawberry.field(description="The cost to fetch a new price table from the host.", name="updatepricetablecost")
    accountbalancecost: Optional[Currency] = strawberry.field(description="The cost to fetch the balance of an ephemeral account.", name="accountbalancecost")
    fundaccountcost: Optional[Currency] = strawberry.field(description="The cost to fund an ephemeral account on the host.", name="fundaccountcost")
    latestrevisioncost: Optional[Currency] = strawberry.field(description="The cost to retrieve the latest revision of a contract.", name="latestrevisioncost")
    subscriptionmemorycost: Optional[Currency] = strawberry.field(description="The cost of storing a byte of data for a subscription period.", name="subscriptionmemorycost")
    subscriptionnotificationcost: Optional[Currency] = strawberry.field(description="The cost of a single notification on top of bandwidth charges.", name="subscriptionnotificationcost")
    initbasecost: Optional[Currency] = strawberry.field(description="The base cost incurred when starting an MDM program.", name="initbasecost")
    memorytimecost: Optional[Currency] = strawberry.field(description="The cost per byte per time for the memory consumed by a program.", name="memorytimecost")
    downloadbandwidthcost: Optional[Currency] = strawberry.field(description="The cost per byte for download bandwidth.", name="downloadbandwidthcost")
    uploadbandwidthcost: Optional[Currency] = strawberry.field(description="The cost per byte for upload bandwidth.", name="uploadbandwidthcost")
    dropsectorsbasecost: Optional[Currency] = strawberry.field(description="The base cost of performing a DropSectors instruction.", name="dropsectorsbasecost")
    dropsectorsunitcost: Optional[Currency] = strawberry.field(description="The unit cost per sector for performing a DropSectors instruction.", name="dropsectorsunitcost")
    hassectorbasecost: Optional[Currency] = strawberry.field(description="The cost for executing the HasSector command.", name="hassectorbasecost")
    readbasecost: Optional[Currency] = strawberry.field(description="The base cost of performing a Read instruction.", name="readbasecost")
    readlengthcost: Optional[Currency] = strawberry.field(description="The cost per byte read during a Read instruction.", name="readlengthcost")
    renewcontractcost: Optional[Currency] = strawberry.field(description="The cost for renewing a contract.", name="renewcontractcost")
    revisionbasecost: Optional[Currency] = strawberry.field(description="The base cost for performing a Revision command.", name="revisionbasecost")
    swapsectorcost: Optional[Currency] = strawberry.field(description="The cost of swapping two full sectors by root.", name="swapsectorcost")
    writebasecost: Optional[Currency] = strawberry.field(description="The base cost per write operation.", name="writebasecost")
    writelengthcost: Optional[Currency] = strawberry.field(description="The cost per byte written during a Write instruction.", name="writelengthcost")
    writestorecost: Optional[Currency] = strawberry.field(description="The cost per byte/block of additional storage.", name="writestorecost")
    txnfeeminrecommended: Optional[Currency] = strawberry.field(description="The minimum recommended transaction fee.", name="txnfeeminrecommended")
    txnfeemaxrecommended: Optional[Currency] = strawberry.field(description="The maximum recommended transaction fee.", name="txnfeemaxrecommended")
    contractprice: Optional[Currency] = strawberry.field(description="The additional fee charged by the host to form or renew a contract.", name="contractprice")
    collateralcost: Optional[Currency] = strawberry.field(description="The cost per byte for the collateral promised by the host.", name="collateralcost")
    maxcollateral: Optional[Currency] = strawberry.field(description="The maximum amount of collateral the host is willing to put into a contract.", name="maxcollateral")
    maxduration: Optional[int] = strawberry.field(description="Maximum duration (in blocks) for which the host is willing to form a contract. | Format: uint64 | Example: 14400", name="maxduration")
    windowsize: Optional[int] = strawberry.field(description="Minimum time (in blocks) requested for the renew window of a contract. | Format: uint64 | Example: 1000", name="windowsize")
    registryentriesleft: Optional[int] = strawberry.field(description="The remaining number of registry entries available on the host. | Format: uint64 | Example: 5000", name="registryentriesleft")
    registryentriestotal: Optional[int] = strawberry.field(description="The total number of registry entries available on the host. | Format: uint64 | Example: 10000", name="registryentriestotal")
    expiry: Optional[datetime.datetime] = strawberry.field(name="expiry", default=None)


@strawberry.type
class HostSettings(SiaType):
    accepting_contracts: Optional[bool] = strawberry.field(description="Whether the host is accepting new contracts", name="acceptingContracts")
    max_download_batch_size: Optional[int] = strawberry.field(description="Maximum allowed download batch size | Format: uint64", name="maxDownloadBatchSize")
    max_duration: Optional[int] = strawberry.field(description="Maximum allowed contract duration | Format: uint64", name="maxDuration")
    max_revise_batch_size: Optional[int] = strawberry.field(description="Maximum allowed revision batch size | Format: uint64", name="maxReviseBatchSize")
    net_address: Optional[str] = strawberry.field(description="Network address of the host", name="netAddress")
    remaining_storage: Optional[int] = strawberry.field(description="Amount of storage the host has remaining | Format: uint64", name="remainingStorage")
    sector_size: Optional[int] = strawberry.field(description="Size of a storage sector | Format: uint64", name="sectorSize")
    total_storage: Optional[int] = strawberry.field(description="Total amount of storage space | Format: uint64", name="totalStorage")
    address: Optional[Address] = strawberry.field(name="address")
    window_size: Optional[int] = strawberry.field(description="Size of the proof window | Format: uint64", name="windowSize")
    collateral: Optional[Currency] = strawberry.field(name="collateral")
    max_collateral: Optional[Currency] = strawberry.field(name="maxCollateral")
    base_rpc_price: Optional[Currency] = strawberry.field(name="baseRPCPrice")
    contract_price: Optional[Currency] = strawberry.field(name="contractPrice")
    download_bandwidth_price: Optional[Currency] = strawberry.field(name="downloadBandwidthPrice")
    sector_access_price: Optional[Currency] = strawberry.field(name="sectorAccessPrice")
    storage_price: Optional[Currency] = strawberry.field(name="storagePrice")
    upload_bandwidth_price: Optional[Currency] = strawberry.field(name="uploadBandwidthPrice")
    ephemeral_account_expiry: Optional[int] = strawberry.field(description="Duration before an ephemeral account expires | Format: int64", name="ephemeralAccountExpiry")
    max_ephemeral_account_balance: Optional[Currency] = strawberry.field(name="maxEphemeralAccountBalance")
    revision_number: Optional[RevisionNumber] = strawberry.field(name="revisionNumber")
    version: Optional[str] = strawberry.field(description="Version of the host software", name="version")
    release: Optional[str] = strawberry.field(description="Release tag of the host software | Example: hostd 1.0.0", name="release")
    siamux_port: Optional[str] = strawberry.field(description="Port used for siamux connections", name="siamuxPort")


@strawberry.type
class HostPrices(SiaType):
    contract_price: Optional[Currency] = strawberry.field(name="contractPrice")
    collateral: Optional[Currency] = strawberry.field(name="collateral")
    storage_price: Optional[Currency] = strawberry.field(name="storagePrice")
    ingress_price: Optional[Currency] = strawberry.field(name="ingressPrice")
    egress_price: Optional[Currency] = strawberry.field(name="egressPrice")
    tip_height: Optional[int] = strawberry.field(description="The height at which the prices were last updated | Format: uint64", name="tipHeight")
    valid_until: Optional[datetime.datetime] = strawberry.field(description="Format: date-time", name="validUntil")
    signature: Optional[Signature] = strawberry.field(name="signature")


@strawberry.type
class HostV2Settings(SiaType):
    protocol_version: Optional[SemVer] = strawberry.field(name="protocolVersion")
    release: Optional[str] = strawberry.field(description="Release tag of the host software | Example: hostd 1.0.0", name="release")
    wallet_address: Optional[Address] = strawberry.field(name="walletAddress")
    accepting_contracts: Optional[bool] = strawberry.field(description="Whether the host is accepting new contracts", name="acceptingContracts")
    max_collateral: Optional[Currency] = strawberry.field(name="maxCollateral")
    max_contract_duration: Optional[int] = strawberry.field(description="Maximum allowed contract duration | Format: uint64", name="maxContractDuration")
    remaining_storage: Optional[int] = strawberry.field(description="Amount of storage the host has remaining | Format: uint64", name="remainingStorage")
    total_storage: Optional[int] = strawberry.field(description="Total amount of storage space | Format: uint64", name="totalStorage")
    prices: Optional[HostPrices] = strawberry.field(name="prices")


@strawberry.type
class HostChecks(SiaType):
    gouging_breakdown: Optional[HostGougingBreakdown] = strawberry.field(name="gougingBreakdown")
    score_breakdown: Optional[HostScoreBreakdown] = strawberry.field(name="scoreBreakdown")
    usability_breakdown: Optional[HostUsabilityBreakdown] = strawberry.field(name="usabilityBreakdown")


@strawberry.type
class Host(SiaType):
    known_since: Optional[datetime.datetime] = strawberry.field(description="The time the host was first seen | Format: date-time", name="knownSince")
    last_announcement: Optional[datetime.datetime] = strawberry.field(description="The time the host last announced itself | Format: date-time", name="lastAnnouncement")
    public_key: Optional[PublicKey] = strawberry.field(name="publicKey")
    net_address: Optional[str] = strawberry.field(description="The address of the host | Example: foo.bar:1234", name="netAddress")
    price_table: Optional[HostPriceTable] = strawberry.field(name="priceTable")
    settings: Optional[HostSettings] = strawberry.field(name="settings")
    v2_settings: Optional[HostV2Settings] = strawberry.field(name="v2Settings")
    interactions: Optional[HostInteractions] = strawberry.field(name="interactions")
    scanned: Optional[bool] = strawberry.field(description="Whether the host has been scanned", name="scanned")
    blocked: Optional[bool] = strawberry.field(description="Whether the host is blocked", name="blocked")
    checks: Optional[HostChecks] = strawberry.field(name="checks")
    stored_data: Optional[int] = strawberry.field(description="The amount of data stored on the host in bytes | Format: uint64", name="storedData")
    v2_siamux_addresses: Optional[List[str]] = strawberry.field(name="v2SiamuxAddresses")


@strawberry.type
class HostInfo(SiaType):
    public_key: Optional[PublicKey] = strawberry.field(name="publicKey")
    siamux_addr: Optional[str] = strawberry.field(description="The address of the host | Example: foo.bar:1234", name="siamuxAddr")
    v2_siamux_addresses: Optional[List[str]] = strawberry.field(name="v2SiamuxAddresses")


@strawberry.type
class MemoryStatus(SiaType):
    available: Optional[int] = strawberry.field(description="The amount of remaining memory currently available in bytes | Format: uint64 | Example: 83886080", name="available")
    total: Optional[int] = strawberry.field(description="The total amount of memory available in bytes | Minimum: 1 | Format: uint64 | Example: 1073741824", name="total")


@strawberry.type
class MultipartCompletedPart(SiaType):
    part_number: Optional[int] = strawberry.field(description="The number of this part", name="partNumber")
    e_tag: Optional[ETag] = strawberry.field(name="eTag")


@strawberry.type
class MultipartListPartItem(SiaType):
    part_number: Optional[int] = strawberry.field(description="The number of this part", name="partNumber")
    last_modified: Optional[datetime.datetime] = strawberry.field(description="When this part was last modified | Format: date-time", name="lastModified")
    e_tag: Optional[ETag] = strawberry.field(name="eTag")
    size: Optional[int] = strawberry.field(description="The size of this part in bytes | Format: int64", name="size")


@strawberry.type
class MultipartUpload(SiaType):
    bucket: Optional[str] = strawberry.field(description="The name of the bucket", name="bucket")
    encryption_key: Optional[EncryptionKey] = strawberry.field(name="encryptionKey")
    key: Optional[str] = strawberry.field(description="The key of the object", name="key")
    upload_id: Optional[UploadID] = strawberry.field(description="The ID of the multipart upload", name="uploadID")
    created_at: Optional[datetime.datetime] = strawberry.field(description="When the upload was created | Format: date-time", name="createdAt")


@strawberry.type
class Network(SiaType):
    name: Optional[str] = strawberry.field(description="The name of the network", name="name")
    initial_coinbase: Optional[Currency] = strawberry.field(description="The initial coinbase reward", name="initialCoinbase")
    minimum_coinbase: Optional[Currency] = strawberry.field(description="The minimum coinbase reward", name="minimumCoinbase")
    initial_target: Optional[BlockID] = strawberry.field(description="The initial target", name="initialTarget")
    block_interval: Optional[int] = strawberry.field(description="The block interval | Format: uint64", default=600000000000, name="blockInterval")
    maturity_delay: Optional[int] = strawberry.field(description="The maturity delay | Format: uint64", default=144, name="maturityDelay")
    hardfork_dev_addr: Optional[JSON] = strawberry.field(name="hardforkDevAddr")
    hardfork_tax: Optional[JSON] = strawberry.field(name="hardforkTax")
    hardfork_storage_proof: Optional[JSON] = strawberry.field(name="hardforkStorageProof")
    hardfork_oak: Optional[JSON] = strawberry.field(name="hardforkOak")
    hardfork_asic: Optional[JSON] = strawberry.field(name="hardforkASIC")
    hardfork_foundation: Optional[JSON] = strawberry.field(name="hardforkFoundation")
    hardfork_v2: Optional[JSON] = strawberry.field(name="hardforkV2")


@strawberry.type
class ObjectMetadata(SiaType):
    bucket: Optional[BucketName] = strawberry.field(name="bucket")
    etag: Optional[ETag] = strawberry.field(description="The ETag of the object", name="etag")
    health: Optional[float] = strawberry.field(description="The health of the object | Format: float", name="health")
    mod_time: Optional[datetime.datetime] = strawberry.field(description="When the object was last modified | Format: date-time", name="modTime")
    key: Optional[str] = strawberry.field(description="The key of the object", name="key")
    size: Optional[int] = strawberry.field(description="The size of the object in bytes | Format: int64", name="size")
    mime_type: Optional[str] = strawberry.field(description="The MIME type of the object", name="mimeType")


@strawberry.type(description="User-defined metadata about an object provided through X-Sia-Meta- headers")
class ObjectUserMetadata(SiaType):
    _dummy: Optional[str] = strawberry.field(default=None)


@strawberry.type(description="A slab of data to migrate")
class Slab(SiaType):
    health: Optional[float] = strawberry.field(description="Minimum: 0 | Maximum: 1 | Format: float", name="health")
    encryption_key: Optional[EncryptionKey] = strawberry.field(description="The encryption key used to encrypt the slab's shards", name="encryptionKey")
    min_shards: Optional[int] = strawberry.field(description="The number of data shards the slab is split into | Minimum: 1 | Maximum: 255 | Format: uint8", name="minShards")


@strawberry.type(description="A contiguous region within a slab")
class SlabSlice(SiaType):
    slab: Optional[Slab] = strawberry.field(name="slab")
    offset: Optional[int] = strawberry.field(description="Format: uint32", name="offset")
    limit: Optional[int] = strawberry.field(description="Format: uint32", name="limit")


@strawberry.type
class Object(SiaType):
    metadata: Optional[ObjectUserMetadata] = strawberry.field(name="metadata")
    encryption_key: Optional[EncryptionKey] = strawberry.field(name="encryptionKey")
    slabs: Optional[List[SlabSlice]] = strawberry.field(name="slabs")


# @strawberry.type
# class Object(SiaType):
#     metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")
#     object_metadata: Optional[ObjectMetadata] = strawberry.field(name="objectMetadata")
#     # The underlying object data is not exposed directly.
    

@strawberry.type
class PackedSlab(SiaType):
    buffer_id: Optional[int] = strawberry.field(description="ID of the buffer containing the slab | Format: uint", name="bufferID")
    data: Optional[str] = strawberry.field(description="The slab data | Format: binary", name="data")
    encryption_key: Optional[EncryptionKey] = strawberry.field(name="encryptionKey")


@strawberry.type
class PinnedSettings(SiaType):
    currency: Optional[Currency] = strawberry.field(name="currency")
    threshold: Optional[float] = strawberry.field(description="A percentage between 0 and 1 that determines when the pinned settings are updated based on the exchange rate at the time | Format: float64", name="threshold")
    gouging_settings_pins: Optional[GougingSettingsPins] = strawberry.field(name="gougingSettingsPins")



@strawberry.type
class S3Settings(SiaType):
    access_key_id: Optional[str] = strawberry.field(description="S3 access key ID", name="accessKeyID")
    secret_access_key: Optional[str] = strawberry.field(description="S3 secret access key", name="secretAccessKey")
    disable_auth: Optional[bool] = strawberry.field(description="Whether to disable S3 authentication", name="disableAuth")


# @strawberry.type
# class S3Settings(SiaType):
#     authentication: Optional[S3AuthenticationSettings] = strawberry.field(name="authentication")


@strawberry.type
class SlabBuffer(SiaType):
    complete: Optional[bool] = strawberry.field(description="Whether the slab buffer is complete and ready to upload", name="complete")
    filename: Optional[str] = strawberry.field(description="Name of the buffer on disk", name="filename")
    size: Optional[int] = strawberry.field(description="Size of the buffer | Format: int64", name="size")
    max_size: Optional[int] = strawberry.field(description="Maximum size of the buffer | Format: int64", name="maxSize")
    locked: Optional[bool] = strawberry.field(description="Whether the slab buffer is locked for uploading", name="locked")


@strawberry.type
class UploadPackingSettings(SiaType):
    enabled: Optional[bool] = strawberry.field(description="Whether upload packing is enabled", name="enabled")
    slab_buffer_max_size_soft: Optional[int] = strawberry.field(description="Maximum size for slab buffers | Format: int64", name="slabBufferMaxSizeSoft")


@strawberry.type
class UploadSettings(SiaType):
    packing: Optional[UploadPackingSettings] = strawberry.field(name="packing")
    redundancy: Optional[RedundancySettings] = strawberry.field(name="redundancy")


@strawberry.type
class UploadedSector(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    root: Optional[Hash256] = strawberry.field(name="root")


@strawberry.type
class UploadedPackedSlab(SiaType):
    buffer_id: Optional[int] = strawberry.field(description="ID of the buffer containing the slab | Format: uint", name="bufferID")
    shards: Optional[List[UploadedSector]] = strawberry.field(name="shards")


@strawberry.type
class WalletMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(description="Format: date-time", name="timestamp")
    confirmed: Optional[Currency] = strawberry.field(name="confirmed")
    spendable: Optional[Currency] = strawberry.field(name="spendable")
    unconfirmed: Optional[Currency] = strawberry.field(name="unconfirmed")
    immature: Optional[Currency] = strawberry.field(name="immature")


@strawberry.type
class Webhook(SiaType):
    module: Optional[str] = strawberry.field(description="The module this webhook belongs to | Allowed values: alerts", name="module")
    event: Optional[str] = strawberry.field(description="The event type this webhook listens for | Allowed values: dismiss, register", name="event")
    url: Optional[str] = strawberry.field(description="The URL to send webhook events to | Example: https://foo.com:8000/api/events", name="url")
    headers: Optional[JSON] = strawberry.field(description="Custom headers to include in webhook requests", name="headers")


@strawberry.type
class WebhookEvent(SiaType):
    module: Optional[str] = strawberry.field(description="The module that triggered the event | Allowed values: alerts", name="module")
    event: Optional[str] = strawberry.field(description="The type of event that occurred | Allowed values: dismiss, register", name="event")
    data: Optional[JSON] = strawberry.field(description="Event-specific data payload", name="data")


@strawberry.type
class WebhookQueueInfo(SiaType):
    url: Optional[str] = strawberry.field(description="The URL of the webhook", name="url")
    num_pending: Optional[int] = strawberry.field(description="Number of pending events in queue", name="numPending")
    last_success: Optional[datetime.datetime] = strawberry.field(description="Timestamp of last successful delivery | Format: date-time", name="lastSuccess")
    last_error: Optional[datetime.datetime] = strawberry.field(description="Timestamp of last failed delivery | Format: date-time", name="lastError")
    last_error_message: Optional[str] = strawberry.field(description="Message from last failed delivery", name="lastErrorMessage")

@strawberry.enum
class Severity(SiaType):
    INFO: int = strawberry.enum_value(1, description="Indicates that the alert is informational.")
    WARNING: int = strawberry.enum_value(2, description="Indicates that the alert is a warning.")
    ERROR: int = strawberry.enum_value(3, description="Indicates that the alert is an error.")
    CRITICAL: int = strawberry.enum_value(4, description="Indicates that the alert is critical.")

@strawberry.type
class Alert(SiaType):
    id: Optional[Hash256] = strawberry.field(description="A unique identifier for the alert", name="id")
    severity: Optional[Severity] = strawberry.field(description="The severity of the alert", name="severity")
    message: Optional[str] = strawberry.field(description="Human-readable message describing the alert", name="message")
    data: Optional[JSON] = strawberry.field(description="Additional context or metadata for the alert", name="data")
    timestamp: Optional[datetime.datetime] = strawberry.field(description="Format: date-time", name="timestamp")

@strawberry.type
class AlertsOpts(SiaType):
    offset: Optional[int] = strawberry.field(description="Offset used in pagination", name="offset")
    limit: Optional[int] = strawberry.field(description="Limit used in pagination", name="limit")
    severity: Optional[Severity] = strawberry.field(description="Severity filter (1=info,2=warning,3=error,4=critical)", name="severity")

@strawberry.type
class AlertTotals(SiaType):
    info: Optional[int] = strawberry.field(description="Number of informational alerts", name="info")
    warning: Optional[int] = strawberry.field(description="Number of warning alerts", name="warning")
    error: Optional[int] = strawberry.field(description="Number of error alerts", name="error")
    critical: Optional[int] = strawberry.field(description="Number of critical alerts", name="critical")

@strawberry.type
class AlertsResponse(SiaType):
    alerts: Optional[List[Alert]] = strawberry.field(description="List of alerts", name="alerts")
    has_more: Optional[bool] = strawberry.field(description="Indicates if more alerts remain", name="hasMore")
    totals: Optional[AlertTotals] = strawberry.field(description="Aggregate counts of alerts by severity", name="totals")


@strawberry.type
class AccountsAddBalanceRequest(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(description="Public key of the host", name="hostKey")
    amount: Optional[int] = strawberry.field(description="Amount to be added to the account balance", name="amount")

@strawberry.type
class AccountHandlerPOST(SiaType):
    host_key: Optional[str] = strawberry.field(description="Public key of the host", name="hostKey")

@strawberry.type
class AccountsRequiresSyncRequest(SiaType):
    host_key: Optional[str] = strawberry.field(description="Public key of the host", name="hostKey")

@strawberry.type
class AccountsUpdateBalanceRequest(SiaType):
    host_key: Optional[str] = strawberry.field(description="Public key of the host", name="hostKey")
    amount: Optional[int] = strawberry.field(description="Updated balance amount", name="amount")

@strawberry.type
class AutopilotTriggerRequest(SiaType):
    force_scan: Optional[bool] = strawberry.field(description="Whether to force an immediate host scan", name="forceScan")

@strawberry.type
class AutopilotTriggerResponse(SiaType):
    triggered: Optional[bool] = strawberry.field(description="Indicates if the autopilot loop was triggered", name="triggered")

@strawberry.type
class AutopilotStateResponse(SiaType):
    enabled: Optional[bool] = strawberry.field(description="Indicates whether the autopilot is enabled", name="enabled")
    migrating: Optional[bool] = strawberry.field(description="Autopilot is currently migrating", name="migrating")
    migrating_last_start: Optional[datetime.datetime] = strawberry.field(description="Last start time for migrating", name="migratingLastStart")
    pruning: Optional[bool] = strawberry.field(description="Autopilot is currently pruning", name="pruning")
    pruning_last_start: Optional[datetime.datetime] = strawberry.field(description="Last start time for pruning", name="pruningLastStart")
    scanning: Optional[bool] = strawberry.field(description="Autopilot is currently scanning hosts", name="scanning")
    scanning_last_start: Optional[datetime.datetime] = strawberry.field(description="Last start time for scanning", name="scanningLastStart")
    uptime_ms: Optional[DurationMS] = strawberry.field(description="Autopilot uptime in milliseconds", name="uptimeMs")
    start_time: Optional[datetime.datetime] = strawberry.field(description="Timestamp of autopilot's start time", name="startTime")
    build_state: Optional[BuildState] = strawberry.field(description="Information about the build state of the autopilot", name="buildState")


@strawberry.type
class ConfigEvaluationRequest(SiaType):
    autopilot_config: Optional[AutopilotConfig] = strawberry.field(description="Proposed autopilot config", name="autopilotConfig")
    gouging_settings: Optional[GougingSettings] = strawberry.field(description="Proposed gouging settings", name="gougingSettings")
    redundancy_settings: Optional[RedundancySettings] = strawberry.field(description="Proposed redundancy settings", name="redundancySettings")

@strawberry.type
class ConfigEvaluationUnusableGouging(SiaType):
    contract: Optional[int] = strawberry.field(name="contract")
    download: Optional[int] = strawberry.field(name="download")
    gouging: Optional[int] = strawberry.field(name="gouging")
    pruning: Optional[int] = strawberry.field(name="pruning")
    upload: Optional[int] = strawberry.field(name="upload")

@strawberry.type
class ConfigEvaluationUnusable(SiaType):
    blocked: Optional[int] = strawberry.field(name="blocked")
    gouging: Optional[ConfigEvaluationUnusableGouging] = strawberry.field(name="gouging")
    low_max_duration: Optional[int] = strawberry.field(name="lowMaxDuration")
    not_accepting_contracts: Optional[int] = strawberry.field(name="notAcceptingContracts")
    not_scanned: Optional[int] = strawberry.field(name="notScanned")

@strawberry.type
class ConfigEvaluationResponse(SiaType):
    hosts: Optional[int] = strawberry.field(description="Total hosts scanned", name="hosts")
    usable: Optional[int] = strawberry.field(description="Number of hosts determined to be usable", name="usable")
    unusable: Optional[ConfigEvaluationUnusable] = strawberry.field(description="Breakdown of unusable hosts", name="unusable")
    recommendation: Optional[ConfigRecommendation] = strawberry.field(description="Recommended config changes", name="recommendation")


@strawberry.type
class CreateBucketOptions(SiaType):
    policy: Optional[BucketPolicy] = strawberry.field(description="Bucket policy options", name="policy")

@strawberry.type
class BucketCreateRequest(SiaType):
    name: Optional[str] = strawberry.field(description="Name of the new bucket", name="name")
    policy: Optional[BucketPolicy] = strawberry.field(description="Policy configuration for this bucket", name="policy")

@strawberry.type
class BucketUpdatePolicyRequest(SiaType):
    policy: Optional[BucketPolicy] = strawberry.field(description="Updated policy configuration for this bucket", name="policy")


# ---


@strawberry.type
class UploadParams(SiaType):
    current_height: Optional[int] = strawberry.field(description="Current block height", name="currentHeight")
    upload_packing: Optional[bool] = strawberry.field(description="Whether upload packing is enabled", name="uploadPacking")
    gouging_params: Optional[GougingParams] = strawberry.field(description="Parameters for gouging checks", name="gougingParams")

@strawberry.type
class AccountsFundRequest(SiaType):
    account_id: Optional[str] = strawberry.field(description="Unique account ID (rhpv3.Account)", name="accountID")
    amount: Optional[Currency] = strawberry.field(description="Amount to fund the account with", name="amount")
    contract_id: Optional[FileContractID] = strawberry.field(description="ID of the contract used for funding", name="contractID")

@strawberry.type
class AccountsFundResponse(SiaType):
    deposit: Optional[Currency] = strawberry.field(description="Amount deposited", name="deposit")

@strawberry.type
class AccountsSaveRequest(SiaType):
    accounts: Optional[List[Account]] = strawberry.field(description="List of accounts to save", name="accounts")

@strawberry.type
class BackupRequest(SiaType):
    database: Optional[str] = strawberry.field(description="Type of database to back up", name="database")
    path: Optional[str] = strawberry.field(description="Path to save the backup", name="path")

@strawberry.type
class ExplorerState(SiaType):
    enabled: Optional[bool] = strawberry.field(description="Indicates whether explorer is enabled", name="enabled")
    url: Optional[str] = strawberry.field(description="Optional URL for the explorer source", name="url")

@strawberry.type
class BusStateResponse(SiaType):
    start_time: Optional[datetime.datetime] = strawberry.field(description="Timestamp when the bus started", name="startTime")
    network: Optional[str] = strawberry.field(description="Network identifier (e.g., 'mainnet', 'testnet')", name="network")
    build_state: Optional[BuildState] = strawberry.field(description="Build state information", name="buildState")
    explorer: Optional[ExplorerState] = strawberry.field(description="Information about the explorer state", name="explorer")

@strawberry.type
class HostScanRequest(SiaType):
    timeout: Optional[DurationMS] = strawberry.field(description="Timeout duration in ms for host scan", name="timeout")

@strawberry.type
class HostScanResponse(SiaType):
    ping: Optional[DurationMS] = strawberry.field(description="Ping time in ms", name="ping")
    scan_error: Optional[str] = strawberry.field(description="Error encountered during scan, if any", name="scanError")
    settings: Optional[JSON] = strawberry.field(description="Host settings (rhpv2.HostSettings)", name="settings")
    price_table: Optional[JSON] = strawberry.field(description="Price table (rhpv3.HostPriceTable)", name="priceTable")
    v2_settings: Optional[JSON] = strawberry.field(description="v2 Host settings (rhp4.HostSettings)", name="v2Settings")

@strawberry.type
class UpdateAutopilotRequest(SiaType):
    enabled: Optional[bool] = strawberry.field(description="Toggle for enabling/disabling the autopilot", name="enabled")
    contracts: Optional[ContractsConfig] = strawberry.field(description="Updated contracts config", name="contracts")
    hosts: Optional[HostsConfig] = strawberry.field(description="Updated hosts config", name="hosts")

# ---

@strawberry.type
class ContractPrunableData(SiaType):
    id: Optional[FileContractID] = strawberry.field(name="id")
    prunable: Optional[int] = strawberry.field(name="prunable")
    size: Optional[int] = strawberry.field(name="size")

@strawberry.type
class ContractSpendingRecord(SiaType):
    deletions: Optional[Currency] = strawberry.field(name="deletions")
    fund_account: Optional[Currency] = strawberry.field(name="fundAccount")
    sector_roots: Optional[Currency] = strawberry.field(name="sectorRoots")
    uploads: Optional[Currency] = strawberry.field(name="uploads")
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    revision_number: Optional[int] = strawberry.field(name="revisionNumber")
    size: Optional[int] = strawberry.field(name="size")
    missed_host_payout: Optional[Currency] = strawberry.field(name="missedHostPayout")
    valid_renter_payout: Optional[Currency] = strawberry.field(name="validRenterPayout")

@strawberry.type
class ContractAcquireRequest(SiaType):
    duration: Optional[DurationMS] = strawberry.field(name="duration")
    priority: Optional[int] = strawberry.field(name="priority")

@strawberry.type
class ContractAcquireResponse(SiaType):
    lock_id: Optional[int] = strawberry.field(name="lockID")

@strawberry.type
class ContractAddRequest(SiaType):
    contract_price: Optional[Currency] = strawberry.field(name="contractPrice")
    initial_renter_funds: Optional[Currency] = strawberry.field(name="initialRenterFunds")
    revision: Optional[JSON] = strawberry.field(name="revision", description="rhpv2.ContractRevision")
    start_height: Optional[int] = strawberry.field(name="startHeight")
    state: Optional[str] = strawberry.field(name="state")

@strawberry.type
class ContractFormRequest(SiaType):
    end_height: Optional[int] = strawberry.field(name="endHeight")
    host_collateral: Optional[Currency] = strawberry.field(name="hostCollateral")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    renter_funds: Optional[Currency] = strawberry.field(name="renterFunds")
    renter_address: Optional[Address] = strawberry.field(name="renterAddress")

@strawberry.type
class ContractKeepaliveRequest(SiaType):
    duration: Optional[DurationMS] = strawberry.field(name="duration")
    lock_id: Optional[int] = strawberry.field(name="lockID")

@strawberry.type
class ContractPruneRequest(SiaType):
    timeout: Optional[DurationMS] = strawberry.field(name="timeout")

@strawberry.type
class ContractPruneResponse(SiaType):
    contract_size: Optional[int] = strawberry.field(name="size")
    pruned: Optional[int] = strawberry.field(name="pruned")
    remaining: Optional[int] = strawberry.field(name="remaining")
    error: Optional[str] = strawberry.field(name="error")

@strawberry.type
class ContractReleaseRequest(SiaType):
    lock_id: Optional[int] = strawberry.field(name="lockID")

@strawberry.type
class ContractRenewRequest(SiaType):
    end_height: Optional[int] = strawberry.field(name="endHeight")
    expected_new_storage: Optional[int] = strawberry.field(name="expectedNewStorage")
    min_new_collateral: Optional[Currency] = strawberry.field(name="minNewCollateral")
    renter_funds: Optional[Currency] = strawberry.field(name="renterFunds")

@strawberry.type
class ContractsArchiveRequest(SiaType):
    # This represents a map of [FileContractID -> reason], encoded as JSON.
    # Example: { "fcid1": "removed", "fcid2": "hostpruned" }
    contracts: Optional[JSON] = strawberry.field(description="Map of contract IDs to archival reasons")

@strawberry.type
class ContractsPrunableDataResponse(SiaType):
    contracts: Optional[List[ContractPrunableData]] = strawberry.field(name="contracts")
    total_prunable: Optional[int] = strawberry.field(name="totalPrunable")
    total_size: Optional[int] = strawberry.field(name="totalSize")

@strawberry.type
class ContractsOpts(SiaType):
    filter_mode: Optional[str] = strawberry.field(name="filterMode")



#

# ...existing code...

@strawberry.type
class HostsPriceTablesRequest(SiaType):
    price_table_updates: Optional[List[JSON]] = strawberry.field(
        description="List of price table updates (host -> updated price table info)", 
        name="priceTableUpdates"
    )

@strawberry.type
class HostsRemoveRequest(SiaType):
    max_downtime_hours: Optional[DurationH] = strawberry.field(name="maxDowntimeHours")
    max_consecutive_scan_failures: Optional[int] = strawberry.field(name="maxConsecutiveScanFailures")

@strawberry.type
class HostsRequest(SiaType):
    offset: Optional[int] = strawberry.field(name="offset")
    limit: Optional[int] = strawberry.field(name="limit")
    filter_mode: Optional[str] = strawberry.field(name="filterMode")
    usability_mode: Optional[str] = strawberry.field(name="usabilityMode")
    address_contains: Optional[str] = strawberry.field(name="addressContains")
    key_in: Optional[List[PublicKey]] = strawberry.field(name="keyIn")
    max_last_scan: Optional[datetime.datetime] = strawberry.field(name="maxLastScan")

@strawberry.type
class UpdateAllowlistRequest(SiaType):
    add: Optional[List[PublicKey]] = strawberry.field(name="add")
    remove: Optional[List[PublicKey]] = strawberry.field(name="remove")
    clear: Optional[bool] = strawberry.field(name="clear")

@strawberry.type
class UpdateBlocklistRequest(SiaType):
    add: Optional[List[str]] = strawberry.field(name="add")
    remove: Optional[List[str]] = strawberry.field(name="remove")
    clear: Optional[bool] = strawberry.field(name="clear")

@strawberry.type
class HostOptions(SiaType):
    address_contains: Optional[str] = strawberry.field(name="addressContains")
    filter_mode: Optional[str] = strawberry.field(name="filterMode")
    usability_mode: Optional[str] = strawberry.field(name="usabilityMode")
    key_in: Optional[List[PublicKey]] = strawberry.field(name="keyIn")
    limit: Optional[int] = strawberry.field(name="limit")
    max_last_scan: Optional[datetime.datetime] = strawberry.field(name="maxLastScan")
    offset: Optional[int] = strawberry.field(name="offset")



@strawberry.type
class HostInteractions(SiaType):
    total_scans: Optional[int] = strawberry.field(name="totalScans")
    last_scan: Optional[datetime.datetime] = strawberry.field(name="lastScan")
    last_scan_success: Optional[bool] = strawberry.field(name="lastScanSuccess")
    lost_sectors: Optional[int] = strawberry.field(name="lostSectors")
    second_to_last_scan_success: Optional[bool] = strawberry.field(name="secondToLastScanSuccess")
    uptime: Optional[DurationMS] = strawberry.field(name="uptime")
    downtime: Optional[DurationMS] = strawberry.field(name="downtime")
    successful_interactions: Optional[float] = strawberry.field(name="successfulInteractions")
    failed_interactions: Optional[float] = strawberry.field(name="failedInteractions")


@strawberry.type
class HostScan(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    price_table: Optional[JSON] = strawberry.field(name="priceTable")
    settings: Optional[JSON] = strawberry.field(name="settings")
    v2_settings: Optional[JSON] = strawberry.field(name="v2Settings")
    success: Optional[bool] = strawberry.field(name="success")
    timestamp: Optional[datetime.datetime] = strawberry.field(name="timestamp")

@strawberry.type
class HostPriceTableUpdate(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    success: Optional[bool] = strawberry.field(name="success")
    timestamp: Optional[datetime.datetime] = strawberry.field(name="timestamp")
    price_table: Optional[HostPriceTable] = strawberry.field(name="priceTable")



@strawberry.type
class PerformanceMetricsQueryOpts(SiaType):
    action: Optional[str] = strawberry.field(description="Name of the action (ex: 'contract')", name="action")
    host_key: Optional[PublicKey] = strawberry.field(description="Public key of a host", name="hostKey")
    origin: Optional[str] = strawberry.field(description="Origin identifier", name="origin")


@strawberry.type
class ContractMetricsQueryOpts(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(description="Specific contract ID", name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(description="Public key of a host", name="hostKey")


@strawberry.type
class ContractPruneMetricsQueryOpts(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(description="Contract ID", name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(description="Public key of the host", name="hostKey")
    host_version: Optional[str] = strawberry.field(description="Host version", name="hostVersion")


@strawberry.type
class WalletMetricsQueryOpts(SiaType):
    # No fields currently defined
    pass

@strawberry.type
class ContractPruneMetricRequestPUT(SiaType):
    metrics: Optional[List[ContractPruneMetric]] = strawberry.field(name="metrics")

@strawberry.type
class ContractMetricRequestPUT(SiaType):
    metrics: Optional[List[ContractMetric]] = strawberry.field(name="metrics")


@strawberry.type
class CreateMultipartOptions(SiaType):
    disable_client_side_encryption: Optional[bool] = strawberry.field(name="disableClientSideEncryption")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")

@strawberry.type
class CompleteMultipartOptions(SiaType):
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")

@strawberry.type
class MultipartAbortRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    key: Optional[str] = strawberry.field(name="key")
    upload_id: Optional[str] = strawberry.field(name="uploadID")

@strawberry.type
class MultipartAddPartRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    e_tag: Optional[str] = strawberry.field(name="eTag")
    key: Optional[str] = strawberry.field(name="key")
    upload_id: Optional[str] = strawberry.field(name="uploadID")
    part_number: Optional[int] = strawberry.field(name="partNumber")
    slices: Optional[List[JSON]] = strawberry.field(name="slices", description="List of slices (object.SlabSlice)")

@strawberry.type
class MultipartCompleteResponse(SiaType):
    e_tag: Optional[str] = strawberry.field(name="eTag")

@strawberry.type
class MultipartCompleteRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")
    key: Optional[str] = strawberry.field(name="key")
    upload_id: Optional[str] = strawberry.field(name="uploadID")
    parts: Optional[List[MultipartCompletedPart]] = strawberry.field(name="parts")

@strawberry.type
class MultipartCreateRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    key: Optional[str] = strawberry.field(name="key")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")
    disable_client_side_encryption: Optional[bool] = strawberry.field(name="disableClientSideEncryption")

@strawberry.type
class MultipartCreateResponse(SiaType):
    upload_id: Optional[str] = strawberry.field(name="uploadID")

@strawberry.type
class MultipartListPartsRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    key: Optional[str] = strawberry.field(name="key")
    upload_id: Optional[str] = strawberry.field(name="uploadID")
    part_number_marker: Optional[int] = strawberry.field(name="partNumberMarker")
    limit: Optional[int] = strawberry.field(name="limit")

@strawberry.type
class MultipartListPartsResponse(SiaType):
    has_more: Optional[bool] = strawberry.field(name="hasMore")
    next_marker: Optional[int] = strawberry.field(name="nextMarker")
    parts: Optional[List[MultipartListPartItem]] = strawberry.field(name="parts")

@strawberry.type
class MultipartListUploadsRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    prefix: Optional[str] = strawberry.field(name="prefix")
    key_marker: Optional[str] = strawberry.field(name="keyMarker")
    upload_id_marker: Optional[str] = strawberry.field(name="uploadIDMarker")
    limit: Optional[int] = strawberry.field(name="limit")

@strawberry.type
class MultipartListUploadsResponse(SiaType):
    has_more: Optional[bool] = strawberry.field(name="hasMore")
    next_path_marker: Optional[str] = strawberry.field(name="nextMarker")
    next_upload_id_marker: Optional[str] = strawberry.field(name="nextUploadIDMarker")
    uploads: Optional[List[MultipartUpload]] = strawberry.field(name="uploads")


# -


@strawberry.type
class GetObjectResponse(SiaType):
    content: Optional[str] = strawberry.field(name="content")
    content_type: Optional[str] = strawberry.field(name="contentType")
    etag: Optional[str] = strawberry.field(name="etag")
    last_modified: Optional[datetime.datetime] = strawberry.field(name="lastModified")
    content_range: Optional[JSON] = strawberry.field(name="range", description="ContentRange") # changed from 'range'
    size: Optional[int] = strawberry.field(name="size")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")

@strawberry.type
class ObjectsResponse(SiaType):
    has_more: Optional[bool] = strawberry.field(name="hasMore")
    next_marker: Optional[str] = strawberry.field(name="nextMarker")
    objects: Optional[List[ObjectMetadata]] = strawberry.field(name="objects")

@strawberry.type
class ObjectsRemoveRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    prefix: Optional[str] = strawberry.field(name="prefix")

@strawberry.type
class ObjectsRenameRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    force: Optional[bool] = strawberry.field(name="force")
    from_key: Optional[str] = strawberry.field(name="from")
    to: Optional[str] = strawberry.field(name="to")
    mode: Optional[str] = strawberry.field(name="mode")

@strawberry.type
class ObjectsStatsOpts(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")

@strawberry.type
class ObjectsStatsResponse(SiaType):
    num_objects: Optional[int] = strawberry.field(name="numObjects")
    num_unfinished_objects: Optional[int] = strawberry.field(name="numUnfinishedObjects")
    min_health: Optional[float] = strawberry.field(name="minHealth")
    total_objects_size: Optional[int] = strawberry.field(name="totalObjectsSize")
    total_unfinished_objects_size: Optional[int] = strawberry.field(name="totalUnfinishedObjectsSize")
    total_sectors_size: Optional[int] = strawberry.field(name="totalSectorsSize")
    total_uploaded_size: Optional[int] = strawberry.field(name="totalUploadedSize")

@strawberry.type
class AddObjectOptions(SiaType):
    e_tag: Optional[str] = strawberry.field(name="ETag")
    mime_type: Optional[str] = strawberry.field(name="MimeType")
    metadata: Optional[JSON] = strawberry.field(name="Metadata", description="ObjectUserMetadata")

@strawberry.type
class AddObjectRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    object_data: Optional[JSON] = strawberry.field(name="object", description="object.Object")
    e_tag: Optional[str] = strawberry.field(name="eTag")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")

@strawberry.type
class CopyObjectOptions(SiaType):
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")

@strawberry.type
class CopyObjectsRequest(SiaType):
    source_bucket: Optional[str] = strawberry.field(name="sourceBucket")
    source_key: Optional[str] = strawberry.field(name="sourcePath")
    destination_bucket: Optional[str] = strawberry.field(name="destinationBucket")
    destination_key: Optional[str] = strawberry.field(name="destinationPath")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")

@strawberry.type
class HeadObjectOptions(SiaType):
    range_arg: Optional[JSON] = strawberry.field(name="range", description="DownloadRange")

@strawberry.type
class DownloadObjectOptions(SiaType):
    range_arg: Optional[JSON] = strawberry.field(name="range", description="DownloadRange")

@strawberry.type
class GetObjectOptions(SiaType):
    only_metadata: Optional[bool] = strawberry.field(name="onlyMetadata")

@strawberry.type
class ListObjectOptions(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    delimiter: Optional[str] = strawberry.field(name="delimiter")
    limit: Optional[int] = strawberry.field(name="limit")
    marker: Optional[str] = strawberry.field(name="marker")
    sort_by: Optional[str] = strawberry.field(name="sortBy")
    sort_dir: Optional[str] = strawberry.field(name="sortDir")
    substring: Optional[str] = strawberry.field(name="substring")
    slab_encryption_key: Optional[JSON] = strawberry.field(name="slabEncryptionKey", description="object.EncryptionKey")

@strawberry.type
class UploadObjectOptions(SiaType):
    min_shards: Optional[int] = strawberry.field(name="minShards")
    total_shards: Optional[int] = strawberry.field(name="totalShards")
    content_length: Optional[int] = strawberry.field(name="contentLength")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")

@strawberry.type
class UploadMultipartUploadPartOptions(SiaType):
    min_shards: Optional[int] = strawberry.field(name="minShards")
    total_shards: Optional[int] = strawberry.field(name="totalShards")
    encryption_offset: Optional[int] = strawberry.field(name="encryptionOffset")
    content_length: Optional[int] = strawberry.field(name="contentLength")

@strawberry.type
class S3AuthenticationSettings(SiaType):
    v4_keypairs: Optional[JSON] = strawberry.field(name="v4Keypairs",
        description="Mapping of accessKeyID -> secretAccessKey")


@strawberry.type
class UnhealthySlab(SiaType):
    encryption_key: Optional[JSON] = strawberry.field(
        name="encryptionKey",
        description="Encryption key object (object.EncryptionKey)"
    )
    health: Optional[float] = strawberry.field(name="health")


@strawberry.type
class AddPartialSlabResponse(SiaType):
    slab_buffer_max_size_soft_reached: Optional[bool] = strawberry.field(name="slabBufferMaxSizeSoftReached")
    slabs: Optional[List[JSON]] = strawberry.field(
        description="List of slabs (object.SlabSlice)",
        name="slabs"
    )

@strawberry.type
class MigrationSlabsRequest(SiaType):
    health_cutoff: Optional[float] = strawberry.field(name="healthCutoff")
    limit: Optional[int] = strawberry.field(name="limit")

@strawberry.type
class PackedSlabsRequestGET(SiaType):
    locking_duration: Optional[DurationMS] = strawberry.field(name="lockingDuration")
    min_shards: Optional[int] = strawberry.field(name="minShards")
    total_shards: Optional[int] = strawberry.field(name="totalShards")
    limit: Optional[int] = strawberry.field(name="limit")

@strawberry.type
class PackedSlabsRequestPOST(SiaType):
    slabs: Optional[List[UploadedPackedSlab]] = strawberry.field(name="slabs")

@strawberry.type
class SlabsForMigrationResponse(SiaType):
    slabs: Optional[List[UnhealthySlab]] = strawberry.field(name="slabs")

@strawberry.type
class UpdateSlabRequest(SiaType):
    # Represented as []UploadedSector in Go
    uploaded_sectors: Optional[List[UploadedSector]] = strawberry.field(name="updateSlabRequest")



@strawberry.type
class ChurnUpdate(SiaType):
    time: Optional[datetime.datetime] = strawberry.field(name="time")
    from_state: Optional[str] = strawberry.field(name="from")
    to_state: Optional[str] = strawberry.field(name="to")
    reason: Optional[str] = strawberry.field(name="reason")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    size: Optional[int] = strawberry.field(name="size")

@strawberry.type
class AccumulatedChurn(SiaType):
    # Maps a contractID to a list of churn updates
    churn_updates: Optional[JSON] = strawberry.field(
        description="Dict[FileContractID -> List[ChurnUpdate]]",
        name="churn"
    )

@strawberry.type
class UsabilityUpdate(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(name="hk")
    contract_id: Optional[FileContractID] = strawberry.field(name="fcid")
    size: Optional[int] = strawberry.field(name="size")
    from_state: Optional[str] = strawberry.field(name="from")
    to_state: Optional[str] = strawberry.field(name="to")
    reason: Optional[str] = strawberry.field(name="reason")




# ------ walletd --------


@strawberry.enum
class IndexMode(SiaType):
    PERSONAL = "personal"
    FULL = "full"
    NONE = "none"


@strawberry.type
class Balance(SiaType):
    siacoins: Optional[Currency] = strawberry.field(name="siacoins")
    immature_siacoins: Optional[Currency] = strawberry.field(name="immatureSiacoins")
    siafunds: Optional[int] = strawberry.field(name="siafunds")

@strawberry.type
class Wallet(SiaType): 
    id: Optional[int] = strawberry.field(name="id")
    name: Optional[str] = strawberry.field(name="name")
    description: Optional[str] = strawberry.field(name="description")
    date_created: Optional[datetime.datetime] = strawberry.field(name="dateCreated")
    last_updated: Optional[datetime.datetime] = strawberry.field(name="lastUpdated")
    metadata: Optional[JSON] = strawberry.field(name="metadata")

@strawberry.type
class StateResponse(SiaType):
    version: Optional[str] = strawberry.field(name="version")
    commit: Optional[str] = strawberry.field(name="commit")
    os: Optional[str] = strawberry.field(name="os")
    build_time: Optional[datetime.datetime] = strawberry.field(name="buildTime")
    start_time: Optional[datetime.datetime] = strawberry.field(name="startTime")
    index_mode: Optional[IndexMode] = strawberry.field(name="indexMode")

@strawberry.type
class GatewayPeer(SiaType):
    address: Optional[str] = strawberry.field(name="address")
    inbound: Optional[bool] = strawberry.field(name="inbound")
    version: Optional[str] = strawberry.field(name="version")
    first_seen: Optional[datetime.datetime] = strawberry.field(name="firstSeen")
    connected_since: Optional[datetime.datetime] = strawberry.field(name="connectedSince")
    synced_blocks: Optional[int] = strawberry.field(name="syncedBlocks")
    sync_duration: Optional[DurationMS] = strawberry.field(name="syncDuration")

@strawberry.type
class TxpoolBroadcastRequest(SiaType):
    basis: Optional[ChainIndex] = strawberry.field(name="basis", description="types.ChainIndex")
    transactions: Optional[List[Transaction]] = strawberry.field(name="transactions", description="[]types.Transaction")
    v2transactions: Optional[List[V2Transaction]] = strawberry.field(name="v2transactions", description="[]types.V2Transaction")

@strawberry.type
class TxpoolTransactionsResponse(SiaType):
    basis: Optional[JSON] = strawberry.field(name="basis", description="types.ChainIndex")
    transactions: Optional[List[JSON]] = strawberry.field(name="transactions", description="[]types.Transaction")
    v2transactions: Optional[List[JSON]] = strawberry.field(name="v2transactions", description="[]types.V2Transaction")

@strawberry.type
class BalanceResponse(Balance):
    # wallet.Balance details; represent as JSON or separate fields if known.
    balance_data: Optional[JSON] = strawberry.field(description="wallet.Balance")

@strawberry.type
class WalletReserveRequest(SiaType):
    siacoin_outputs: Optional[List[SiacoinOutputID]] = strawberry.field(
        name="siacoinOutputs",
        description="[]types.SiacoinOutputID"
    )
    siafund_outputs: Optional[List[SiafundOutputID]] = strawberry.field(
        name="siafundOutputs",
        description="[]types.SiafundOutputID"
    )

@strawberry.type
class WalletUpdateRequest(SiaType):
    name: Optional[str] = strawberry.field(name="name")
    description: Optional[str] = strawberry.field(name="description")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="json.RawMessage")

@strawberry.type
class WalletReleaseRequest(SiaType):
    siacoin_outputs: Optional[List[SiacoinOutputID]] = strawberry.field(
        name="siacoinOutputs",
        description="[]types.SiacoinOutputID"
    )
    siafund_outputs: Optional[List[SiafundOutputID]] = strawberry.field(
        name="siafundOutputs",
        description="[]types.SiafundOutputID"
    )

@strawberry.type
class WalletFundRequest(SiaType):
    transaction: Optional[Transaction] = strawberry.field(description="types.Transaction", name="transaction")
    amount: Optional[Currency] = strawberry.field(name="amount")
    change_address: Optional[Address] = strawberry.field(
        name="changeAddress",
        description="types.Address"
    )

@strawberry.type
class WalletFundSFRequest(SiaType):
    transaction: Optional[Transaction] = strawberry.field(description="types.Transaction", name="transaction")
    amount: Optional[int] = strawberry.field(name="amount")
    change_address: Optional[Address] = strawberry.field(
        name="changeAddress",
        description="types.Address"
    )
    claim_address: Optional[Address] = strawberry.field(
        name="claimAddress",
        description="types.Address"
    )

@strawberry.type
class WalletFundResponse(SiaType):
    transaction: Optional[Transaction] = strawberry.field(description="types.Transaction", name="transaction")
    to_sign: Optional[List[Hash256]] = strawberry.field(name="toSign")
    depends_on: Optional[List[Transaction]] = strawberry.field(
        name="dependsOn",
        description="[]types.Transaction"
    )

@strawberry.type
class WalletConstructRequest(SiaType):
    siacoins: Optional[List[SiacoinOutput]] = strawberry.field(
        name="siacoins",
        description="[]types.SiacoinOutput"
    )
    siafunds: Optional[List[SiafundOutput]] = strawberry.field(
        name="siafunds",
        description="[]types.SiafundOutput"
    )
    change_address: Optional[Address] = strawberry.field(
        name="changeAddress",
        description="types.Address"
    )

@strawberry.type
class SignaturePayload(SiaType):
    public_key: Optional[PublicKey] = strawberry.field(
        name="publicKey",
        description="types.PublicKey"
    )
    sig_hash: Optional[Hash256] = strawberry.field(name="sigHash")

@strawberry.type
class WalletConstructResponse(SiaType):
    basis: Optional[ChainIndex] = strawberry.field(name="basis", description="types.ChainIndex")
    id: Optional[TransactionID] = strawberry.field(name="id", description="types.TransactionID")
    transaction: Optional[Transaction] = strawberry.field(name="transaction", description="types.Transaction")
    estimated_fee: Optional[Currency] = strawberry.field(name="estimatedFee")

@strawberry.type
class WalletConstructV2Response(SiaType):
    basis: Optional[ChainIndex] = strawberry.field(name="basis", description="types.ChainIndex")
    id: Optional[TransactionID] = strawberry.field(name="id", description="types.TransactionID")
    transaction: Optional[V2Transaction] = strawberry.field(name="transaction", description="types.V2Transaction")
    estimated_fee: Optional[Currency] = strawberry.field(name="estimatedFee")

@strawberry.type
class SeedSignRequest(SiaType):
    transaction: Optional[Transaction] = strawberry.field(name="transaction", description="types.Transaction")
    keys: Optional[List[int]] = strawberry.field(name="keys")

@strawberry.type
class RescanResponse(SiaType):
    start_index: Optional[ChainIndex] = strawberry.field(name="startIndex", description="types.ChainIndex")
    index: Optional[ChainIndex] = strawberry.field(name="index", description="types.ChainIndex")
    start_time: Optional[datetime.datetime] = strawberry.field(name="startTime")
    error: Optional[str] = strawberry.field(name="error")

@strawberry.type
class ApplyUpdate(SiaType):
    update: Optional[JSON] = strawberry.field(name="update", description="consensus.ApplyUpdate")
    state: Optional[JSON] = strawberry.field(name="state", description="consensus.State")
    block: Optional[Block] = strawberry.field(name="block", description="types.Block")

@strawberry.type
class RevertUpdate(SiaType):
    update: Optional[JSON] = strawberry.field(name="update", description="consensus.RevertUpdate")
    state: Optional[JSON] = strawberry.field(name="state", description="consensus.State")
    block: Optional[Block] = strawberry.field(name="block", description="types.Block")

@strawberry.type
class ConsensusUpdatesResponse(SiaType):
    applied: Optional[List[ApplyUpdate]] = strawberry.field(name="applied")
    reverted: Optional[List[RevertUpdate]] = strawberry.field(name="reverted")

@strawberry.type
class DebugMineRequest(SiaType):
    blocks: Optional[int] = strawberry.field(name="blocks")
    address: Optional[Address] = strawberry.field(name="address", description="types.Address")
