from typing import List, Optional, Union
from strawberry.types import Info
import strawberry
from datetime import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from strawberry.scalars import JSON
from typing import List, Optional, Dict, Any, NewType
from enum import Enum


# Constants
MAX_REVISION_NUMBER = 2**64 - 1
RENTER_CONTRACT_INDEX = 0
HOST_CONTRACT_INDEX = 1
UNASSIGNED_LEAF_INDEX = 10101010101010101010


@strawberry.type
class Hash256:
    value: str = strawberry.field(description="hex-encoded 32-byte hash")


@strawberry.type
class AttestationID:
    value: Hash256 = strawberry.field(description="uniquely identifies an attestation")


@strawberry.type
class FileContractID:
    value: Hash256 = strawberry.field(description="uniquely identifies an attestation")


@strawberry.type
class PublicKey:
    value: str = strawberry.field(description="hex-encoded 32-byte public key")


@strawberry.type
class PrivateKey:
    value: str = strawberry.field(description="hex-encoded private key")


@strawberry.type
class Signature:
    value: str = strawberry.field(description="hex-encoded 64-byte signature")


@strawberry.type
class Specifier:
    value: str = strawberry.field(description="16-byte identifier")


@strawberry.type
class UnlockKey:
    algorithm: Specifier = strawberry.field()
    key: str = strawberry.field(description="hex-encoded bytes")


@strawberry.type
class UnlockConditions:
    timelock: int
    public_keys: List[UnlockKey] = strawberry.field(name="publicKeys")
    signatures_required: int = strawberry.field(name="signaturesRequired")


@strawberry.type
class Address:
    value: str


@strawberry.type
class BlockID:
    value: str


@strawberry.type
class TransactionID:
    value: str


@strawberry.type
class ChainIndex:
    height: int
    id: BlockID


@strawberry.type
class SiacoinOutput:
    value: str
    address: str


@strawberry.type
class SiafundOutput:
    value: int
    address: str
    claim_start: str = strawberry.field(name="claimStart")


@strawberry.type
class AddressBalance:
    siacoins: str
    immature_siacoins: str = strawberry.field(name="immatureSiacoins")
    siafunds: int


@strawberry.type
class HardforkDevAddr:
    height: int
    old_address: str = strawberry.field(name="oldAddress")
    new_address: str = strawberry.field(name="newAddress")


@strawberry.type
class HardforkTax:
    height: int


@strawberry.type
class HardforkStorageProof:
    height: int


@strawberry.type
class HardforkOak:
    height: int
    fix_height: int = strawberry.field(name="fixHeight")
    genesis_timestamp: datetime = strawberry.field(name="genesisTimestamp")


@strawberry.type
class HardforkASIC:
    height: int
    oak_time: str = strawberry.field(name="oakTime")
    oak_target: str = strawberry.field(name="oakTarget")


@strawberry.type
class HardforkFoundation:
    height: int
    primary_address: str = strawberry.field(name="primaryAddress")
    failsafe_address: str = strawberry.field(name="failsafeAddress")


@strawberry.type
class HardforkV2:
    allow_height: int = strawberry.field(name="allowHeight")
    require_height: int = strawberry.field(name="requireHeight")


@strawberry.type
class MerkleProof:
    hashes: List[Hash256]


@strawberry.type
class StateElement:
    leaf_index: int = strawberry.field(name="leafIndex")
    merkle_proof: MerkleProof = strawberry.field(name="merkleProof")


@strawberry.type
class SiacoinElement:
    id: str
    state_element: StateElement = strawberry.field(name="stateElement")
    siacoin_output: SiacoinOutput = strawberry.field(name="siacoinOutput")
    maturity_height: int = strawberry.field(name="maturityHeight")


@strawberry.type
class SiafundElement:
    id: str
    state_element: StateElement = strawberry.field(name="stateElement")
    siafund_output: SiafundOutput = strawberry.field(name="siafundOutput")
    claim_start: str = strawberry.field(name="claimStart")


@strawberry.type
class BlockIndex:
    height: int
    id: str


# Input Types
@strawberry.input
class SiacoinOutputInput:
    value: str
    address: str


@strawberry.input
class TransactionInput:
    raw_data: JSON


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


# @strawberry.type
# class Signature:
#     parent_id: str = strawberry.field(name="parentID")
#     public_key_index: int = strawberry.field(name="publicKeyIndex")
#     covered_fields: CoveredFields = strawberry.field(name="coveredFields")
#     signature: str


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
class SiacoinInput:
    parent_id: str = strawberry.field(name="parentID")
    unlock_conditions: UnlockConditions = strawberry.field(name="unlockConditions")


