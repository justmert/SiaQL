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
    # A Hash256 is a generic 256-bit cryptographic hash
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


@strawberry.type
class AlertData:
    account_id: str = strawberry.field(name="accountID")
    contract_id: str = strawberry.field(name="contractID")
    host_key: str = strawberry.field(name="hostKey")
    origin: str


@strawberry.type
class Alert:
    id: str
    severity: str
    message: str
    data: AlertData
    timestamp: str


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


@strawberry.input
class AlertInput:
    id: str
    severity: str
    message: str
    data: AlertDataInput
    timestamp: str


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
class ContractSpending:
    deletions: int
    fund_account: int = strawberry.field(name="fundAccount")
    sector_roots: int = strawberry.field(name="sectorRoots")
    uploads: int


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
class ContractMetric:
    timestamp: str
    contract_id: str = strawberry.field(name="contractID")
    host_key: str = strawberry.field(name="hostKey")
    remaining_collateral: str = strawberry.field(name="remainingCollateral")
    remaining_funds: str = strawberry.field(name="remainingFunds")
    revision_number: int = strawberry.field(name="revisionNumber")
    upload_spending: str = strawberry.field(name="uploadSpending")
    download_spending: str = strawberry.field(name="downloadSpending")
    fund_account_spending: str = strawberry.field(name="fundAccountSpending")
    delete_spending: str = strawberry.field(name="deleteSpending")
    list_spending: str = strawberry.field(name="listSpending")


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
class WalletMetric:
    timestamp: str
    confirmed: str
    spendable: str
    unconfirmed: str


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
class MultipartUploadInput:
    bucket: str
    path: str
    key: Optional[str] = None
    generate_key: bool = strawberry.field(name="generateKey", default=False)


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
class GougingSettingsPins:
    max_download: PinningValue = strawberry.field(name="maxDownload")
    max_storage: PinningValue = strawberry.field(name="maxStorage")
    max_upload: PinningValue = strawberry.field(name="maxUpload")
    max_rpc_price: Optional[PinningValue] = strawberry.field(name="maxRPCPrice", default=None)


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
class Slab:
    health: float
    key: str
    min_shards: int = strawberry.field(name="minShards")
    shards: List[Shard]


@strawberry.type
class SlabSlice:
    slab: Slab
    offset: int
    length: int


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
class Webhook:
    module: str
    event: str
    url: str


@strawberry.type
class WebhookQueue:
    url: str
    size: int


@strawberry.type
class WebhookInfo:
    webhooks: List[Webhook]
    queues: List[WebhookQueue]


@strawberry.input
class WebhookInput:
    module: str
    event: str
    url: str


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
class ContractRevision:
    parent_id: str = strawberry.field(name="ParentID")
    unlock_conditions: ContractRevisionUnlockConditions = strawberry.field(name="UnlockConditions")
    filesize: int = strawberry.field(name="Filesize")
    file_merkle_root: str = strawberry.field(name="FileMerkleRoot")
    window_start: int = strawberry.field(name="WindowStart")
    window_end: int = strawberry.field(name="WindowEnd")
    payout: str = strawberry.field(name="Payout")
    valid_proof_outputs: List[ContractOutput] = strawberry.field(name="ValidProofOutputs")
    missed_proof_outputs: List[ContractOutput] = strawberry.field(name="MissedProofOutputs")
    unlock_hash: str = strawberry.field(name="UnlockHash")
    revision_number: int = strawberry.field(name="RevisionNumber")


@strawberry.type
class RHPContract:
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
    revision: Optional[ContractRevision] = None


@strawberry.type
class RHPContractsResponse:
    contracts: List[RHPContract]


@strawberry.type
class ContractPruneResponse:
    pruned: int
    remaining: int


@strawberry.input
class FormContractInput:
    end_height: int = strawberry.field(name="endHeight")
    host_collateral: str = strawberry.field(name="hostCollateral")
    host_key: str = strawberry.field(name="hostKey")
    host_ip: str = strawberry.field(name="hostIP")
    renter_funds: str = strawberry.field(name="renterFunds")
    renter_address: str = strawberry.field(name="renterAddress")


@strawberry.type
class FormContractResponse:
    contract_id: str = strawberry.field(name="contractID")
    contract: ContractRevision
    transaction_set: List[Dict[str, Any]] = strawberry.field(name="transactionSet")


@strawberry.input
class RHPFundInput:
    contract_id: str = strawberry.field(name="contractID")
    host_key: str = strawberry.field(name="hostKey")
    siamux_addr: str = strawberry.field(name="siamuxAddr")
    balance: str