@strawberry.type
class SiafundInput:
    parent_id: str = strawberry.field(name="parentID")
    unlock_conditions: UnlockConditions = strawberry.field(name="unlockConditions")
    claim_address: str = strawberry.field(name="claimAddress")


@strawberry.type
class CoveredFields:
    whole_transaction: bool = strawberry.field(name="wholeTransaction")
    siacoin_inputs: Optional[List[int]] = strawberry.field(name="siacoinInputs", default=None)
    siacoin_outputs: Optional[List[int]] = strawberry.field(name="siacoinOutputs", default=None)
    file_contracts: Optional[List[int]] = strawberry.field(name="fileContracts", default=None)
    file_contract_revisions: Optional[List[int]] = strawberry.field(name="fileContractRevisions", default=None)
    storage_proofs: Optional[List[int]] = strawberry.field(name="storageProofs", default=None)
    siafund_inputs: Optional[List[int]] = strawberry.field(name="siafundInputs", default=None)
    siafund_outputs: Optional[List[int]] = strawberry.field(name="siafundOutputs", default=None)
    miner_fees: Optional[List[int]] = strawberry.field(name="minerFees", default=None)
    arbitrary_data: Optional[List[int]] = strawberry.field(name="arbitraryData", default=None)
    signatures: Optional[List[int]] = strawberry.field(name="signatures", default=None)


@strawberry.type
class TransactionSignature:
    parent_id: Hash256 = strawberry.field(name="parentID")
    public_key_index: int = strawberry.field(name="publicKeyIndex")
    timelock: Optional[int] = None
    covered_fields: CoveredFields = strawberry.field(name="coveredFields")
    signature: str


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
class FileContract:
    filesize: int = strawberry.field(description="uint64 file size")
    file_merkle_root: Hash256 = strawberry.field(name="fileMerkleRoot")
    window_start: int = strawberry.field(name="windowStart", description="uint64 start height")
    window_end: int = strawberry.field(name="windowEnd", description="uint64 end height")
    payout: Currency
    valid_proof_outputs: List[SiacoinOutput] = strawberry.field(name="validProofOutputs")
    missed_proof_outputs: List[SiacoinOutput] = strawberry.field(name="missedProofOutputs")
    unlock_hash: Address = strawberry.field(name="unlockHash")
    revision_number: int = strawberry.field(name="revisionNumber", description="uint64 revision number")


@strawberry.type
class FileContractRevision:
    parent_id: str = strawberry.field(name="parentID")
    unlock_conditions: UnlockConditions = strawberry.field(name="unlockConditions")
    file_contract: FileContract = strawberry.field(name="fileContract")


@strawberry.type
class StorageProof:
    parent_id: str = strawberry.field(name="parentID")
    segment_index: int = strawberry.field(name="segmentIndex")
    proof: List[Hash256]


@strawberry.type
class Transaction:
    siacoin_inputs: Optional[List[SiacoinInput]] = strawberry.field(name="siacoinInputs", default=None)
    siacoin_outputs: List[SiacoinOutput] = strawberry.field(name="siacoinOutputs")
    siafund_inputs: Optional[List[SiafundInput]] = strawberry.field(name="siafundInputs", default=None)
    siafund_outputs: Optional[List[SiafundOutput]] = strawberry.field(name="siafundOutputs", default=None)
    file_contracts: Optional[List[FileContract]] = strawberry.field(name="fileContracts", default=None)
    file_contract_revisions: Optional[List[FileContractRevision]] = strawberry.field(
        name="fileContractRevisions", default=None
    )
    storage_proofs: Optional[List[StorageProof]] = strawberry.field(name="storageProofs", default=None)
    miner_fees: List[str] = strawberry.field(name="minerFees")
    arbitrary_data: Optional[List[str]] = strawberry.field(name="arbitraryData", default=None)
    signatures: Optional[List[TransactionSignature]] = strawberry.field(name="signatures", default=None)


@strawberry.type
class FundTransactionResponse:
    transaction: Transaction
    to_sign: List[str] = strawberry.field(name="toSign")
    depends_on: Optional[List[str]] = strawberry.field(name="dependsOn", default=None)


# ---


# V2 Contract Types
@strawberry.type
class V2FileContract:
    capacity: int
    filesize: int
    file_merkle_root: str = strawberry.field(name="fileMerkleRoot")
    proof_height: int = strawberry.field(name="proofHeight")
    expiration_height: int = strawberry.field(name="expirationHeight")
    renter_output: SiacoinOutput = strawberry.field(name="renterOutput")
    host_output: SiacoinOutput = strawberry.field(name="hostOutput")
    missed_host_value: str = strawberry.field(name="missedHostValue")
    total_collateral: str = strawberry.field(name="totalCollateral")
    renter_public_key: str = strawberry.field(name="renterPublicKey")
    host_public_key: str = strawberry.field(name="hostPublicKey")
    revision_number: int = strawberry.field(name="revisionNumber")
    renter_signature: str = strawberry.field(name="renterSignature")
    host_signature: str = strawberry.field(name="hostSignature")


@strawberry.type
class V2FileContractElement:
    id: FileContractID = strawberry.field(name="id")
    state_element: StateElement = strawberry.field(name="stateElement")
    v2_file_contract: V2FileContract = strawberry.field(name="v2FileContract")


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
class SatisfiedPolicy:
    """A satisfied spend policy with signatures and preimages."""

    policy: "SpendPolicy" = strawberry.field()
    signatures: List[str] = strawberry.field(description="List of signatures")
    preimages: List[str] = strawberry.field(description="List of 32-byte preimages in hex format")


@strawberry.type
class V2SiafundInput:
    parent: "SiafundElement" = strawberry.field(name="parent")
    claim_address: str = strawberry.field(name="claimAddress")
    satisfied_policy: SatisfiedPolicy = strawberry.field(name="satisfiedPolicy")


@strawberry.type
class V2FileContractResolution:
    parent: V2FileContractElement = strawberry.field(name="parent")
    resolution: V2FileContractResolutionType = strawberry.field(name="resolution")


@strawberry.type
class Attestation:
    public_key: str = strawberry.field(name="publicKey")
    key: str = strawberry.field()
    value: str = strawberry.field(description="hex-encoded bytes")
    signature: str = strawberry.field()


@strawberry.type
class V2FileContractRevision:
    parent: V2FileContractElement = strawberry.field()
    revision: V2FileContract = strawberry.field()


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
class V2SiacoinInput:
    parent: SiacoinElement = strawberry.field(name="parent")
    satisfied_policy: SatisfiedPolicy = strawberry.field(name="satisfiedPolicy")


@strawberry.type
class V2Transaction:
    siacoin_inputs: List[V2SiacoinInput] = strawberry.field(name="siacoinInputs")
    siacoin_outputs: List[SiacoinOutput] = strawberry.field(name="siacoinOutputs")
    siafund_inputs: List[V2SiafundInput] = strawberry.field(name="siafundInputs")
    siafund_outputs: List[SiafundOutput] = strawberry.field(name="siafundOutputs")
    file_contracts: List[V2FileContract] = strawberry.field(name="fileContracts")
    file_contract_revisions: List[V2FileContractRevision] = strawberry.field(name="fileContractRevisions")
    file_contract_resolutions: List[V2FileContractResolution] = strawberry.field(name="fileContractResolutions")
    attestations: List[Attestation] = strawberry.field()
    arbitrary_data: str = strawberry.field(name="arbitraryData", description="hex-encoded bytes")
    new_foundation_address: Optional[str] = strawberry.field(name="newFoundationAddress")
    miner_fee: str = strawberry.field(name="minerFee", description="Currency amount")


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
class Event:
    id: str = strawberry.field(description="Unique identifier for the event")
    index: ChainIndex  # Changed from BlockIndex to ChainIndex to match Go types
    timestamp: datetime
    maturity_height: int = strawberry.field(
        name="maturityHeight", description="uint64 block height at which this event matures"
    )
    type: str = strawberry.field(description="Type of event (miner/v1transaction/v2transaction)")
    data: Optional[Union[MinerEventData, V1TransactionEventData, V2TransactionEventData]]
    relevant: List[str] = strawberry.field(description="List of relevant addresses")


@strawberry.type
class V2BlockData:
    height: int = strawberry.field()
    commitment: str = strawberry.field()
    transactions: List[V2Transaction] = strawberry.field()


@strawberry.type
class Block:
    parent_id: str = strawberry.field(name="parentID")
    nonce: int = strawberry.field(description="uint64 nonce")
    timestamp: datetime
    miner_payouts: List[SiacoinOutput] = strawberry.field(name="minerPayouts")
    transactions: List[Transaction]
    v2: Optional[V2BlockData] = strawberry.field(
        description="V2 block data containing additional v2 transaction information"
    )


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