@strawberry.input
class RHPRenewInput:
    contract_id: str = strawberry.field(name="contractID")
    end_height: int = strawberry.field(name="endHeight")
    host_key: str = strawberry.field(name="hostKey")
    host_ip: str = strawberry.field(name="hostIP")
    new_collateral: str = strawberry.field(name="newCollateral")
    renter_address: str = strawberry.field(name="renterAddress")
    renter_funds: str = strawberry.field(name="renterFunds")


@strawberry.type
class RenewedContract:
    error: str
    contract_id: str = strawberry.field(name="contractID")
    contract: ContractRevision
    transaction_set: List[Dict[str, Any]] = strawberry.field(name="transactionSet")


@strawberry.input
class RHPScanInput:
    host_ip: str = strawberry.field(name="hostIP")
    host_key: str = strawberry.field(name="hostKey")
    timeout: int


@strawberry.type
class HostSettings:
    accepting_contracts: bool = strawberry.field(name="acceptingcontracts")
    base_rpc_price: str = strawberry.field(name="baserpcprice")
    collateral: str
    contract_price: str = strawberry.field(name="contractprice")
    download_bandwidth_price: str = strawberry.field(name="downloadbandwidthprice")
    ephemeral_account_expiry: int = strawberry.field(name="ephemeralaccountexpiry")
    max_collateral: str = strawberry.field(name="maxcollateral")
    max_download_batch_size: int = strawberry.field(name="maxdownloadbatchsize")
    max_duration: int = strawberry.field(name="maxduration")
    max_ephemeral_account_balance: str = strawberry.field(name="maxephemeralaccountbalance")
    max_revise_batch_size: int = strawberry.field(name="maxrevisebatchsize")
    net_address: str = strawberry.field(name="netaddress")
    remaining_storage: int = strawberry.field(name="remainingstorage")
    revision_number: int = strawberry.field(name="revisionnumber")
    sector_access_price: str = strawberry.field(name="sectoraccessprice")
    sector_size: int = strawberry.field(name="sectorsize")
    siamux_port: str = strawberry.field(name="siamuxport")
    storage_price: str = strawberry.field(name="storageprice")
    total_storage: int = strawberry.field(name="totalstorage")
    unlock_hash: str = strawberry.field(name="unlockhash")
    upload_bandwidth_price: str = strawberry.field(name="uploadbandwidthprice")
    version: str
    window_size: int = strawberry.field(name="windowsize")


@strawberry.type
class ScanResponse:
    ping: str
    settings: HostSettings


@strawberry.input
class RHPSyncInput:
    contract_id: str = strawberry.field(name="contractID")
    host_key: str = strawberry.field(name="hostKey")
    siamux_addr: str = strawberry.field(name="siamuxAddr")


@strawberry.type
class DownloaderStats:
    avg_sector_download_speed_mbps: float = strawberry.field(name="avgSectorDownloadSpeedMbps")
    host_key: str = strawberry.field(name="hostKey")


@strawberry.type
class UploaderStats:
    host_key: str = strawberry.field(name="hostKey")
    avg_sector_upload_speed_mbps: float = strawberry.field(name="avgSectorUploadSpeedMbps")


@strawberry.type
class DownloadStats:
    avg_download_speed_mbps: float = strawberry.field(name="avgDownloadSpeedMBPS")
    avg_overdrive_pct: float = strawberry.field(name="avgOverdrivePct")
    healthy_downloaders: int = strawberry.field(name="healthyDownloaders")
    num_downloaders: int = strawberry.field(name="numDownloaders")
    downloaders_stats: List[DownloaderStats] = strawberry.field(name="downloadersStats")


@strawberry.type
class UploadStats:
    avg_slab_upload_speed_mbps: float = strawberry.field(name="avgSlabUploadSpeedMBPS")
    avg_overdrive_pct: float = strawberry.field(name="avgOverdrivePct")
    healthy_uploaders: int = strawberry.field(name="healthyUploaders")
    num_uploaders: int = strawberry.field(name="numUploaders")
    uploaders_stats: List[UploaderStats] = strawberry.field(name="uploadersStats")


# ----------------------------------------------------------------------------


from datetime import datetime, timedelta
import typing
from int import int
import strawberry
from enum import Enum
import dataclasses

# Constants
BLOCKS_PER_DAY = 144

S3_MIN_ACCESS_KEY_LEN = 16
S3_MAX_ACCESS_KEY_LEN = 128
S3_SECRET_KEY_LEN = 40


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


# Account Types
@strawberry.type
class Account:
    id: str = strawberry.field(description="ID identifies an account. It's a public key.")
    clean_shutdown: bool = strawberry.field(
        name="cleanShutdown", description="Indicates whether the account was saved during a clean shutdown"
    )
    host_key: str = strawberry.field(name="hostKey", description="Host the account was created with")
    balance: int = strawberry.field(description="Balance of the account")
    drift: int = strawberry.field(
        description="Accumulated delta between bus' tracked balance and host reported balance"
    )
    owner: str
    requires_sync: bool = strawberry.field(
        name="requiresSync", description="Indicates if account needs sync with host before use"
    )


@strawberry.type
class AccountsAddBalanceRequest:
    host_key: str = strawberry.field(name="hostKey")
    amount: int


@strawberry.type
class AccountHandlerPOST:
    host_key: str = strawberry.field(name="hostKey")


@strawberry.type
class AccountsRequiresSyncRequest:
    host_key: str = strawberry.field(name="hostKey")


@strawberry.type
class AccountsUpdateBalanceRequest:
    host_key: str = strawberry.field(name="hostKey")
    amount: int


@strawberry.type
class ContractsConfig:
    amount: int
    period: int
    renew_window: int = strawberry.field(name="renewWindow")
    download: int
    upload: int
    storage: int
    prune: bool


@strawberry.type
class HostsConfig:
    max_consecutive_scan_failures: int = strawberry.field(name="maxConsecutiveScanFailures")
    max_downtime_hours: int = strawberry.field(name="maxDowntimeHours")
    min_protocol_version: str = strawberry.field(name="minProtocolVersion")


# Autopilot Types
@strawberry.type
class AutopilotConfig:
    enabled: bool
    contracts: ContractsConfig
    hosts: HostsConfig


@strawberry.type
class AutopilotTriggerRequest:
    force_scan: bool = strawberry.field(name="forceScan")


@strawberry.type
class AutopilotTriggerResponse:
    triggered: bool


@strawberry.type
class AutopilotStateResponse:
    enabled: bool
    migrating: bool
    migrating_last_start: datetime = strawberry.field(name="migratingLastStart")
    pruning: bool
    pruning_last_start: datetime = strawberry.field(name="pruningLastStart")
    scanning: bool
    scanning_last_start: datetime = strawberry.field(name="scanningLastStart")
    uptime_ms: int = strawberry.field(name="uptimeMs")
    start_time: datetime = strawberry.field(name="startTime")


# Bucket Types
@strawberry.type
class Bucket:
    created_at: datetime = strawberry.field(name="createdAt")
    name: str
    policy: "BucketPolicy"


@strawberry.type
class BucketPolicy:
    public_read_access: bool = strawberry.field(name="publicReadAccess")


@strawberry.type
class CreateBucketOptions:
    policy: BucketPolicy


@strawberry.type
class BucketCreateRequest:
    name: str
    policy: BucketPolicy


@strawberry.type
class BucketUpdatePolicyRequest:
    policy: BucketPolicy


# Consensus Types
@strawberry.type
class ConsensusState:
    block_height: int = strawberry.field(name="blockHeight")
    last_block_time: datetime = strawberry.field(name="lastBlockTime")
    synced: bool


# Upload Types
@strawberry.type
class UploadParams:
    current_height: int = strawberry.field(name="currentHeight")
    upload_packing: bool = strawberry.field(name="uploadPacking")
    gouging_params: "GougingParams" = strawberry.field(name="gougingParams")


@strawberry.type
class GougingParams:
    consensus_state: ConsensusState = strawberry.field(name="consensusState")
    gouging_settings: "GougingSettings" = strawberry.field(name="gougingSettings")
    redundancy_settings: "RedundancySettings" = strawberry.field(name="redundancySettings")


# Contract Types
@strawberry.type
class ContractSize:
    prunable: int
    size: int


@strawberry.type
class ContractMetadata:
    id: str
    host_key: str = strawberry.field(name="hostKey")
    v2: bool
    proof_height: int = strawberry.field(name="proofHeight")
    renewed_from: str = strawberry.field(name="renewedFrom")
    revision_height: int = strawberry.field(name="revisionHeight")
    revision_number: int = strawberry.field(name="revisionNumber")
    size: int
    start_height: int = strawberry.field(name="startHeight")
    state: str
    usability: str
    window_start: int = strawberry.field(name="windowStart")
    window_end: int = strawberry.field(name="windowEnd")
    contract_price: int = strawberry.field(name="contractPrice")
    initial_renter_funds: int = strawberry.field(name="initialRenterFunds")
    spending: ContractSpending
    archival_reason: typing.Optional[str] = strawberry.field(name="archivalReason")
    renewed_to: typing.Optional[str] = strawberry.field(name="renewedTo")


@strawberry.type
class ContractPrunableData:
    id: str
    size: ContractSize


@strawberry.type
class UnhealthySlab:
    encryption_key: str = strawberry.field(name="encryptionKey")
    health: float


@strawberry.type
class SlabBuffer:
    complete: bool
    filename: str
    size: int
    max_size: int = strawberry.field(name="maxSize")
    locked: bool


# MultipartUpload Types
@strawberry.type
class MultipartUpload:
    bucket: str
    encryption_key: str = strawberry.field(name="encryptionKey")
    key: str
    upload_id: str = strawberry.field(name="uploadID")
    created_at: datetime = strawberry.field(name="createdAt")


@strawberry.type
class MultipartListPartItem:
    part_number: int = strawberry.field(name="partNumber")
    last_modified: datetime = strawberry.field(name="lastModified")
    etag: str = strawberry.field(name="eTag")
    size: int


@strawberry.type
class MultipartCompletedPart:
    part_number: int = strawberry.field(name="partNumber")
    etag: str = strawberry.field(name="eTag")


# Object Types
@strawberry.type
class ObjectMetadata:
    bucket: str
    etag: typing.Optional[str] = strawberry.field(name="eTag")
    health: float
    mod_time: datetime = strawberry.field(name="modTime")
    key: str
    size: int
    mime_type: typing.Optional[str] = strawberry.field(name="mimeType")


@strawberry.type
class Object:
    metadata: "ObjectUserMetadata"
    object_metadata: ObjectMetadata = strawberry.field(name="objectMetadata")


@strawberry.type
class ObjectUserMetadata:
    data: typing.Dict[str, str]


# Settings Types
@strawberry.type
class GougingSettings:
    max_rpc_price: int = strawberry.field(name="maxRPCPrice")
    max_contract_price: int = strawberry.field(name="maxContractPrice")
    max_download_price: int = strawberry.field(name="maxDownloadPrice")
    max_upload_price: int = strawberry.field(name="maxUploadPrice")
    max_storage_price: int = strawberry.field(name="maxStoragePrice")
    host_block_height_leeway: int = strawberry.field(name="hostBlockHeightLeeway")
    min_price_table_validity: timedelta = strawberry.field(name="minPriceTableValidity")
    min_account_expiry: timedelta = strawberry.field(name="minAccountExpiry")
    min_max_ephemeral_account_balance: int = strawberry.field(name="minMaxEphemeralAccountBalance")


@strawberry.type
class RedundancySettings:
    min_shards: int = strawberry.field(name="minShards")
    total_shards: int = strawberry.field(name="totalShards")


@strawberry.type
class UploadPackingSettings:
    enabled: bool
    slab_buffer_max_size_soft: int = strawberry.field(name="slabBufferMaxSizeSoft")


@strawberry.type
class UploadSettings:
    packing: UploadPackingSettings
    redundancy: RedundancySettings


# Host Types
@strawberry.type
class Host:
    known_since: datetime = strawberry.field(name="knownSince")
    last_announcement: datetime = strawberry.field(name="lastAnnouncement")
    public_key: str = strawberry.field(name="publicKey")
    net_address: str = strawberry.field(name="netAddress")
    scanned: bool
    blocked: bool
    stored_data: int = strawberry.field(name="storedData")
    v2_siamux_addresses: typing.List[str] = strawberry.field(name="v2SiamuxAddresses")


@strawberry.type
class HostInfo:
    public_key: str = strawberry.field(name="publicKey")
    siamux_addr: str = strawberry.field(name="siamuxAddr")
    v2_siamux_addresses: typing.List[str] = strawberry.field(name="v2SiamuxAddresses")


@strawberry.type
class HostInteractions:
    total_scans: int = strawberry.field(name="totalScans")
    last_scan: datetime = strawberry.field(name="lastScan")
    last_scan_success: bool = strawberry.field(name="lastScanSuccess")
    lost_sectors: int = strawberry.field(name="lostSectors")
    second_to_last_scan_success: bool = strawberry.field(name="secondToLastScanSuccess")
    uptime: timedelta
    downtime: timedelta
    successful_interactions: float = strawberry.field(name="successfulInteractions")
    failed_interactions: float = strawberry.field(name="failedInteractions")


# Worker Types
@strawberry.type
class DownloadStatsResponse:
    avg_download_speed_mbps: float = strawberry.field(name="avgDownloadSpeedMbps")
    avg_overdrive_pct: float = strawberry.field(name="avgOverdrivePct")
    healthy_downloaders: int = strawberry.field(name="healthyDownloaders")
    num_downloaders: int = strawberry.field(name="numDownloaders")
    downloaders_stats: typing.List["DownloaderStats"] = strawberry.field(name="downloadersStats")


@strawberry.type
class UploadStatsResponse:
    avg_slab_upload_speed_mbps: float = strawberry.field(name="avgSlabUploadSpeedMbps")
    avg_overdrive_pct: float = strawberry.field(name="avgOverdrivePct")
    healthy_uploaders: int = strawberry.field(name="healthyUploaders")
    num_uploaders: int = strawberry.field(name="numUploaders")
    uploaders_stats: typing.List["UploaderStats"] = strawberry.field(name="uploadersStats")
