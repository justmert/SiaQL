from typing import List, Optional, Union
from strawberry.types import Info
import strawberry
import datetime
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from strawberry.scalars import JSON
from typing import List, Optional, Dict, Any
from enum import Enum
from strawberry.types.enum import EnumDefinition

from dataclasses import dataclass
from typing import Type, TypeVar, get_type_hints, Optional, get_origin, get_args

# from strawberry.field import StrawberryField
from functools import wraps
from dataclasses import dataclass, fields

T = TypeVar("T")

# Cache for input types
_input_type_cache: Dict[str, Any] = {}


def is_valid_input_type(field_type):
    """Check if a type can be used as input"""
    basic_types = (str, int, float, bool, datetime.datetime, datetime.date)

    # Handle Strawberry Optional types
    if isinstance(field_type, strawberry.types.base.StrawberryOptional):
        return is_valid_input_type(field_type.of_type)

    # Handle Strawberry List type
    if isinstance(field_type, strawberry.types.base.StrawberryList):
        return is_valid_input_type(field_type.of_type)

    # Handle standard Optional and List
    origin = get_origin(field_type)
    if origin in (Optional, list):
        args = get_args(field_type)
        if not args:
            return False
        return is_valid_input_type(args[0])

    # Handle scalar wrappers
    if isinstance(field_type, strawberry.types.scalar.ScalarWrapper):
        return True

    # Handle Enums (Strawberry EnumDefinition)
    if isinstance(field_type, EnumDefinition):
        return True

    # Handle SiaType subclasses
    if isinstance(field_type, type) and issubclass(field_type, SiaType):
        return True

    # Check basic types (exact match)
    if field_type in basic_types:
        return True

    return False


def _process_field_type(field_type):
    """Process field type to handle Optional and List types"""
    # Handle Strawberry Enum definitions first
    if isinstance(field_type, EnumDefinition):
        return field_type.wrapped_cls  # Return original Enum class

    # Handle Strawberry Optional
    if isinstance(field_type, strawberry.types.base.StrawberryOptional):
        processed_type = _process_field_type(field_type.of_type)
        return Optional[processed_type]

    # Handle Strawberry List
    if isinstance(field_type, strawberry.types.base.StrawberryList):
        inner_type = _process_field_type(field_type.of_type)
        return List[inner_type]

    # Handle ScalarWrapper
    if isinstance(field_type, strawberry.types.scalar.ScalarWrapper):
        return str  # Convert scalars to strings for input types

    # Handle standard Optional and List
    origin = get_origin(field_type)
    if origin in (Optional, list):
        args = get_args(field_type)
        if not args:
            return field_type
        base_type = _process_field_type(args[0])
        if origin is Optional:
            return Optional[base_type]
        return List[base_type]

    # Handle SiaType subclasses
    if isinstance(field_type, type) and issubclass(field_type, SiaType):
        input_type = field_type.Input
        return input_type if input_type is not None else str

    return field_type


def create_input_type(cls: Type[T]) -> Optional[Type[T]]:
    """Create an input version of a type"""
    cache_key = f"{cls.__module__}.{cls.__name__}"
    if cache_key in _input_type_cache:
        return _input_type_cache[cache_key]

    class_dict = {}
    annotations = {}

    # Get Strawberry fields which contain the metadata
    strawberry_fields = cls.__strawberry_definition__.fields

    # Process fields
    for field in fields(cls):
        if not is_valid_input_type(field.type):
            print(f"Field {field.name} failed validation")
            continue

        try:
            field_type = _process_field_type(field.type)
            if isinstance(field_type, strawberry.types.base.StrawberryOptional):
                field_type = Optional[field_type.of_type]

            annotations[field.name] = field_type

            # Get the corresponding Strawberry field
            strawberry_field = next((f for f in strawberry_fields if f.python_name == field.name), None)

            if strawberry_field:
                field_kwargs = {
                    "name": strawberry_field.graphql_name,
                    "description": strawberry_field.description,
                    "default": None,
                }
            else:
                field_kwargs = {"name": field.name, "default": None}

            class_dict[field.name] = strawberry.field(**field_kwargs)

        except Exception as e:
            print(f"Exception processing field {field.name}: {e}")
            continue

    if not annotations:
        print("No valid annotations found")
        return None

    # Add dict method to the class_dict
    def dict(self) -> Dict[str, Any]:
        result = {}
        for field_name, field_value in self.__dict__.items():
            # Get the field object to access metadata
            field_obj = next((f for f in fields(self.__class__) if f.name == field_name), None)
            if field_obj:
                # Get JSON field name from strawberry metadata
                json_name = field_obj.graphql_name if hasattr(field, "graphql_name") else field_obj.name
                # Skip None values
                if field_value is None:
                    continue

                # Handle nested objects
                if hasattr(field_value, "dict"):
                    result[json_name] = field_value.dict()
                # Handle lists
                elif isinstance(field_value, list):
                    result[json_name] = [item.dict() if hasattr(item, "dict") else item for item in field_value]
                # Handle other values directly
                else:
                    result[json_name] = field_value
        return result

    class_dict["dict"] = dict

    # Create the input type class
    input_cls = type(
        f"{cls.__name__}Input", (), {"__annotations__": annotations, **class_dict, "__module__": cls.__module__}
    )

    # Apply strawberry input decorator
    input_cls = strawberry.input(input_cls)

    _input_type_cache[cache_key] = input_cls
    return input_cls


@strawberry.type
class SiaType:
    """Base class for all Sia types"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Any:
        """Convert dictionary data to this type"""
        if not isinstance(data, dict):
            return data
        result = {}
        for field in fields(cls):
            field_name = field.name
            json_name = field.metadata.get("strawberry", {}).get("name", field_name)

            if json_name in data:
                result[field_name] = data[json_name]
        return result

    @classmethod
    @property
    def Input(cls) -> Type:
        """Dynamically create and cache input type when accessed"""
        cache_key = f"{cls.__module__}.{cls.__name__}"

        if cache_key not in _input_type_cache:
            input_type = create_input_type(cls)
            if input_type is not None:
                _input_type_cache[cache_key] = input_type

        return _input_type_cache.get(cache_key)

    # def dict(self) -> Dict[str, Any]:
    #     """Convert to dictionary for JSON serialization"""
    #     result = {}
    #     for field in fields(self.__class__):
    #         # Get the JSON field name from strawberry metadata
    #         field_name = field.name
    #         json_name = field.metadata.get("strawberry", {}).get("name", field_name)

    #         # Get the field value
    #         value = getattr(self, field_name)

    #         # Skip None values
    #         if value is None:
    #             continue

    #         # Handle nested SiaTypes
    #         if isinstance(value, SiaType):
    #             result[json_name] = value.dict()
    #         # Handle lists
    #         elif isinstance(value, list):
    #             result[json_name] = [
    #                 item.dict() if isinstance(item, SiaType) else str(item) if hasattr(item, '__strawberry_scalar__') else item
    #                 for item in value if item is not None
    #             ]
    #         # Handle scalar types (like PublicKey)
    #         elif hasattr(value, '__strawberry_scalar__'):
    #             result[json_name] = str(value)
    #         else:
    #             result[json_name] = value

    #     return result


# ****************************************


@strawberry.scalar(
    description="An unsigned amount of Hastings, the smallest unit of currency in Sia. 1 Siacoin (SC) equals 10^24 Hastings (H). | Pattern: ^\d+$ | Max length: 39"
)
class Currency(str):
    @classmethod
    def parse_value(cls, value: str) -> "Currency":
        return cls(value)

    @classmethod
    def serialize(cls, value: "Currency") -> str:
        return str(value)


@strawberry.scalar(description="A unique identifier for a file contract | Pattern: ^fcid:[0-9a-fA-F]{64}$")
class FileContractID(str):
    @classmethod
    def parse_value(cls, value: str) -> "FileContractID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "FileContractID") -> str:
        return str(value)


@strawberry.scalar(description="A 256-bit blake2b hash | Pattern: ^[0-9a-fA-F]{64}$")
class Hash256(str):
    @classmethod
    def parse_value(cls, value: str) -> "Hash256":
        return cls(value)

    @classmethod
    def serialize(cls, value: "Hash256") -> str:
        return str(value)


@strawberry.scalar(description="A ed25519 public key | Pattern: ^ed25519:[0-9a-fA-F]{64}$")
class PublicKey(str):
    @classmethod
    def parse_value(cls, value: str) -> "PublicKey":
        return cls(value)

    @classmethod
    def serialize(cls, value: "PublicKey") -> str:
        return str(value)


@strawberry.scalar(description="A ed25519 signature | Pattern: [0-9a-fA-F]{64}")
class Signature(str):
    @classmethod
    def parse_value(cls, value: str) -> "Signature":
        return cls(value)

    @classmethod
    def serialize(cls, value: "Signature") -> str:
        return str(value)


@strawberry.scalar(
    description="A signed amount of Hastings, the smallest unit of currency in Sia. 1 Siacoin (SC) equals 10^24 Hastings (H). | Pattern: ^-?\d+$ | Max length: 39"
)
class SignedCurrency(str):
    @classmethod
    def parse_value(cls, value: str) -> "SignedCurrency":
        return cls(value)

    @classmethod
    def serialize(cls, value: "SignedCurrency") -> str:
        return str(value)


@strawberry.scalar(description="The height of a block")
class BlockHeight(int):
    @classmethod
    def parse_value(cls, value: int) -> "BlockHeight":
        return cls(value)

    @classmethod
    def serialize(cls, value: "BlockHeight") -> int:
        return int(value)


@strawberry.scalar(description="The name of the bucket")
class BucketName(str):
    @classmethod
    def parse_value(cls, value: str) -> "BucketName":
        return cls(value)

    @classmethod
    def serialize(cls, value: "BucketName") -> str:
        return str(value)


@strawberry.scalar(description="time.Duration")
class Duration(int):
    @classmethod
    def parse_value(cls, value: int) -> "DurationMS":
        return cls(value)

    @classmethod
    def serialize(cls, value: "DurationMS") -> int:
        return int(value)


@strawberry.scalar(description="A duration in millisecond")
class DurationMS(int):
    @classmethod
    def parse_value(cls, value: int) -> "DurationMS":
        return cls(value)

    @classmethod
    def serialize(cls, value: "DurationMS") -> int:
        return int(value)


@strawberry.scalar(description="A duration in hours  ")
class DurationH(int):
    @classmethod
    def parse_value(cls, value: int) -> "DurationH":
        return cls(value)

    @classmethod
    def serialize(cls, value: "DurationH") -> int:
        return int(value)


@strawberry.scalar(
    description="A key used to encrypt and decrypt data. The key is either a regular key (key) or a salted key (skey). The latter requires a seed to be used for encryption and decryption. | Pattern: ^(key|skey):[0-9a-fA-F]{64}$"
)
class EncryptionKey(str):
    @classmethod
    def parse_value(cls, value: str) -> "EncryptionKey":
        return cls(value)

    @classmethod
    def serialize(cls, value: "EncryptionKey") -> str:
        return str(value)


@strawberry.scalar(description="An ETag representing a resource | Pattern: ^(W/)?" "$ ")
class ETag(str):
    @classmethod
    def parse_value(cls, value: str) -> "ETag":
        return cls(value)

    @classmethod
    def serialize(cls, value: "ETag") -> str:
        return str(value)


@strawberry.scalar(description="A unique identifier for a multipart upload | Pattern: ^[0-9a-fA-F]{64}$")
class MultipartUploadID(str):
    @classmethod
    def parse_value(cls, value: str) -> "MultipartUploadID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "MultipartUploadID") -> str:
        return str(value)


@strawberry.scalar(description="The revision number of the contract")
class RevisionNumber(int):
    @classmethod
    def parse_value(cls, value: int) -> "RevisionNumber":
        return cls(value)

    @classmethod
    def serialize(cls, value: "RevisionNumber") -> int:
        return int(value)


@strawberry.scalar(
    description="Represents a semantic version as an array of three unsigned 8-bit integers: [major, minor, patch]"
)
class SemVer(List[int]):
    @classmethod
    def parse_value(cls, value: List[int]) -> "SemVer":
        return cls(value)

    @classmethod
    def serialize(cls, value: "SemVer") -> List[int]:
        return value


@strawberry.scalar(description="A 16-byte unique identifier represented as a hex string.")
class SettingsID(str):
    @classmethod
    def parse_value(cls, value: str) -> "SettingsID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "SettingsID") -> str:
        return str(value)


@strawberry.scalar(description="A 32-byte unique identifier represented as a hex string.")
class UploadID(str):
    @classmethod
    def parse_value(cls, value: str) -> "UploadID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "UploadID") -> str:
        return str(value)


@strawberry.scalar(description="The address of the syncer ")
class SyncerAddress(str):
    @classmethod
    def parse_value(cls, value: str) -> "SyncerAddress":
        return cls(value)

    @classmethod
    def serialize(cls, value: "SyncerAddress") -> str:
        return str(value)


# @strawberry.scalar()
# class TimeRFC3339(str):
#     @classmethod
#     def parse_value(cls, value: str) -> "SyncerAddress":
#         return cls(value)

#     @classmethod
#     def serialize(cls, value: "SyncerAddress") -> str:
#         return str(value)


@strawberry.scalar(description="Unique identifier for a Siacoin output.")
class SiacoinOutputID(str):
    @classmethod
    def parse_value(cls, value: str) -> "SiacoinOutputID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "SiacoinOutputID") -> str:
        return str(value)


@strawberry.scalar(description="Unique identifier for a Siafund output.")
class SiafundOutputID(str):
    @classmethod
    def parse_value(cls, value: str) -> "SiafundOutputID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "SiafundOutputID") -> str:
        return str(value)


@strawberry.scalar(description="Unique identifier for a transaction.")
class TransactionID(str):
    @classmethod
    def parse_value(cls, value: str) -> "TransactionID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "TransactionID") -> str:
        return str(value)


@strawberry.scalar(description="The hash of a set of UnlockConditions | Pattern: ^[0-9a-fA-F]{64}$")
class Address(str):
    @classmethod
    def parse_value(cls, value: str) -> "Address":
        return cls(value)

    @classmethod
    def serialize(cls, value: "Address") -> str:
        return str(value)


@strawberry.scalar(description="A unique identifier for a block")
class BlockID(str):
    @classmethod
    def parse_value(cls, value: str) -> "BlockID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "BlockID") -> str:
        return str(value)


@strawberry.scalar(description="// A Specifier is a fixed-size, 0-padded identifier")
class Specifier(str):
    @classmethod
    def parse_value(cls, value: str) -> "BlockID":
        return cls(value)

    @classmethod
    def serialize(cls, value: "BlockID") -> str:
        return str(value)


@strawberry.type
class StateElement(SiaType):
    leaf_index: int = strawberry.field(description="The index of the element in the Merkle tree", name="leafIndex")
    merkle_proof: Optional[List[Hash256]] = strawberry.field(
        description="The Merkle proof demonstrating the inclusion of the leaf", name="merkleProof"
    )


@strawberry.type
class CoveredFields(SiaType):
    whole_transaction: Optional[bool] = strawberry.field(
        description="Whether the whole transaction is covered by the signature", name="wholeTransaction"
    )
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
    algorithm: Optional[Specifier] = strawberry.field(
        description="A fixed 16-byte array that specifies the algorithm used to generatethe key",
        name="algorithm",
    )
    key: Optional[str] = strawberry.field(
        description="A 32-byte key represented as a hex-encoded string. Must be exactly64 characters long, containing only hexadecimal digits | Pattern: ^[a-fA-F0-9]{64}$",
        name="key",
    )


@strawberry.type
class UnlockConditions(SiaType):
    timelock: Optional[int] = strawberry.field(
        description="The block height at which the outputs can be spent", name="timelock"
    )
    public_keys: Optional[List[UnlockKey]] = strawberry.field(name="publicKeys")
    signatures_required: Optional[int] = strawberry.field(
        description="The number of signatures required to spend the output", name="signaturesRequired"
    )


@strawberry.type
class Account(SiaType):
    id: Optional[PublicKey] = strawberry.field(description="The account's ID", name="id")  # rhpv3.Account
    clean_shutdown: Optional[bool] = strawberry.field(
        description="Whether the account has been cleanly shutdown. If not, the account will require a sync with the host.",
        name="cleanShutdown",
    )
    host_key: Optional[PublicKey] = strawberry.field(description="The host's public key", name="hostKey")
    balance: Optional[int] = strawberry.field(
        description="The account's balance as expected by the worker", name="balance"
    )
    drift: Optional[int] = strawberry.field(
        description="The accumulated drift between the worker's expected balance and the host's actual balance. Used to track if a host is trying to cheat the renter over time.",
        name="drift",
    )
    owner: Optional[str] = strawberry.field(
        description="The owner of the account that manages it. This is the id of the worker that maintains the account. | Min length: 1",
        name="owner",
    )
    requires_sync: Optional[bool] = strawberry.field(
        description="Whether the account requires a sync with the host. This is usually the case when the host reports insufficient balance for an account that the worker still believes to be funded.",
        name="requiresSync",
    )


@strawberry.type
class Attestation(SiaType):
    public_key: Optional[PublicKey] = strawberry.field(name="publicKey")
    key: Optional[str] = strawberry.field(name="key")
    value: Optional[str] = strawberry.field(name="value")
    signature: Optional[Signature] = strawberry.field(name="signature")


@strawberry.type
class ContractsConfig(SiaType):
    set: Optional[str] = strawberry.field(name="set")
    amount: Optional[int] = strawberry.field(description="The minimum number of contracts to form", name="amount")
    allowance: Optional[Currency] = strawberry.field(name="allowance")
    period: Optional[int] = strawberry.field(
        description="The length of a contract's period in blocks (1 block being 10 minutes on average)",
        name="period",
    )
    renew_window: Optional[int] = strawberry.field(
        description="The number of blocks before the end of a contract that a contract should be renewed",
        name="renewWindow",
    )
    download: Optional[int] = strawberry.field(
        description="Expected download bandwidth used per period in bytes", name="download"
    )
    upload: Optional[int] = strawberry.field(
        description="Expected upload bandwidth used per period in bytes", name="upload"
    )
    storage: Optional[int] = strawberry.field(description="Expected amount of data stored in bytes", name="storage")
    prune: Optional[bool] = strawberry.field(
        description="Whether to automatically prune deleted data from contracts", name="prune"
    )


@strawberry.type
class HostsConfig(SiaType):
    allow_redundant_ips: Optional[bool] = strawberry.field(
        description="Whether to allow hosts with redundant IPs", name="allowRedundantIPs"
    )
    max_downtime_hours: Optional[int] = strawberry.field(
        description="The maximum number of hours a host can be offline before it is removed from the database",
        name="maxDowntimeHours",
    )
    min_protocol_version: Optional[str] = strawberry.field(
        description="The minimum supported protocol version of a host to be considered good", name="minProtocolVersion"
    )
    max_consecutive_scan_failures: Optional[int] = strawberry.field(
        description="The maximum number of consecutive scan failures before a host is removed from the database",
        name="maxConsecutiveScanFailures",
    )
    score_overrides: Optional[JSON] = strawberry.field(
        description="Map of host public keys to score override values", name="scoreOverrides"
    )  # Dict[PublicKey, float]


@strawberry.type
class AutopilotConfig(SiaType):
    """Contains all autopilot configuration."""

    contracts: Optional[ContractsConfig] = strawberry.field(
        description="Contract configuration settings", name="contracts"
    )
    hosts: Optional[HostsConfig] = strawberry.field(description="Host configuration settings", name="hosts")


@strawberry.type
class Autopilot(SiaType):
    id: Optional[str] = strawberry.field(description="The identifier of the autopilot", name="id")
    config: Optional[AutopilotConfig] = strawberry.field(
        description="The configuration of the autopilot", name="config"
    )
    current_period: Optional[int] = strawberry.field(description="The current period number", name="currentPeriod")


@strawberry.type
class SiacoinOutput(SiaType):
    value: Optional[Currency] = strawberry.field(description="The amount of Siacoins in the output", name="value")
    address: Optional[Address] = strawberry.field(name="address")


# @strawberry.type(description="A storage agreement between a renter and a host.")
@strawberry.type
class FileContract(SiaType):
    filesize: Optional[int] = strawberry.field(description="The size of the contract in bytes.", name="filesize")
    file_merkle_root: Optional[Hash256] = strawberry.field(
        description="The Merkle root of the contract's data.", name="fileMerkleRoot"
    )
    window_start: Optional[int] = strawberry.field(
        description="The block height when the contract's proof window starts.", name="windowStart"
    )
    window_end: Optional[int] = strawberry.field(
        description="The block height when the contract's proof window ends.", name="windowEnd"
    )
    payout: Optional[Currency] = strawberry.field(description="The total payout for the contract.", name="payout")
    valid_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="List of outputs created if the contract is successfully fulfilled.", name="validProofOutputs"
    )
    missed_proof_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="List of outputs created if the contract is not fulfilled.", name="missedProofOutputs"
    )
    unlock_hash: Optional[Address] = strawberry.field(name="unlockHash")
    revision_number: Optional[RevisionNumber] = strawberry.field(name="revisionNumber")


@strawberry.type
class FileContractRevision(SiaType):
    parent_id: Optional[FileContractID] = strawberry.field(name="parentID")
    unlock_conditions: Optional[UnlockConditions] = strawberry.field(name="unlockConditions")


@strawberry.type
class SiacoinInput(SiaType):
    parent_id: Optional[SiacoinOutputID] = strawberry.field(
        description="The ID of the output being spent", name="parentID"
    )
    unlock_conditions: Optional[UnlockConditions] = strawberry.field(
        description="The unlock conditions required to spend the output", name="unlockConditions"
    )


# @strawberry.type(description="Represents an input used to spend an unspent Siafund output.")
@strawberry.type
class SiafundInput(SiaType):
    parent_id: Optional[SiafundOutputID] = strawberry.field(
        description="The ID of the parent Siafund output being spent.", name="parentID"
    )
    unlock_conditions: Optional[UnlockConditions] = strawberry.field(
        description="The conditions required to unlock the parent Siafund output.", name="unlockConditions"
    )
    claim_address: Optional[Address] = strawberry.field(
        description="The address receiving the Siacoin claim generated by the Siafund output.", name="claimAddress"
    )


# @strawberry.type(description="Represents an output created to distribute Siafund.")
@strawberry.type
class SiafundOutput(SiaType):
    value: Optional[int] = strawberry.field(description="The amount of Siafund in the output.", name="value")
    address: Optional[Address] = strawberry.field(description="The address receiving the Siafund.", name="address")


# @strawberry.type(description="Represents a proof of storage for a file contract.")
@strawberry.type
class StorageProof(SiaType):
    parent_id: Optional[FileContractID] = strawberry.field(
        description="The ID of the file contract being proven.", name="parentID"
    )
    leaf: Optional[str] = strawberry.field(
        description="The selected leaf from the Merkle tree of the file's data.", name="leaf"
    )
    proof: Optional[List[Hash256]] = strawberry.field(
        description="The Merkle proof demonstrating the inclusion of the leaf.", name="proof"
    )


@strawberry.type
class TransactionSignature(SiaType):
    parent_id: Optional[Hash256] = strawberry.field(
        description="The ID of the transaction being signed", name="parentID"
    )
    public_key_index: Optional[int] = strawberry.field(
        description="The index of the public key used to sign the transaction", name="publicKeyIndex"
    )
    timelock: Optional[int] = strawberry.field(
        description="The block height at which the outputs in the transaction can be spent", name="timelock"
    )
    covered_fields: Optional[CoveredFields] = strawberry.field(
        description="Indicates which fields of the transaction are covered by the signature", name="coveredFields"
    )
    signature: Optional[Signature] = strawberry.field(description="The signature of the transaction", name="signature")


@strawberry.type
class Transaction(SiaType):
    siacoin_inputs: Optional[List[SiacoinInput]] = strawberry.field(
        description="List of Siacoin inputs used in the transaction.", name="siacoinInputs"
    )
    siacoin_outputs: Optional[List[SiacoinOutput]] = strawberry.field(
        description="List of Siacoin outputs created by the transaction.", name="siacoinOutputs"
    )
    file_contracts: Optional[List[FileContract]] = strawberry.field(
        description="List of file contracts created by the transaction.", name="fileContracts"
    )
    file_contract_revisions: Optional[List[FileContractRevision]] = strawberry.field(
        description="List of revisions to existing file contracts included in the transaction.",
        name="fileContractRevisions",
    )
    storage_proofs: Optional[List[StorageProof]] = strawberry.field(
        description="List of storage proofs asserting the storage of data for file contracts.", name="storageProofs"
    )
    siafund_inputs: Optional[List[SiafundInput]] = strawberry.field(
        description="List of Siafund inputs spent in the transaction.", name="siafundInputs"
    )
    siafund_outputs: Optional[List[SiafundOutput]] = strawberry.field(
        description="List of Siafund outputs created by the transaction.", name="siafundOutputs"
    )
    miner_fees: Optional[List[Currency]] = strawberry.field(
        description="List of miner fees included in the transaction.", name="minerFees"
    )
    arbitrary_data: Optional[List[str]] = strawberry.field(
        description="Arbitrary binary data included in the transaction.", name="arbitraryData"
    )
    signatures: Optional[List[TransactionSignature]] = strawberry.field(
        description="List of cryptographic signatures verifying the transaction.", name="signatures"
    )


@strawberry.type
class V2FileContract(SiaType):
    capacity: Optional[int] = strawberry.field(name="capacity")
    filesize: Optional[int] = strawberry.field(name="filesize")
    file_merkle_root: Optional[Hash256] = strawberry.field(name="fileMerkleRoot")
    proof_height: Optional[int] = strawberry.field(name="proofHeight")
    expiration_height: Optional[int] = strawberry.field(name="expirationHeight")
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
    state_element: Optional[StateElement] = strawberry.field(
        description="The state of the element", name="stateElement"
    )
    v2_file_contract: Optional[V2FileContract] = strawberry.field(name="v2FileContract")


@strawberry.type
class V2FileContractResolution(SiaType):
    parent: Optional[V2FileContractElement] = strawberry.field(name="parent")
    resolution: Optional[JSON] = strawberry.field(
        name="resolution"
    )  # type V2FileContractResolutionType interface {isV2FileContractResolution()


@strawberry.type
class V2FileContractRevision(SiaType):
    parent: Optional[V2FileContractElement] = strawberry.field(name="parent")
    revision: Optional[V2FileContract] = strawberry.field(name="revision")


@strawberry.type
class SatisfiedPolicy(SiaType):
    policy: Optional[JSON] = strawberry.field(name="policy")  # SpendPolicy
    signature: Optional[List[Signature]] = strawberry.field(name="signature")
    preimages: Optional[List[str]] = strawberry.field(name="preimages")


@strawberry.type
class SiacoinElement(SiacoinOutput):
    id: Optional[SiacoinOutputID] = strawberry.field(description="The ID of the element", name="id")
    maturity_height: Optional[int] = strawberry.field(
        description="The block height when the output matures", name="maturityHeight"
    )


@strawberry.type
class V2SiacoinInput(SiaType):
    parent: Optional[SiacoinElement] = strawberry.field(name="parent")
    satisfied_policy: Optional[SatisfiedPolicy] = strawberry.field(name="satisfiedPolicy")


@strawberry.type
class SiafundElement(SiaType):
    id: Optional[SiafundOutputID] = strawberry.field(description="The ID of the element", name="id")
    state_element: Optional[StateElement] = strawberry.field(
        description="The state of the element", name="stateElement"
    )
    siafund_output: Optional[SiafundOutput] = strawberry.field(
        description="The output of the element", name="siafundOutput"
    )
    claim_start: Optional[Currency] = strawberry.field(
        description="value of SiafundTaxRevenue when element was created", name="claimStart"
    )


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
    file_contract_resolutions: Optional[List[V2FileContractResolution]] = strawberry.field(
        name="fileContractResolutions"
    )
    attestations: Optional[List[Attestation]] = strawberry.field(name="attestations")
    arbitrary_data: Optional[List[str]] = strawberry.field(name="arbitraryData")
    new_foundation_address: Optional[Address] = strawberry.field(name="newFoundationAddress")
    miner_fee: Optional[Currency] = strawberry.field(name="minerFee")


@strawberry.type
class V2BlockData(SiaType):
    height: Optional[int] = strawberry.field(description="The height of the block", name="height")
    commitment: Optional[Hash256] = strawberry.field(name="commitment")
    transactions: Optional[List[V2Transaction]] = strawberry.field(name="transactions")


@strawberry.type
class Block(SiaType):
    parent_id: Optional[BlockID] = strawberry.field(description="The ID of the parent block", name="parentID")
    nonce: Optional[int] = strawberry.field(description="The nonce used to mine the block", name="nonce")
    timestamp: Optional[datetime.datetime] = strawberry.field(
        description="The time the block was mined", name="timestamp"
    )
    miner_payouts: Optional[List[SiacoinOutput]] = strawberry.field(name="minerPayouts")
    transactions: Optional[List[Transaction]] = strawberry.field(name="transactions")
    v2: Optional[V2BlockData] = strawberry.field(name="v2")


@strawberry.type
class BucketPolicy(SiaType):
    public_read_access: Optional[bool] = strawberry.field(
        description="Indicates if the bucket is publicly readable", name="publicReadAccess"
    )


@strawberry.type
class Bucket(SiaType):
    created_at: Optional[datetime.datetime] = strawberry.field(
        description="The time the bucket was created", name="createdAt"
    )  # datetime.datetime
    name: Optional[str] = strawberry.field(name="name")
    policy: Optional[BucketPolicy] = strawberry.field(name="policy")  # change to JSON if it creates problem


@strawberry.type
class BuildState(SiaType):
    version: Optional[str] = strawberry.field(description="The version of the build", name="version")
    commit: Optional[str] = strawberry.field(description="The commit hash of the build", name="commit")
    os: Optional[str] = strawberry.field(description="The operating system of the build", name="os")
    build_time: Optional[datetime.datetime] = strawberry.field(
        description="The build time of the build", name="buildTime"
    )


@strawberry.type
class ChainIndex(SiaType):
    height: Optional[int] = strawberry.field(description="The height of the block in the blockchain", name="height")
    id: Optional[BlockID] = strawberry.field(description="The ID of the block", name="id")


@strawberry.type
class GougingSettings(SiaType):
    max_rpc_price: Optional[Currency] = strawberry.field(
        description="The maximum base price a host can charge per RPC", name="maxRPCPrice"
    )
    max_contract_price: Optional[Currency] = strawberry.field(
        description="The maximum price a host can charge for a contract formation", name="maxContractPrice"
    )
    max_download_price: Optional[Currency] = strawberry.field(
        description="The maximum price a host can charge for downloading in hastings / byte", name="maxDownloadPrice"
    )
    max_upload_price: Optional[Currency] = strawberry.field(
        description="The maximum price a host can charge for uploading in hastings / byte", name="maxUploadPrice"
    )
    max_storage_price: Optional[Currency] = strawberry.field(
        description="The maximum price a host can charge for storage in hastings / byte / block", name="maxStoragePrice"
    )
    host_block_height_leeway: Optional[int] = strawberry.field(
        description="The number of blocks a host's chain's height can diverge from our own before we stop using it",
        name="hostBlockHeightLeeway",
    )
    min_price_table_validity: Optional[Duration] = strawberry.field(
        description="The time a host's price table should be valid after acquiring it in milliseconds",
        name="minPriceTableValidity",
    )
    min_account_expiry: Optional[Duration] = strawberry.field(
        description="The minimum amount of time an account on a host can be idle for before expiring",
        name="minAccountExpiry",
    )
    min_max_ephemeral_account_balance: Optional[Currency] = strawberry.field(
        description="The minimum max balance a host should allow us to fund an account with",
        name="minMaxEphemeralAccountBalance",
    )
    migration_surcharge_multiplier: Optional[int] = strawberry.field(
        description="The multiplier for the migration surcharge", name="migrationSurchargeMultiplier"
    )


@strawberry.type
class ConfigRecommendation(SiaType):
    gouging_settings: Optional[GougingSettings] = strawberry.field(name="gougingSettings")


@strawberry.type
class ConsensusState(SiaType):
    block_height: Optional[int] = strawberry.field(description="The current block height", name="blockHeight")
    last_block_time: Optional[datetime.datetime] = strawberry.field(
        description="The time of the last block", name="lastBlockTime"
    )
    synced: Optional[bool] = strawberry.field(description="Whether the node is synced with the network", name="synced")


@strawberry.type
class ContractSpending(SiaType):
    uploads: Optional[Currency] = strawberry.field(name="uploads")
    downloads: Optional[Currency] = strawberry.field(name="downloads")
    fund_account: Optional[Currency] = strawberry.field(name="fundAccount")
    deletions: Optional[Currency] = strawberry.field(name="deletions")
    sector_roots: Optional[Currency] = strawberry.field(name="sectorRoots")


@strawberry.type
class ArchivedContract(SiaType):
    id: Optional[FileContractID] = strawberry.field(description="The unique identifier for the contract", name="id")
    host_ip: Optional[str] = strawberry.field(description="The IP address of the host", name="hostIP")
    host_key: Optional[PublicKey] = strawberry.field(description="The public key of the host", name="hostKey")
    renewed_to: Optional[FileContractID] = strawberry.field(
        description="The ID of the contract this was renewed to", name="renewedTo"
    )
    spending: Optional[ContractSpending] = strawberry.field(description="Contract spending details", name="spending")

    archival_reason: Optional[str] = strawberry.field(
        description="The reason the contract was archived", name="archivalReason"
    )
    contract_price: Optional[Currency] = strawberry.field(
        description="The price of forming the contract", name="contractPrice"
    )
    proof_height: Optional[int] = strawberry.field(
        description="The height at which the storage proof needs to be submitted", name="proofHeight"
    )
    renewed_from: Optional[FileContractID] = strawberry.field(
        description="The ID of the contract this was renewed from", name="renewedFrom"
    )
    revision_height: Optional[int] = strawberry.field(
        description="The height of the latest revision", name="revisionHeight"
    )
    revision_number: Optional[int] = strawberry.field(
        description="The revision number of the contract", name="revisionNumber"
    )
    size: Optional[int] = strawberry.field(description="The size of the contract in bytes", name="size")
    start_height: Optional[int] = strawberry.field(
        description="The height at which the contract was created", name="startHeight"
    )
    state: Optional[str] = strawberry.field(description="The state of the contract", name="state")
    total_cost: Optional[Currency] = strawberry.field(description="The total cost of the contract", name="totalCost")
    window_start: Optional[int] = strawberry.field(
        description="The height at which the proof window starts", name="windowStart"
    )
    window_end: Optional[int] = strawberry.field(
        description="The height at which the proof window ends", name="windowEnd"
    )


@strawberry.type
class ContractMetadata(SiaType):
    id: Optional[FileContractID] = strawberry.field(
        description="The unique identifier for the file contract.", name="id"
    )
    host_ip: Optional[str] = strawberry.field(name="hostIP")
    host_key: Optional[PublicKey] = strawberry.field(description="The public key of the host.", name="hostKey")
    siamux_addr: Optional[str] = strawberry.field(name="siamuxAddr")

    proof_height: Optional[int] = strawberry.field(
        description="The height at which the storage proof needs to be submitted", name="proofHeight"
    )
    revision_height: Optional[int] = strawberry.field(
        description="The block height of the latest revision", name="revisionHeight"
    )
    revision_number: Optional[RevisionNumber] = strawberry.field(
        description="The current revision number of the contract", name="revisionNumber"
    )
    size: Optional[int] = strawberry.field(description="The size of the contract in bytes", name="size")
    start_height: Optional[int] = strawberry.field(
        description="The block height at which the contract created", name="startHeight"
    )
    state: Optional[str] = strawberry.field(
        description="The state of the contract | Allowed values: pending, active, complete, failed", name="state"
    )
    window_start: Optional[int] = strawberry.field(
        description="The block height when the contract's proof window starts.", name="windowStart"
    )
    window_end: Optional[int] = strawberry.field(
        description="The block height when the contract's proof window ends.", name="windowEnd"
    )

    contract_price: Optional[Currency] = strawberry.field(
        description="The price of forming the contract.", name="contractPrice"
    )
    renewed_from: Optional[FileContractID] = strawberry.field(
        description="The ID of the contract this one was renewed from", name="renewedFrom"
    )
    spending: Optional[ContractSpending] = strawberry.field(
        description="Costs and spending details of the contract.", name="spending"
    )
    total_cost: Optional[Currency] = strawberry.field(name="totalCost")

    contract_sets: Optional[List[str]] = strawberry.field(name="contractSets")


@strawberry.type
class Contract(ContractMetadata):
    revision: Optional[FileContractRevision] = strawberry.field(name="revision")


@strawberry.type
class ContractMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(name="timestamp")

    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")

    remaining_collateral: Optional[Currency] = strawberry.field(name="remainingCollateral")
    remaining_funds: Optional[Currency] = strawberry.field(name="remainingFunds")
    revision_number: Optional[int] = strawberry.field(name="revisionNumber")

    upload_spending: Optional[Currency] = strawberry.field(name="uploadSpending")
    download_spending: Optional[Currency] = strawberry.field(name="downloadSpending")
    fund_account_spending: Optional[Currency] = strawberry.field(name="fundAccountSpending")
    delete_spending: Optional[Currency] = strawberry.field(name="deleteSpending")
    list_spending: Optional[Currency] = strawberry.field(name="listSpending")


@strawberry.type
class ContractPruneMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(name="timestamp")
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    host_version: Optional[str] = strawberry.field(name="hostVersion")
    pruned: Optional[int] = strawberry.field(name="pruned")
    remaining: Optional[int] = strawberry.field(name="remaining")
    duration: Optional[Duration] = strawberry.field(description="Duration in nanoseconds", name="duration")


@strawberry.type
class ContractSize(SiaType):
    prunable: Optional[int] = strawberry.field(
        description="The amount of data that can be pruned from a contract", name="prunable"
    )
    size: Optional[int] = strawberry.field(description="The total size of a contract", name="size")


# @strawberry.type(description="A transaction or other event that affects the wallet including miner payouts, siafund claims, and file contract payouts.")
@strawberry.type
class Event(SiaType):
    module: Optional[str] = strawberry.field(description="The module that produced the event", name="module")
    event: Optional[str] = strawberry.field(description="The type/name of the event", name="event")
    payload: Optional[JSON] = strawberry.field(description="Optional event-specific payload data", name="payload")


@strawberry.type
class RedundancySettings(SiaType):
    min_shards: Optional[int] = strawberry.field(
        description="The number of data shards a piece of an object gets erasure-coded into | Minimum: 1",
        default=10,
        name="minShards",
    )
    total_shards: Optional[int] = strawberry.field(
        description="The number of total data shards a piece of an object gets erasure-coded into | Minimum: 2",
        default=30,
        name="totalShards",
    )


@strawberry.type
class GougingParams(SiaType):
    consensus_state: Optional[ConsensusState] = strawberry.field(name="consensusState")
    gouging_settings: Optional[GougingSettings] = strawberry.field(name="gougingSettings")
    redundancy_settings: Optional[RedundancySettings] = strawberry.field(name="redundancySettings")
    transaction_fee: Optional[Currency] = strawberry.field(name="transactionFee")


@strawberry.type
class Pin(SiaType):
    pinned: Optional[bool] = strawberry.field(description="Whether pin is enabled", name="pinned")
    value: Optional[float] = strawberry.field(
        description="The value of the underlying currency to which the setting is pinned",
        name="value",
    )


@strawberry.type
class GougingSettingsPins(SiaType):
    max_download: Optional[Pin] = strawberry.field(name="maxDownload")
    max_storage: Optional[Pin] = strawberry.field(name="maxStorage")
    max_upload: Optional[Pin] = strawberry.field(name="maxUpload")


@strawberry.type
class HostGougingBreakdown(SiaType):
    contract_err: Optional[str] = strawberry.field(
        description="Error message related to contract gouging checks.", name="contractErr"
    )
    download_err: Optional[str] = strawberry.field(
        description="Error message related to download gouging checks.", name="downloadErr"
    )
    gouging_err: Optional[str] = strawberry.field(
        description="Error message related to general gouging checks.", name="gougingErr"
    )
    prune_err: Optional[str] = strawberry.field(description="Error message related to pruning checks.", name="pruneErr")
    upload_err: Optional[str] = strawberry.field(
        description="Error message related to upload gouging checks.", name="uploadErr"
    )


@strawberry.type
class HostScoreBreakdown(SiaType):
    age: Optional[float] = strawberry.field(description="Score contribution based on the host's age.", name="age")
    collateral: Optional[float] = strawberry.field(
        description="Score contribution based on the host's collateral amount.", name="collateral"
    )
    interactions: Optional[float] = strawberry.field(
        description="Score contribution based on successful interactions.", name="interactions"
    )
    storage_remaining: Optional[float] = strawberry.field(
        description="Score contribution based on remaining storage capacity.", name="storageRemaining"
    )
    uptime: Optional[float] = strawberry.field(description="Score contribution based on host uptime.", name="uptime")
    version: Optional[float] = strawberry.field(
        description="Score contribution based on the host's software version.", name="version"
    )
    prices: Optional[float] = strawberry.field(
        description="Score contribution based on pricing metrics.", name="prices"
    )


@strawberry.type
class HostUsabilityBreakdown(SiaType):
    blocked: Optional[bool] = strawberry.field(description="Indicates if the host is blocked.", name="blocked")
    offline: Optional[bool] = strawberry.field(description="Indicates if the host is offline.", name="offline")
    low_score: Optional[bool] = strawberry.field(description="Indicates if the host has a low score.", name="lowScore")
    redundant_ip: Optional[bool] = strawberry.field(
        description="Indicates if the host's IP address is redundant.", name="redundantIP"
    )
    gouging: Optional[bool] = strawberry.field(description="Indicates if the host is gouging prices.", name="gouging")
    not_accepting_contracts: Optional[bool] = strawberry.field(
        description="Indicates if the host is not accepting new contracts.", name="notAcceptingContracts"
    )
    not_announced: Optional[bool] = strawberry.field(
        description="Indicates if the host has not been announced on the network.", name="notAnnounced"
    )
    not_completing_scan: Optional[bool] = strawberry.field(
        description="Indicates if the host is failing to complete scans.", name="notCompletingScan"
    )


@strawberry.type
class HostInteractions(SiaType):
    total_scans: Optional[int] = strawberry.field(
        description="The total number of scans performed on the host.", name="totalScans"
    )
    last_scan: Optional[datetime.datetime] = strawberry.field(
        description="Timestamp of the last scan performed.", name="lastScan"
    )
    last_scan_success: Optional[bool] = strawberry.field(
        description="Indicates whether the last scan was successful.", name="lastScanSuccess"
    )
    lost_sectors: Optional[int] = strawberry.field(
        description="Number of sectors lost since the last reporting period.", name="lostSectors"
    )
    second_to_last_scan_success: Optional[bool] = strawberry.field(
        description="Indicates whether the second-to-last scan was successful.", name="secondToLastScanSuccess"
    )
    uptime: Optional[Duration] = strawberry.field(description="Total uptime duration of the host.", name="uptime")
    downtime: Optional[Duration] = strawberry.field(description="Total downtime duration of the host.", name="downtime")
    successful_interactions: Optional[float] = strawberry.field(
        description="The number of successful interactions with the host.",
        name="successfulInteractions",
    )
    failed_interactions: Optional[float] = strawberry.field(
        description="The number of failed interactions with the host.", name="failedInteractions"
    )


# @strawberry.type(description="A detailed price table containing cost and configuration values for a host.")
@strawberry.type
class HostPriceTable(SiaType):
    uid: Optional[SettingsID] = strawberry.field(
        description="A unique specifier that identifies this price table", name="uid"
    )
    validity: Optional[Duration] = strawberry.field(
        description="Duration that specifies how long the host guarantees these prices for", name="validity"
    )
    host_block_height: Optional[int] = strawberry.field(
        description="The block height of the host, allows creating valid withdrawal messages if not synced",
        name="hostblockheight",
    )
    update_price_table_cost: Optional[Currency] = strawberry.field(
        description="Cost of fetching a new price table from the host", name="updatepricetablecost"
    )
    account_balance_cost: Optional[Currency] = strawberry.field(
        description="Cost of fetching the balance of an ephemeral account", name="accountbalancecost"
    )
    fund_account_cost: Optional[Currency] = strawberry.field(
        description="Cost of funding an ephemeral account on the host", name="fundaccountcost"
    )
    latest_revision_cost: Optional[Currency] = strawberry.field(
        description="Cost of asking the host for the latest revision of a contract", name="latestrevisioncost"
    )
    subscription_memory_cost: Optional[Currency] = strawberry.field(
        description="Cost of storing a byte of data for SubscriptionPeriod time", name="subscriptionmemorycost"
    )
    subscription_notification_cost: Optional[Currency] = strawberry.field(
        description="Cost of a single notification on top of bandwidth charges", name="subscriptionnotificationcost"
    )
    init_base_cost: Optional[Currency] = strawberry.field(
        description="Base cost incurred when an MDM program starts to run (excluding memory)", name="initbasecost"
    )
    memory_time_cost: Optional[Currency] = strawberry.field(
        description="Cost per byte per time incurred by program memory consumption", name="memorytimecost"
    )
    download_bandwidth_cost: Optional[Currency] = strawberry.field(
        description="Cost per byte for download bandwidth", name="downloadbandwidthcost"
    )
    upload_bandwidth_cost: Optional[Currency] = strawberry.field(
        description="Cost per byte for upload bandwidth", name="uploadbandwidthcost"
    )
    drop_sectors_base_cost: Optional[Currency] = strawberry.field(
        description="Base cost for DropSectors instruction", name="dropsectorsbasecost"
    )
    drop_sectors_unit_cost: Optional[Currency] = strawberry.field(
        description="Cost per sector for DropSectors instruction", name="dropsectorsunitcost"
    )
    has_sector_base_cost: Optional[Currency] = strawberry.field(
        description="Base cost for HasSector command", name="hassectorbasecost"
    )
    read_base_cost: Optional[Currency] = strawberry.field(
        description="Base cost for Read instruction", name="readbasecost"
    )
    read_length_cost: Optional[Currency] = strawberry.field(
        description="Cost per byte for Read instruction", name="readlengthcost"
    )
    renew_contract_cost: Optional[Currency] = strawberry.field(
        description="Cost for RenewContract instruction", name="renewcontractcost"
    )
    revision_base_cost: Optional[Currency] = strawberry.field(
        description="Base cost for Revision command", name="revisionbasecost"
    )
    swap_sector_cost: Optional[Currency] = strawberry.field(
        description="Cost of swapping 2 full sectors by root", name="swapsectorcost"
    )
    write_base_cost: Optional[Currency] = strawberry.field(
        description="Base cost per write operation", name="writebasecost"
    )
    write_length_cost: Optional[Currency] = strawberry.field(
        description="Cost per byte written", name="writelengthcost"
    )
    write_store_cost: Optional[Currency] = strawberry.field(
        description="Cost per byte/block of additional storage", name="writestorecost"
    )
    txn_fee_min_recommended: Optional[Currency] = strawberry.field(
        description="Minimum recommended transaction fee", name="txnfeeminrecommended"
    )
    txn_fee_max_recommended: Optional[Currency] = strawberry.field(
        description="Maximum recommended transaction fee", name="txnfeemaxrecommended"
    )
    contract_price: Optional[Currency] = strawberry.field(
        description="Fee charged for forming/renewing contracts to cover miner fees", name="contractprice"
    )
    collateral_cost: Optional[Currency] = strawberry.field(
        description="Collateral locked per byte when adding new data", name="collateralcost"
    )
    max_collateral: Optional[Currency] = strawberry.field(
        description="Maximum collateral the host will put in a single contract", name="maxcollateral"
    )
    max_duration: Optional[int] = strawberry.field(
        description="Maximum contract formation duration in blocks", name="maxduration"
    )
    window_size: Optional[int] = strawberry.field(
        description="Minimum blocks for contract renew window", name="windowsize"
    )
    registry_entries_left: Optional[int] = strawberry.field(
        description="Remaining available registry entries", name="registryentriesleft"
    )
    registry_entries_total: Optional[int] = strawberry.field(
        description="Total available registry entries", name="registryentriestotal"
    )
    expiry: Optional[datetime.datetime] = strawberry.field(
        description="Time when this price table expires", name="expiry"
    )


@strawberry.type
class HostV4Settings(SiaType):
    accepting_contracts: Optional[bool] = strawberry.field(
        description="Whether the host is accepting new contracts", name="acceptingcontracts"
    )
    max_download_batch_size: Optional[int] = strawberry.field(
        description="Maximum allowed download batch size", name="maxdownloadbatchsize"
    )
    max_duration: Optional[int] = strawberry.field(description="Maximum allowed contract duration", name="maxduration")
    max_revise_batch_size: Optional[int] = strawberry.field(
        description="Maximum allowed revision batch size", name="maxrevisebatchsize"
    )
    net_address: Optional[str] = strawberry.field(description="Network address of the host", name="netaddress")
    remaining_storage: Optional[int] = strawberry.field(
        description="Amount of storage the host has remaining", name="remainingstorage"
    )
    sector_size: Optional[int] = strawberry.field(description="Size of a storage sector", name="sectorsize")
    total_storage: Optional[int] = strawberry.field(description="Total amount of storage space", name="totalstorage")
    address: Optional[Address] = strawberry.field(name="unlockhash")
    window_size: Optional[int] = strawberry.field(description="Size of the proof window", name="windowsize")
    collateral: Optional[Currency] = strawberry.field(name="collateral")
    max_collateral: Optional[Currency] = strawberry.field(name="maxcollateral")
    base_rpc_price: Optional[Currency] = strawberry.field(name="baserpcprice")
    contract_price: Optional[Currency] = strawberry.field(name="contractprice")
    download_bandwidth_price: Optional[Currency] = strawberry.field(name="downloadbandwidthprice")
    sector_access_price: Optional[Currency] = strawberry.field(name="sectoraccessprice")
    storage_price: Optional[Currency] = strawberry.field(name="storageprice")
    upload_bandwidth_price: Optional[Currency] = strawberry.field(name="uploadbandwidthprice")
    ephemeral_account_expiry: Optional[Duration] = strawberry.field(
        description="Duration before an ephemeral account expires", name="ephemeralaccountexpiry"
    )
    max_ephemeral_account_balance: Optional[Currency] = strawberry.field(name="maxephemeralaccountbalance")
    revision_number: Optional[int] = strawberry.field(name="revisionnumber")
    version: Optional[str] = strawberry.field(description="Version of the host software", name="version")
    release: Optional[str] = strawberry.field(description="Release tag of the host software", name="release")
    siamux_port: Optional[str] = strawberry.field(description="Port used for siamux connections", name="siamuxport")


@strawberry.type
class HostPrices(SiaType):
    contract_price: Optional[Currency] = strawberry.field(name="contractPrice")
    collateral: Optional[Currency] = strawberry.field(name="collateral")
    storage_price: Optional[Currency] = strawberry.field(name="storagePrice")
    ingress_price: Optional[Currency] = strawberry.field(name="ingressPrice")
    egress_price: Optional[Currency] = strawberry.field(name="egressPrice")
    free_sector_price: Optional[Currency] = strawberry.field(name="freeSectorPrice")
    tip_height: Optional[int] = strawberry.field(
        description="The height at which the prices were last updated", name="tipHeight"
    )
    valid_until: Optional[datetime.datetime] = strawberry.field(name="validUntil")
    signature: Optional[Signature] = strawberry.field(name="signature")


@strawberry.type
class HostV2Settings(SiaType):
    accepting_contracts: Optional[bool] = strawberry.field(
        description="Whether the host is accepting new contracts", name="acceptingcontracts"
    )
    max_download_batch_size: Optional[int] = strawberry.field(
        description="Maximum allowed download batch size", name="maxdownloadbatchsize"
    )
    max_duration: Optional[int] = strawberry.field(description="Maximum allowed duration", name="maxduration")
    max_revise_batch_size: Optional[int] = strawberry.field(
        description="Maximum allowed revision batch size", name="maxrevisebatchsize"
    )
    net_address: Optional[str] = strawberry.field(description="Network address of the host", name="netaddress")
    remaining_storage: Optional[int] = strawberry.field(
        description="Amount of storage the host has remaining", name="remainingstorage"
    )
    sector_size: Optional[int] = strawberry.field(description="Size of a storage sector", name="sectorsize")
    total_storage: Optional[int] = strawberry.field(description="Total amount of storage space", name="totalstorage")
    address: Optional[Address] = strawberry.field(name="unlockhash")
    window_size: Optional[int] = strawberry.field(description="Size of the proof window", name="windowsize")
    collateral: Optional[Currency] = strawberry.field(name="collateral")
    max_collateral: Optional[Currency] = strawberry.field(name="maxcollateral")
    base_rpc_price: Optional[Currency] = strawberry.field(name="baserpcprice")
    contract_price: Optional[Currency] = strawberry.field(name="contractprice")
    download_bandwidth_price: Optional[Currency] = strawberry.field(name="downloadbandwidthprice")
    sector_access_price: Optional[Currency] = strawberry.field(name="sectoraccessprice")
    storage_price: Optional[Currency] = strawberry.field(name="storageprice")
    upload_bandwidth_price: Optional[Currency] = strawberry.field(name="uploadbandwidthprice")
    ephemeral_account_expiry: Optional[Duration] = strawberry.field(
        description="Duration before an ephemeral account expires", name="ephemeralaccountexpiry"
    )
    max_ephemeral_account_balance: Optional[Currency] = strawberry.field(name="maxephemeralaccountbalance")
    revision_number: Optional[int] = strawberry.field(name="revisionnumber")
    version: Optional[str] = strawberry.field(description="Version of the host software", name="version")
    release: Optional[str] = strawberry.field(description="Release tag of the host software", name="release")
    siamux_port: Optional[str] = strawberry.field(description="Port used for siamux connections", name="siamuxport")


@strawberry.type
class HostChecks(SiaType):
    gouging: Optional[bool] = strawberry.field(description="Whether the host is gouging", name="gouging")
    gouging_breakdown: Optional[HostGougingBreakdown] = strawberry.field(name="gougingBreakdown")
    score: Optional[float] = strawberry.field(description="The host's overall score", name="score")
    score_breakdown: Optional[HostScoreBreakdown] = strawberry.field(name="scoreBreakdown")
    usable: Optional[bool] = strawberry.field(description="Whether the host is usable", name="usable")
    unusable_reasons: Optional[List[str]] = strawberry.field(
        description="Reasons why the host is unusable", name="unusableReasons"
    )


@strawberry.type
class HostCheck(SiaType):
    gouging: Optional[HostGougingBreakdown] = strawberry.field(name="gouging")
    score: Optional[HostScoreBreakdown] = strawberry.field(name="score")
    usability: Optional[HostUsabilityBreakdown] = strawberry.field(name="usability")


@strawberry.type
class Host(SiaType):
    known_since: Optional[datetime.datetime] = strawberry.field(
        description="The time the host was first seen", name="knownSince"
    )
    last_announcement: Optional[datetime.datetime] = strawberry.field(
        description="The time the host last announced itself", name="lastAnnouncement"
    )
    public_key: Optional[PublicKey] = strawberry.field(name="publicKey")
    net_address: Optional[str] = strawberry.field(description="The address of the host", name="netAddress")
    price_table: Optional[HostPriceTable] = strawberry.field(name="priceTable")
    settings: Optional[HostV2Settings] = strawberry.field(name="settings")
    interactions: Optional[HostInteractions] = strawberry.field(name="interactions")
    scanned: Optional[bool] = strawberry.field(description="Whether the host has been scanned", name="scanned")
    blocked: Optional[bool] = strawberry.field(description="Whether the host is blocked", name="blocked")
    checks: Optional[JSON] = strawberry.field(name="checks")  # Dict[str, HostCheck]
    stored_data: Optional[int] = strawberry.field(
        description="The amount of data stored on the host in bytes", name="storedData"
    )
    resolved_addresses: Optional[List[str]] = strawberry.field(name="resolvedAddresses")
    subnets: Optional[List[str]] = strawberry.field(name="subnets")


@strawberry.type
class MemoryStatus(SiaType):
    available: Optional[int] = strawberry.field(
        description="The amount of remaining memory currently available in bytes",
        name="available",
    )
    total: Optional[int] = strawberry.field(
        description="The total amount of memory available in bytes | Minimum: 1",
        name="total",
    )


@strawberry.type
class MigrateSlabResponse(SiaType):
    num_shards_migrated: Optional[int] = strawberry.field(name="numShardsMigrated")
    surcharge_applied: Optional[bool] = strawberry.field(name="surchargeApplied")
    error: Optional[str] = strawberry.field(name="error")


@strawberry.type
class ContractRevision(SiaType):
    revision: Optional[FileContractRevision] = strawberry.field(
        description="The revised file contract", name="revision"
    )
    signatures: Optional[List[TransactionSignature]] = strawberry.field(
        description="The transaction signatures [2]", name="signatures"
    )


@strawberry.type
class RHPFormResponse(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    contract: Optional[ContractRevision] = strawberry.field(name="contract")
    transaction_set: Optional[List[Transaction]] = strawberry.field(name="transactionSet")


@strawberry.type
class RHPFundRequest(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    siamux_addr: Optional[str] = strawberry.field(name="siamuxAddr")
    balance: Optional[Currency] = strawberry.field(name="balance")


@strawberry.type
class RHPPriceTableRequest(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    siamux_addr: Optional[str] = strawberry.field(name="siamuxAddr")
    timeout: Optional[DurationMS] = strawberry.field(name="timeout")


@strawberry.type
class RHPScanRequest(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    host_ip: Optional[str] = strawberry.field(name="hostIP")
    timeout: Optional[DurationMS] = strawberry.field(name="timeout")


@strawberry.type
class RHPScanResponse(SiaType):
    ping: Optional[DurationMS] = strawberry.field(name="ping")
    scan_error: Optional[str] = strawberry.field(name="scanError")
    settings: Optional[HostV2Settings] = strawberry.field(name="settings")
    price_table: Optional[HostPriceTable] = strawberry.field(name="priceTable")


@strawberry.type
class RHPSyncRequest(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    siamux_addr: Optional[str] = strawberry.field(name="siamuxAddr")


@strawberry.type
class RHPPreparePaymentRequest(SiaType):
    account: Optional[Account] = strawberry.field(name="account")
    amount: Optional[Currency] = strawberry.field(name="amount")
    expiry: Optional[int] = strawberry.field(name="expiry")
    account_key: Optional[str] = strawberry.field(name="accountKey")


@strawberry.type
class DownloaderStats(SiaType):
    avg_sector_download_speed_mbps: Optional[float] = strawberry.field(name="avgSectorDownloadSpeedMbps")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    num_downloads: Optional[int] = strawberry.field(name="numDownloads")


@strawberry.type
class DownloadStatsResponse(SiaType):
    avg_download_speed_mbps: Optional[float] = strawberry.field(name="avgDownloadSpeedMbps")
    avg_overdrive_pct: Optional[float] = strawberry.field(name="avgOverdrivePct")
    healthy_downloaders: Optional[int] = strawberry.field(name="healthyDownloaders")
    num_downloaders: Optional[int] = strawberry.field(name="numDownloaders")
    downloaders_stats: Optional[List[DownloaderStats]] = strawberry.field(name="downloadersStats")


@strawberry.type
class UploaderStats(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    avg_sector_upload_speed_mbps: Optional[float] = strawberry.field(name="avgSectorUploadSpeedMbps")


@strawberry.type
class UploadStatsResponse(SiaType):
    avg_slab_upload_speed_mbps: Optional[float] = strawberry.field(name="avgSlabUploadSpeedMbps")
    avg_overdrive_pct: Optional[float] = strawberry.field(name="avgOverdrivePct")
    healthy_uploaders: Optional[int] = strawberry.field(name="healthyUploaders")
    num_uploaders: Optional[int] = strawberry.field(name="numUploaders")
    uploaders_stats: Optional[List[UploaderStats]] = strawberry.field(name="uploadersStats")


@strawberry.type
class WorkerStateResponse(BuildState):
    id: Optional[str] = strawberry.field(name="id")
    start_time: Optional[datetime.datetime] = strawberry.field(name="startTime")


@strawberry.type
class UploadMultipartUploadPartResponse(SiaType):
    etag: Optional[str] = strawberry.field(name="etag")


@strawberry.type
class MultipartCompletedPart(SiaType):
    part_number: Optional[int] = strawberry.field(description="The number of this part", name="partNumber")
    e_tag: Optional[ETag] = strawberry.field(name="eTag")


@strawberry.type
class MultipartListPartItem(SiaType):
    part_number: Optional[int] = strawberry.field(description="The number of this part", name="partNumber")
    last_modified: Optional[datetime.datetime] = strawberry.field(
        description="When this part was last modified", name="lastModified"
    )
    e_tag: Optional[ETag] = strawberry.field(name="eTag")
    size: Optional[int] = strawberry.field(description="The size of this part in bytes", name="size")


@strawberry.type
class MultipartUpload(SiaType):
    bucket: Optional[str] = strawberry.field(description="The name of the bucket", name="bucket")
    key: Optional[EncryptionKey] = strawberry.field(name="key")
    path: Optional[str] = strawberry.field(name="path")
    upload_id: Optional[str] = strawberry.field(name="uploadID")
    created_at: Optional[datetime.datetime] = strawberry.field(name="createdAt")


@strawberry.type
class HardforkDevAddr(SiaType):
    height: Optional[int] = strawberry.field(name="height")
    old_address: Optional[Address] = strawberry.field(name="oldAddress")
    new_address: Optional[Address] = strawberry.field(name="newAddress")


@strawberry.type
class HardforkTax(SiaType):
    height: Optional[int] = strawberry.field(name="height")


@strawberry.type
class HardforkStorageProof(SiaType):
    height: Optional[int] = strawberry.field(name="height")


@strawberry.type
class HardforkOak(SiaType):
    height: Optional[int] = strawberry.field(name="height")
    fix_height: Optional[int] = strawberry.field(name="fixHeight")
    genesis_timestamp: Optional[datetime.datetime] = strawberry.field(name="genesisTimestamp")


@strawberry.type
class HardforkASIC(SiaType):
    height: Optional[int] = strawberry.field(name="height")
    oak_time: Optional[Duration] = strawberry.field(name="oakTime")
    oak_target: Optional[BlockID] = strawberry.field(name="oakTarget")


@strawberry.type
class HardforkFoundation(SiaType):
    height: Optional[int] = strawberry.field(name="height")
    primary_address: Optional[Address] = strawberry.field(name="primaryAddress")
    failsafe_address: Optional[Address] = strawberry.field(name="failsafeAddress")


@strawberry.type
class HardforkV2(SiaType):
    allow_height: Optional[int] = strawberry.field(name="allowHeight")
    require_height: Optional[int] = strawberry.field(name="requireHeight")


@strawberry.type
class Network(SiaType):
    name: Optional[str] = strawberry.field(description="The name of the network", name="name")
    initial_coinbase: Optional[Currency] = strawberry.field(
        description="The initial coinbase reward", name="initialCoinbase"
    )
    minimum_coinbase: Optional[Currency] = strawberry.field(
        description="The minimum coinbase reward", name="minimumCoinbase"
    )
    initial_target: Optional[BlockID] = strawberry.field(description="The initial target", name="initialTarget")
    block_interval: Optional[Duration] = strawberry.field(
        description="The block interval", name="blockInterval"
    )  # time.Duration
    maturity_delay: Optional[int] = strawberry.field(description="The maturity delay", name="maturityDelay")
    hardfork_dev_addr: Optional[HardforkDevAddr] = strawberry.field(name="hardforkDevAddr")
    hardfork_tax: Optional[HardforkTax] = strawberry.field(name="hardforkTax")
    hardfork_storage_proof: Optional[HardforkStorageProof] = strawberry.field(name="hardforkStorageProof")
    hardfork_oak: Optional[HardforkOak] = strawberry.field(name="hardforkOak")
    hardfork_asic: Optional[HardforkASIC] = strawberry.field(name="hardforkASIC")
    hardfork_foundation: Optional[HardforkFoundation] = strawberry.field(name="hardforkFoundation")
    hardfork_v2: Optional[HardforkV2] = strawberry.field(name="hardforkV2")


class ElementAccumulator(SiaType):
    trees: List[Hash256] = strawberry.field(name="trees")
    num_leaves: int = strawberry.field(name="numLeaves")


class Work(SiaType):
    n: str = strawberry.field(name="n")


@strawberry.type
class ChainState(SiaType):
    network: Optional[Network] = strawberry.field(default=None)
    index: Optional[ChainIndex] = strawberry.field(name="index")
    prev_timestamps: Optional[List[datetime.datetime]] = strawberry.field(name="prevTimestamps")
    depth: Optional[BlockID] = strawberry.field(name="depth")
    child_target: Optional[BlockID] = strawberry.field(name="childTarget")
    siafund_tax_revenue: Optional[Currency] = strawberry.field(name="siafundTaxRevenue")
    oak_time: Optional[Duration] = strawberry.field(name="oakTime")
    oak_target: Optional[BlockID] = strawberry.field(name="oakTarget")
    foundation_subsidy_address: Optional[Address] = strawberry.field(name="foundationSubsidyAddress")
    foundation_management_address: Optional[Address] = strawberry.field(name="foundationManagementAddress")
    total_work: Optional[Work] = strawberry.field(name="totalWork")  # Work type
    difficulty: Optional[Work] = strawberry.field(name="difficulty")  # Work type
    oak_work: Optional[Work] = strawberry.field(name="oakWork")  # Work type
    elements: Optional[ElementAccumulator] = strawberry.field(name="elements")  # ElementAccumulator
    attestations: Optional[int] = strawberry.field(name="attestations")


@strawberry.type
class ObjectMetadata(SiaType):
    etag: Optional[str] = strawberry.field(description="The ETag of the object", name="eTag")
    health: Optional[float] = strawberry.field(description="The health of the object", name="health")
    mod_time: Optional[datetime.datetime] = strawberry.field(
        description="When the object was last modified", name="modTime"
    )
    name: Optional[str] = strawberry.field(description="The name of the object", name="name")
    size: Optional[int] = strawberry.field(description="The size of the object in bytes", name="size")
    mime_type: Optional[str] = strawberry.field(description="The MIME type of the object", name="mimeType")


@strawberry.type
class Sector(SiaType):
    contracts: Optional[JSON] = strawberry.field(name="contracts")  # Dict[PublicKey, List[FileContractID]]
    latest_host: Optional[PublicKey] = strawberry.field(name="latestHost")
    root: Optional[Hash256] = strawberry.field(name="root")


@strawberry.type
class Slab(SiaType):
    health: Optional[float] = strawberry.field(description="Minimum: 0 | Maximum: 1", name="health")
    key: Optional[EncryptionKey] = strawberry.field(name="key")
    min_shards: Optional[int] = strawberry.field(
        description="The number of data shards the slab is split into | Minimum: 1 | Maximum: 255",
        name="minShards",
    )
    shards: Optional[List[Sector]] = strawberry.field(description="List of sectors", name="shards")


# @strawberry.type(description="A contiguous region within a slab")
@strawberry.type
class SlabSlice(Slab):
    offset: Optional[int] = strawberry.field(name="offset")
    limit: Optional[int] = strawberry.field(name="limit")


@strawberry.type
class Object(SiaType):
    metadata: Optional[ObjectMetadata] = strawberry.field(name="metadata")  # ObjectUserMetadata
    key: Optional[EncryptionKey] = strawberry.field(name="key")
    slabs: Optional[List[SlabSlice]] = strawberry.field(name="slabs")
    etag: Optional[str] = strawberry.field(name="eTag")
    health: Optional[float] = strawberry.field(name="health")
    mod_time: Optional[datetime.datetime] = strawberry.field(name="modTime")
    name: Optional[str] = strawberry.field(name="name")
    size: Optional[int] = strawberry.field(name="size")
    mime_type: Optional[str] = strawberry.field(name="mimeType")


@strawberry.type
class PackedSlab(SiaType):
    buffer_id: Optional[int] = strawberry.field(description="ID of the buffer containing the slab", name="bufferID")
    shards: Optional[List[Sector]] = strawberry.field(name="shards")


@strawberry.type
class PinnedSettings(SiaType):
    # Currency is the external three letter currency code. If empty,
    # pinning is disabled. If the explorer does not support the
    # currency an error is returned.
    currency: Optional[str] = strawberry.field(name="currency")

    # Threshold is a percentage from 0 to 1 that determines when the
    # host's settings are updated based on the current exchange rate.
    threshold: Optional[float] = strawberry.field(name="threshold")

    # Storage, Ingress, and Egress are the pinned prices in the
    # external currency.
    storage: Optional[Pin] = strawberry.field(name="storage")
    ingress: Optional[Pin] = strawberry.field(name="ingress")
    egress: Optional[Pin] = strawberry.field(name="egress")

    # MaxCollateral is the maximum collateral that the host will
    # accept in the external currency.
    max_collateral: Optional[Pin] = strawberry.field(name="maxCollateral")


@strawberry.type
class SlabBuffer(SiaType):
    contract_set: Optional[str] = strawberry.field(
        description="Contract set that be buffer will be uploaded to", name="contractSet"
    )
    complete: Optional[bool] = strawberry.field(
        description="Whether the slab buffer is complete and ready to upload", name="complete"
    )
    filename: Optional[str] = strawberry.field(description="Name of the buffer on disk", name="filename")
    size: Optional[int] = strawberry.field(description="Size of the buffer", name="size")
    max_size: Optional[int] = strawberry.field(description="Maximum size of the buffer", name="maxSize")
    locked: Optional[bool] = strawberry.field(
        description="Whether the slab buffer is locked for uploading", name="locked"
    )


@strawberry.type
class UploadPackingSettings(SiaType):
    enabled: Optional[bool] = strawberry.field(description="Whether upload packing is enabled", name="enabled")
    slab_buffer_max_size_soft: Optional[int] = strawberry.field(
        description="Maximum size for slab buffers", name="slabBufferMaxSizeSoft"
    )


@strawberry.type
class UploadedPackedSlab(SiaType):
    buffer_id: Optional[int] = strawberry.field(description="ID of the buffer", name="bufferID")
    shards: Optional[List[Sector]] = strawberry.field(name="shards")


@strawberry.type
class WalletMetric(SiaType):
    timestamp: Optional[datetime.datetime] = strawberry.field(name="timestamp")
    confirmed: Optional[Currency] = strawberry.field(name="confirmed")
    spendable: Optional[Currency] = strawberry.field(name="spendable")
    unconfirmed: Optional[Currency] = strawberry.field(name="unconfirmed")
    immature: Optional[Currency] = strawberry.field(name="immature")


@strawberry.type
class Webhook(SiaType):
    module: str = strawberry.field(name="module")
    event: str = strawberry.field(name="event")
    url: str = strawberry.field(name="url")
    headers: Optional[JSON] = strawberry.field(name="headers")  # Dict[str, str]


@strawberry.type
class WebhookEvent(SiaType):
    module: Optional[str] = strawberry.field(description="The module that triggered the event", name="module")
    event: Optional[str] = strawberry.field(description="The type of event that occurred", name="event")
    data: Optional[JSON] = strawberry.field(description="Event-specific data payload", name="data")


@strawberry.type
class WebhookQueueInfo(SiaType):
    url: Optional[str] = strawberry.field(description="The URL of the webhook", name="url")
    size: Optional[int] = strawberry.field(description="The number of events in the queue", name="size")


@strawberry.type
class WebhookResponse(SiaType):
    webhooks: Optional[List[Webhook]] = strawberry.field(description="List of registered webhooks", name="webhooks")
    queues: Optional[List[WebhookQueueInfo]] = strawberry.field(
        description="Information about webhook event queues", name="queues"
    )


@strawberry.enum
class Severity(Enum):
    INFO = strawberry.enum_value(1, description="Indicates that the alert is informational.")
    WARNING = strawberry.enum_value(2, description="Indicates that the alert is a warning.")
    ERROR = strawberry.enum_value(3, description="Indicates that the alert is an error.")
    CRITICAL = strawberry.enum_value(4, description="Indicates that the alert is critical.")


@strawberry.type
class Alert(SiaType):
    # ID is a unique identifier for the alert.
    id: Optional[Hash256] = strawberry.field(description="A unique identifier for the alert.", name="id")

    # Severity is the severity of the alert.
    severity: Optional[Severity] = strawberry.field(description="The severity of the alert.", name="severity")

    # Message is a human-readable message describing the alert.
    message: Optional[str] = strawberry.field(
        description="A human-readable message describing the alert.", name="message"
    )

    # Data is a map of arbitrary data that can be used to provide additional context to the alert.
    data: Optional[JSON] = strawberry.field(
        description="A map of arbitrary data that can be used to provide additional context to the alert.", name="data"
    )

    # Timestamp when the alert occurred
    timestamp: Optional[datetime.datetime] = strawberry.field(name="timestamp")


@strawberry.type
class AlertsOpts(SiaType):
    offset: Optional[int] = strawberry.field(description="Offset used in pagination", name="offset")
    limit: Optional[int] = strawberry.field(description="Limit used in pagination", name="limit")
    severity: Optional[Severity] = strawberry.field(
        description="Severity filter (1=info,2=warning,3=error,4=critical)", name="severity"
    )


@strawberry.type
class AlertTotals(SiaType):
    info: Optional[int] = strawberry.field(description="Number of info alerts", name="info")
    warning: Optional[int] = strawberry.field(description="Number of warning alerts", name="warning")
    error: Optional[int] = strawberry.field(description="Number of error alerts", name="error")
    critical: Optional[int] = strawberry.field(description="Number of critical alerts", name="critical")


@strawberry.type
class AlertsResponse(SiaType):
    alerts: List[Alert] = strawberry.field(description="List of alerts", name="alerts")
    has_more: bool = strawberry.field(description="Indicates if more alerts remain", name="hasMore")
    totals: AlertTotals = strawberry.field(description="Aggregate counts of alerts by severity", name="totals")


@strawberry.type
class AccountsAddBalanceRequest(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(description="Public key of the host", name="hostKey")
    amount: Optional[int] = strawberry.field(description="Amount to be added to the account balance", name="amount")


@strawberry.type
class AccountHandlerPOST(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(description="Public key of the host", name="hostKey")


@strawberry.type
class AccountsRequiresSyncRequest(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(description="Public key of the host", name="hostKey")


@strawberry.type
class AccountsUpdateBalanceRequest(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(description="Public key of the host", name="hostKey")
    amount: Optional[int] = strawberry.field(description="Updated balance amount", name="amount")


@strawberry.type
class AutopilotTriggerRequest(SiaType):
    force_scan: Optional[bool] = strawberry.field(
        description="Whether to force an immediate host scan", name="forceScan"
    )


@strawberry.type
class AutopilotTriggerResponse(SiaType):
    triggered: Optional[bool] = strawberry.field(
        description="Indicates if the autopilot loop was triggered", name="triggered"
    )


@strawberry.type
class AutopilotStateResponse(BuildState):
    configured: Optional[bool] = strawberry.field(
        description="Indicates whether the autopilot is configured", name="configured"
    )
    migrating: Optional[bool] = strawberry.field(description="Autopilot is currently migrating", name="migrating")
    migrating_last_start: Optional[datetime.datetime] = strawberry.field(
        description="Last start time for migrating", name="migratingLastStart"
    )
    pruning: Optional[bool] = strawberry.field(description="Autopilot is currently pruning", name="pruning")
    pruning_last_start: Optional[datetime.datetime] = strawberry.field(
        description="Last start time for pruning", name="pruningLastStart"
    )
    scanning: Optional[bool] = strawberry.field(description="Autopilot is currently scanning hosts", name="scanning")
    scanning_last_start: Optional[datetime.datetime] = strawberry.field(
        description="Last start time for scanning", name="scanningLastStart"
    )
    uptime_ms: Optional[Duration] = strawberry.field(description="Autopilot uptime in milliseconds", name="uptimeMs")
    start_time: Optional[datetime.datetime] = strawberry.field(
        description="Timestamp of autopilot's start time", name="startTime"
    )


@strawberry.type
class ConfigEvaluationRequest(SiaType):
    autopilot_config: Optional[AutopilotConfig] = strawberry.field(
        description="Proposed autopilot config", name="autopilotConfig"
    )
    gouging_settings: Optional[GougingSettings] = strawberry.field(
        description="Proposed gouging settings", name="gougingSettings"
    )
    redundancy_settings: Optional[RedundancySettings] = strawberry.field(
        description="Proposed redundancy settings", name="redundancySettings"
    )

    @strawberry.type
    class ConfigRecommendation(SiaType):
        gouging_settings: Optional[GougingSettings] = strawberry.field(
            description="Recommended gouging settings", name="gougingSettings"
        )


@strawberry.type
class GougingUnusable(SiaType):
    contract: Optional[int] = strawberry.field(name="contract")
    download: Optional[int] = strawberry.field(name="download")
    gouging: Optional[int] = strawberry.field(name="gouging")
    pruning: Optional[int] = strawberry.field(name="pruning")
    upload: Optional[int] = strawberry.field(name="upload")


@strawberry.type
class ConfigEvaluationUnusable(SiaType):
    blocked: Optional[int] = strawberry.field(name="blocked")
    gouging: Optional[GougingUnusable] = strawberry.field(name="gouging")
    not_accepting_contracts: Optional[int] = strawberry.field(name="notAcceptingContracts")
    not_scanned: Optional[int] = strawberry.field(name="notScanned")


@strawberry.type
class ConfigEvaluationResponse(SiaType):
    hosts: Optional[int] = strawberry.field(description="Total hosts scanned", name="hosts")
    usable: Optional[int] = strawberry.field(description="Number of hosts determined to be usable", name="usable")
    unusable: Optional[ConfigEvaluationUnusable] = strawberry.field(
        description="Breakdown of unusable hosts", name="unusable"
    )
    recommendation: Optional[ConfigRecommendation] = strawberry.field(
        description="Recommended config changes", name="recommendation"
    )


@strawberry.type
class CreateBucketOptions(SiaType):
    policy: Optional[BucketPolicy] = strawberry.field(description="Bucket policy options", name="policy")


@strawberry.type
class BucketCreateRequest(SiaType):
    name: Optional[str] = strawberry.field(description="Name of the new bucket", name="name")
    policy: Optional[BucketPolicy] = strawberry.field(description="Policy configuration for this bucket", name="policy")


@strawberry.type
class BucketUpdatePolicyRequest(SiaType):
    policy: Optional[BucketPolicy] = strawberry.field(
        description="Updated policy configuration for this bucket", name="policy"
    )


@strawberry.type
class UploadParams(GougingParams):
    current_height: Optional[int] = strawberry.field(description="Current block height", name="currentHeight")
    contract_set: Optional[str] = strawberry.field(description="Contract set identifier", name="contractSet")
    upload_packing: Optional[bool] = strawberry.field(
        description="Whether upload packing is enabled", name="uploadPacking"
    )


@strawberry.type
class AccountsFundRequest(SiaType):
    account_id: Optional[PublicKey] = strawberry.field(
        description="Unique account ID (rhpv3.Account)", name="accountID"
    )
    amount: Optional[Currency] = strawberry.field(description="Amount to fund the account with", name="amount")
    contract_id: Optional[FileContractID] = strawberry.field(
        description="ID of the contract used for funding", name="contractID"
    )


@strawberry.type
class AccountsFundResponse(SiaType):
    deposit: Optional[Currency] = strawberry.field(description="Amount deposited", name="deposit")


@strawberry.type
class AccountsSaveRequest(SiaType):
    accounts: Optional[List[Account]] = strawberry.field(description="List of accounts to save", name="accounts")


@strawberry.type
class BackupRequest(SiaType):
    path: Optional[str] = strawberry.field(description="Path to save the backup", name="path")


@strawberry.type
class ExplorerState(SiaType):
    enabled: Optional[bool] = strawberry.field(description="Indicates whether explorer is enabled", name="enabled")
    url: Optional[str] = strawberry.field(description="Optional URL for the explorer source", name="url")


@strawberry.type
class BusStateResponse(BuildState):
    start_time: Optional[datetime.datetime] = strawberry.field(
        description="Timestamp when the bus started", name="startTime"
    )
    network: Optional[str] = strawberry.field(
        description="Network identifier (e.g., 'mainnet', 'testnet')", name="network"
    )


@strawberry.type
class ContractSetUpdateRequest(SiaType):
    to_add: Optional[List[FileContractID]] = strawberry.field(
        description="List of contract IDs to add to the set", name="toAdd"
    )
    to_remove: Optional[List[FileContractID]] = strawberry.field(
        description="List of contract IDs to remove from the set", name="toRemove"
    )


@strawberry.type
class MemoryResponse(SiaType):
    download: Optional[MemoryStatus] = strawberry.field(name="download")
    upload: Optional[MemoryStatus] = strawberry.field(name="upload")


@strawberry.type
class ContractsResponse(SiaType):
    contracts: Optional[List[Contract]] = strawberry.field(description="List of contracts", name="contracts")
    errors: Optional[JSON] = strawberry.field(
        description="Map of host public keys to error messages", name="errors"
    )  # Dict[PublicKey, str]
    error: Optional[str] = strawberry.field(description="Deprecated error field", name="error")


@strawberry.type
class ContractPrunableData(ContractSize):
    id: Optional[FileContractID] = strawberry.field(name="id")


@strawberry.type
class ContractSpendingRecord(ContractSpending):
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
    contract: Optional[ContractRevision] = strawberry.field(name="contract", description="rhpv2.ContractRevision")
    contract_price: Optional[Currency] = strawberry.field(name="contractPrice")
    start_height: Optional[int] = strawberry.field(name="startHeight")
    state: Optional[str] = strawberry.field(name="state")
    total_cost: Optional[Currency] = strawberry.field(name="totalCost")


@strawberry.type
class ContractFormRequest(SiaType):
    end_height: Optional[int] = strawberry.field(name="endHeight")
    host_collateral: Optional[Currency] = strawberry.field(name="hostCollateral")
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    host_ip: Optional[str] = strawberry.field(name="hostIP")
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
class ContractRootsResponse(SiaType):
    roots: Optional[List[Hash256]] = strawberry.field(description="List of root hashes", name="roots")
    uploading: Optional[List[Hash256]] = strawberry.field(
        description="List of root hashes currently being uploaded", name="uploading"
    )


@strawberry.type
class ContractRenewRequest(SiaType):
    end_height: Optional[int] = strawberry.field(name="endHeight")
    expected_new_storage: Optional[int] = strawberry.field(name="expectedNewStorage")
    max_fund_amount: Optional[Currency] = strawberry.field(name="maxFundAmount")
    min_new_collateral: Optional[Currency] = strawberry.field(name="minNewCollateral")
    renter_funds: Optional[Currency] = strawberry.field(name="renterFunds")


@strawberry.type
class ContractRenewedRequest(SiaType):
    contract: Optional[ContractRevision] = strawberry.field(description="rhpv2.ContractRevision", name="contract")
    contract_price: Optional[Currency] = strawberry.field(name="contractPrice")
    renewed_from: Optional[FileContractID] = strawberry.field(name="renewedFrom")
    start_height: Optional[int] = strawberry.field(name="startHeight")
    state: Optional[str] = strawberry.field(name="state")
    total_cost: Optional[Currency] = strawberry.field(name="totalCost")


@strawberry.type
class ContractsArchiveRequest(SiaType):  # 	ContractsArchiveRequest = map[types.FileContractID]string
    contracts: Optional[JSON] = strawberry.field(
        description="Map of contract IDs to their archive reasons", name="contracts"
    )  # Dict[FileContractID, str]


@strawberry.type
class ContractsPrunableDataResponse(SiaType):
    contracts: Optional[List[ContractPrunableData]] = strawberry.field(name="contracts")
    total_prunable: Optional[int] = strawberry.field(name="totalPrunable")
    total_size: Optional[int] = strawberry.field(name="totalSize")


@strawberry.type
class ContractsOpts(SiaType):
    contract_set: Optional[str] = strawberry.field(name="contractset")


@strawberry.type
class HostsPriceTablesRequest(SiaType):
    price_table_updates: Optional[List[JSON]] = strawberry.field(
        description="List of price table updates (host -> updated price table info)", name="priceTableUpdates"
    )


@strawberry.type
class HostsRemoveRequest(SiaType):
    max_downtime_hours: Optional[DurationH] = strawberry.field(name="maxDowntimeHours")
    max_consecutive_scan_failures: Optional[int] = strawberry.field(name="maxConsecutiveScanFailures")


@strawberry.type
class SearchHostsRequest(SiaType):
    offset: Optional[int] = strawberry.field(name="offset")
    limit: Optional[int] = strawberry.field(name="limit")
    autopilot_id: Optional[str] = strawberry.field(name="autopilotID")
    filter_mode: Optional[str] = strawberry.field(name="filterMode")
    usability_mode: Optional[str] = strawberry.field(name="usabilityMode")
    address_contains: Optional[str] = strawberry.field(name="addressContains")
    key_in: Optional[List[PublicKey]] = strawberry.field(name="keyIn")


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
class HostInteractions(SiaType):
    total_scans: Optional[int] = strawberry.field(
        description="The total number of scans performed on the host", name="totalScans"
    )
    last_scan: Optional[datetime.datetime] = strawberry.field(
        description="Timestamp of the last scan performed", name="lastScan"
    )
    last_scan_success: Optional[bool] = strawberry.field(
        description="Indicates whether the last scan was successful", name="lastScanSuccess"
    )
    lost_sectors: Optional[int] = strawberry.field(
        description="Number of sectors lost since the last reporting period", name="lostSectors"
    )
    second_to_last_scan_success: Optional[bool] = strawberry.field(
        description="Indicates whether the second-to-last scan was successful", name="secondToLastScanSuccess"
    )
    uptime: Optional[Duration] = strawberry.field(description="Total uptime duration of the host", name="uptime")
    downtime: Optional[Duration] = strawberry.field(description="Total downtime duration of the host", name="downtime")
    successful_interactions: Optional[float] = strawberry.field(
        description="The number of successful interactions with the host", name="successfulInteractions"
    )
    failed_interactions: Optional[float] = strawberry.field(
        description="The number of failed interactions with the host", name="failedInteractions"
    )


@strawberry.type
class HostAddress(SiaType):
    public_key: Optional[PublicKey] = strawberry.field(description="The public key of the host", name="publicKey")
    net_address: Optional[str] = strawberry.field(description="The network address of the host", name="netAddress")


@strawberry.type
class HostResponse(SiaType):
    host: Optional[Host] = strawberry.field(description="Host information", name="host")
    checks: Optional[HostChecks] = strawberry.field(description="Host check results", name="checks")


@strawberry.type
class HostScan(SiaType):
    host_key: Optional[PublicKey] = strawberry.field(name="hostKey")
    price_table: Optional[HostPriceTable] = strawberry.field(name="priceTable")
    settings: Optional[HostV2Settings] = strawberry.field(name="settings")
    resolved_addresses: Optional[List[str]] = strawberry.field(name="resolvedAddresses")
    subnets: Optional[List[str]] = strawberry.field(name="subnets")
    success: Optional[bool] = strawberry.field(name="success")
    timestamp: Optional[datetime.datetime] = strawberry.field(name="timestamp")


@strawberry.type
class HostsScanRequest(SiaType):
    """Request containing host scan results"""

    scans: Optional[List[HostScan]] = strawberry.field(description="List of host scan results", name="scans")


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
class ContractPruneMetricRequestPUT(SiaType):
    metrics: Optional[List[ContractPruneMetric]] = strawberry.field(name="metrics")


@strawberry.type
class ContractMetricRequestPUT(SiaType):
    metrics: Optional[List[ContractMetric]] = strawberry.field(name="metrics")


@strawberry.type
class CreateMultipartOptions(SiaType):
    generate_key: Optional[bool] = strawberry.field(name="generateKey")
    key: Optional[EncryptionKey] = strawberry.field(name="key")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")


@strawberry.type
class CompleteMultipartOptions(SiaType):
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")  # Dict[str, str]


@strawberry.type
class MultipartAbortRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    key: Optional[str] = strawberry.field(name="key")
    upload_id: Optional[str] = strawberry.field(name="uploadID")


@strawberry.type
class MultipartAddPartRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    e_tag: Optional[str] = strawberry.field(name="eTag")
    path: Optional[str] = strawberry.field(name="path")
    contract_set: Optional[str] = strawberry.field(name="contractSet")
    upload_id: Optional[str] = strawberry.field(name="uploadID")
    part_number: Optional[int] = strawberry.field(name="partNumber")
    slices: Optional[List[SlabSlice]] = strawberry.field(name="slices", description="List of slices (object.SlabSlice)")


@strawberry.type
class MultipartCompleteResponse(SiaType):
    e_tag: Optional[ETag] = strawberry.field(name="eTag")


@strawberry.type
class MultipartCompleteRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")  # Dict[str, str]
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
    path: Optional[str] = strawberry.field(name="path")
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
    path_marker: Optional[str] = strawberry.field(name="pathMarker")
    upload_id_marker: Optional[str] = strawberry.field(name="uploadIDMarker")
    limit: Optional[int] = strawberry.field(name="limit")


@strawberry.type
class MultipartListUploadsResponse(SiaType):
    has_more: Optional[bool] = strawberry.field(name="hasMore")
    next_path_marker: Optional[str] = strawberry.field(name="nextMarker")
    next_upload_id_marker: Optional[str] = strawberry.field(name="nextUploadIDMarker")
    uploads: Optional[List[MultipartUpload]] = strawberry.field(name="uploads")


@strawberry.type
class ContentRange(SiaType):
    offset: Optional[int] = strawberry.field(description="The offset of the range", name="offset")
    length: Optional[int] = strawberry.field(description="The length of the range", name="length")
    size: Optional[int] = strawberry.field(description="The total size", name="size")


@strawberry.type
class ObjectsListRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    limit: Optional[int] = strawberry.field(name="limit")
    sort_by: Optional[str] = strawberry.field(name="sortBy")
    sort_dir: Optional[str] = strawberry.field(name="sortDir")
    prefix: Optional[str] = strawberry.field(name="prefix")
    marker: Optional[str] = strawberry.field(name="marker")


@strawberry.type
class ObjectsListResponse(SiaType):
    has_more: Optional[bool] = strawberry.field(description="Whether there are more objects to list", name="hasMore")
    next_marker: Optional[str] = strawberry.field(description="Marker for the next page of results", name="nextMarker")
    objects: Optional[List[ObjectMetadata]] = strawberry.field(
        description="List of object metadata entries", name="objects"
    )


@strawberry.type
class HeadObjectResponse(SiaType):
    content_type: Optional[str] = strawberry.field(name="contentType")
    etag: Optional[str] = strawberry.field(name="etag")
    last_modified: Optional[datetime.datetime] = strawberry.field(name="lastModified")
    range: Optional[ContentRange] = strawberry.field(name="range", description="ContentRange")
    size: Optional[int] = strawberry.field(name="size")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")  # Dict[str, str]


@strawberry.type
class GetObjectResponse(HeadObjectResponse):
    content: Optional[str] = strawberry.field(name="content")


@strawberry.type
class ObjectsResponse(SiaType):
    has_more: Optional[bool] = strawberry.field(description="Whether there are more entries", name="hasMore")
    entries: Optional[List[ObjectMetadata]] = strawberry.field(name="entries")
    object: Optional[Object] = strawberry.field(name="object")


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
    e_tag: Optional[ETag] = strawberry.field(name="eTag")
    mime_type: Optional[str] = strawberry.field(name="MimeType")
    metadata: Optional[JSON] = strawberry.field(name="Metadata", description="ObjectUserMetadata")  # Dict[str, str]


@strawberry.type
class AddObjectRequest(SiaType):
    bucket: Optional[str] = strawberry.field(name="bucket")
    contract_set: Optional[str] = strawberry.field(name="contractSet")
    object_data: Optional[JSON] = strawberry.field(name="object", description="object.Object")
    e_tag: Optional[ETag] = strawberry.field(name="eTag")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")


@strawberry.type
class CopyObjectOptions(SiaType):
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")  # Dict[str, str]


@strawberry.type
class CopyObjectsRequest(SiaType):
    source_bucket: Optional[str] = strawberry.field(name="sourceBucket")
    source_path: Optional[str] = strawberry.field(name="sourcePath")
    destination_bucket: Optional[str] = strawberry.field(name="destinationBucket")
    destination_path: Optional[str] = strawberry.field(name="destinationPath")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")  # Dict[str, str]


@strawberry.type
class DownloadRange(SiaType):
    offset: Optional[int] = strawberry.field(description="The offset of the range in bytes", name="offset")
    length: Optional[int] = strawberry.field(description="The length of the range in bytes", name="length")


@strawberry.type
class HeadObjectOptions(SiaType):
    ignore_delim: Optional[bool] = strawberry.field(name="ignoreDelim")
    range_arg: Optional[DownloadRange] = strawberry.field(name="range", description="DownloadRange")


@strawberry.type
class GetObjectOptions(SiaType):
    prefix: Optional[str] = strawberry.field(name="prefix")
    offset: Optional[int] = strawberry.field(name="offset")
    limit: Optional[int] = strawberry.field(name="limit")
    ignore_delim: Optional[bool] = strawberry.field(name="ignoreDelim")
    marker: Optional[str] = strawberry.field(name="marker")
    only_metadata: Optional[bool] = strawberry.field(name="onlyMetadata")
    sort_by: Optional[str] = strawberry.field(name="sortBy")
    sort_dir: Optional[str] = strawberry.field(name="sortDir")


@strawberry.type
class DownloadObjectOptions(GetObjectOptions):
    range: Optional[DownloadRange] = strawberry.field(name="range", description="DownloadRange")


@strawberry.type
class ListObjectOptions(SiaType):
    prefix: Optional[str] = strawberry.field(name="prefix")
    marker: Optional[str] = strawberry.field(name="marker")
    limit: Optional[int] = strawberry.field(name="limit")
    sort_by: Optional[str] = strawberry.field(name="sortBy")
    sort_dir: Optional[str] = strawberry.field(name="sortDir")


@strawberry.type
class UploadObjectOptions(SiaType):
    min_shards: Optional[int] = strawberry.field(name="minShards")
    total_shards: Optional[int] = strawberry.field(name="totalShards")
    contract_set: Optional[str] = strawberry.field(name="contractSet")
    content_length: Optional[int] = strawberry.field(name="contentLength")
    mime_type: Optional[str] = strawberry.field(name="mimeType")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="ObjectUserMetadata")  # Dict[str, str]


@strawberry.type
class DeleteObjectOptions(SiaType):
    batch: Optional[bool] = strawberry.field(name="batch")


@strawberry.type
class UploadObjectResponse(SiaType):
    etag: Optional[str] = strawberry.field(description="ETag of the uploaded object", name="etag")


@strawberry.type
class UploadMultipartUploadPartOptions(SiaType):
    contract_set: Optional[str] = strawberry.field(name="contractSet")
    min_shards: Optional[int] = strawberry.field(name="minShards")
    total_shards: Optional[int] = strawberry.field(name="totalShards")
    encryption_offset: Optional[int] = strawberry.field(name="encryptionOffset")
    content_length: Optional[int] = strawberry.field(name="contentLength")


@strawberry.type
class S3AuthenticationSettings(SiaType):
    v4_keypairs: Optional[JSON] = strawberry.field(
        name="v4Keypairs", description="Mapping of accessKeyID -> secretAccessKey"
    )  # Dict[str, str]


@strawberry.type
class UnhealthySlab(SiaType):
    encryption_key: Optional[EncryptionKey] = strawberry.field(
        name="key", description="Encryption key object (object.EncryptionKey)"
    )
    health: Optional[float] = strawberry.field(name="health")


@strawberry.type
class AddPartialSlabResponse(SiaType):
    slab_buffer_max_size_soft_reached: Optional[bool] = strawberry.field(name="slabBufferMaxSizeSoftReached")
    slabs: Optional[List[SlabSlice]] = strawberry.field(description="List of slabs (object.SlabSlice)", name="slabs")


@strawberry.type
class MigrationSlabsRequest(SiaType):
    contract_set: Optional[str] = strawberry.field(name="contractSet")
    health_cutoff: Optional[float] = strawberry.field(name="healthCutoff")
    limit: Optional[int] = strawberry.field(name="limit")


@strawberry.type
class PackedSlabsRequestGET(SiaType):
    locking_duration: Optional[DurationMS] = strawberry.field(name="lockingDuration")
    min_shards: Optional[int] = strawberry.field(name="minShards")
    total_shards: Optional[int] = strawberry.field(name="totalShards")
    contract_set: Optional[str] = strawberry.field(name="contractSet")
    limit: Optional[int] = strawberry.field(name="limit")


@strawberry.type
class PackedSlabsRequestPOST(SiaType):
    slabs: Optional[List[UploadedPackedSlab]] = strawberry.field(name="slabs")


@strawberry.type
class UploadSectorRequest(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(
        description="Contract ID for the upload", name="contractID"
    )
    root: Optional[Hash256] = strawberry.field(description="Root hash of the sector", name="root")


@strawberry.type
class UnhealthySlabsResponse(SiaType):
    slabs: Optional[List[UnhealthySlab]] = strawberry.field(description="List of unhealthy slabs", name="slabs")


@strawberry.type
class UpdateSlabRequest(SiaType):
    contract_set: Optional[str] = strawberry.field(name="contractSet")
    slab: Optional[Slab] = strawberry.field(name="slab")


# ------ walletd --------


@strawberry.enum
class IndexMode(Enum):
    PERSONAL: str = strawberry.enum_value("personal", description="Personal mode - indexes only relevant transactions.")
    FULL: str = strawberry.enum_value("full", description="Full mode - indexes all transactions.")
    NONE: str = strawberry.enum_value("none", description="None mode - does not index transactions.")


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
    addr: Optional[str] = strawberry.field(name="address")
    inbound: Optional[bool] = strawberry.field(name="inbound")
    version: Optional[str] = strawberry.field(name="version")
    first_seen: Optional[datetime.datetime] = strawberry.field(name="firstSeen")
    connected_since: Optional[datetime.datetime] = strawberry.field(name="connectedSince")
    synced_blocks: Optional[int] = strawberry.field(name="syncedBlocks")
    sync_duration: Optional[Duration] = strawberry.field(name="syncDuration")


@strawberry.type
class TxpoolBroadcastRequest(SiaType):
    transactions: Optional[List[Transaction]] = strawberry.field(name="transactions", description="[]types.Transaction")
    v2transactions: Optional[List[V2Transaction]] = strawberry.field(
        name="v2transactions", description="[]types.V2Transaction"
    )


@strawberry.type
class TxpoolTransactionsResponse(SiaType):
    transactions: Optional[List[Transaction]] = strawberry.field(name="transactions", description="[]types.Transaction")
    v2transactions: Optional[List[V2Transaction]] = strawberry.field(
        name="v2transactions", description="[]types.V2Transaction"
    )


@strawberry.type
class WalletReserveRequest(SiaType):
    siacoin_outputs: Optional[List[SiacoinOutputID]] = strawberry.field(
        description="List of Siacoin output IDs to reserve", name="siacoinOutputs"
    )
    siafund_outputs: Optional[List[SiafundOutputID]] = strawberry.field(
        description="List of Siafund output IDs to reserve", name="siafundOutputs"
    )
    duration: Optional[Duration] = strawberry.field(description="Duration to reserve the outputs for", name="duration")


@strawberry.type
class WalletUpdateRequest(SiaType):
    name: Optional[str] = strawberry.field(name="name")
    description: Optional[str] = strawberry.field(name="description")
    metadata: Optional[JSON] = strawberry.field(name="metadata", description="json.RawMessage")


@strawberry.type
class WalletReleaseRequest(SiaType):
    siacoin_outputs: Optional[List[SiacoinOutputID]] = strawberry.field(
        name="siacoinOutputs", description="[]types.SiacoinOutputID"
    )
    siafund_outputs: Optional[List[SiafundOutputID]] = strawberry.field(
        name="siafundOutputs", description="[]types.SiafundOutputID"
    )


@strawberry.type
class WalletFundSFRequest(SiaType):
    transaction: Optional[Transaction] = strawberry.field(description="types.Transaction", name="transaction")
    amount: Optional[int] = strawberry.field(name="amount")
    change_address: Optional[Address] = strawberry.field(name="changeAddress", description="types.Address")
    claim_address: Optional[Address] = strawberry.field(name="claimAddress", description="types.Address")


@strawberry.type
class WalletFundRequest(SiaType):
    transaction: Optional[Transaction] = strawberry.field(name="transaction")
    amount: Optional[Currency] = strawberry.field(name="amount")
    change_address: Optional[Address] = strawberry.field(name="changeAddress")


@strawberry.type
class WalletRedistributeRequest(SiaType):
    amount: Optional[Currency] = strawberry.field(name="amount")
    outputs: Optional[int] = strawberry.field(name="outputs")


@strawberry.type
class WalletResponse(SiaType):
    scan_height: Optional[int] = strawberry.field(name="scanHeight")
    address: Optional[Address] = strawberry.field(name="address")
    spendable: Optional[Currency] = strawberry.field(name="spendable")
    confirmed: Optional[Currency] = strawberry.field(name="confirmed")
    unconfirmed: Optional[Currency] = strawberry.field(name="unconfirmed")
    immature: Optional[Currency] = strawberry.field(name="immature")


@strawberry.type
class WalletSendRequest(SiaType):
    address: Optional[Address] = strawberry.field(name="address")
    amount: Optional[Currency] = strawberry.field(name="amount")
    subtract_miner_fee: Optional[bool] = strawberry.field(name="subtractMinerFee")
    use_unconfirmed: Optional[bool] = strawberry.field(name="useUnconfirmed")


@strawberry.type
class WalletSignRequest(SiaType):
    transaction: Optional[Transaction] = strawberry.field(name="transaction")
    to_sign: Optional[List[Hash256]] = strawberry.field(name="toSign")
    covered_fields: Optional[CoveredFields] = strawberry.field(name="coveredFields")


@strawberry.type
class WalletFundResponse(SiaType):
    transaction: Optional[Transaction] = strawberry.field(description="types.Transaction", name="transaction")
    to_sign: Optional[List[Hash256]] = strawberry.field(name="toSign")
    depends_on: Optional[List[Transaction]] = strawberry.field(name="dependsOn", description="[]types.Transaction")


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
class WalletEvent(SiaType):
    id: Optional[Hash256] = strawberry.field(description="Unique identifier for the event", name="id")
    index: Optional[ChainIndex] = strawberry.field(description="Chain index where event occurred", name="index")
    type: Optional[str] = strawberry.field(description="Type of event", name="type")
    data: Optional[JSON] = strawberry.field(description="Event-specific data", name="data")
    maturity_height: Optional[int] = strawberry.field(
        description="Block height when event matures", name="maturityHeight"
    )
    timestamp: Optional[datetime.datetime] = strawberry.field(description="Time event occurred", name="timestamp")
    relevant: Optional[List[Address]] = strawberry.field(description="Relevant addresses", name="relevant")


# ------ hostd --------


@strawberry.type
class SyncerConnectRequest(SiaType):
    address: Optional[str] = strawberry.field(name="address")


@strawberry.type
class BuildState(SiaType):
    version: Optional[str] = strawberry.field(name="version")
    commit: Optional[str] = strawberry.field(name="commit")
    os: Optional[str] = strawberry.field(name="os")
    build_time: Optional[datetime.datetime] = strawberry.field(name="buildTime")


@strawberry.type
class Announcement(SiaType):
    index: Optional[ChainIndex] = strawberry.field(
        description="Chain index when this announcement was made", name="index"
    )
    address: Optional[str] = strawberry.field(description="The host's announced network address", name="address")


@strawberry.type
class HostdState(BuildState):
    name: Optional[str] = strawberry.field(name="name")
    public_key: Optional[PublicKey] = strawberry.field(name="publicKey")
    last_announcement: Optional[Announcement] = strawberry.field(
        name="lastAnnouncement", description="settings.Announcement"
    )
    start_time: Optional[datetime.datetime] = strawberry.field(name="startTime")
    explorer: Optional[ExplorerState] = strawberry.field(name="explorer")


# --
@strawberry.type
class Revenue(SiaType):
    rpc: Optional[Currency] = strawberry.field(name="rpc")
    storage: Optional[Currency] = strawberry.field(name="storage")
    ingress: Optional[Currency] = strawberry.field(name="ingress")
    egress: Optional[Currency] = strawberry.field(name="egress")
    registry_read: Optional[Currency] = strawberry.field(name="registryRead")
    registry_write: Optional[Currency] = strawberry.field(name="registryWrite")


@strawberry.type
class RHPData(SiaType):
    ingress: Optional[int] = strawberry.field(description="The number of bytes received by the host", name="ingress")
    egress: Optional[int] = strawberry.field(description="The number of bytes sent by the host", name="egress")


@strawberry.type
class DataMetrics(SiaType):
    rhp: Optional[RHPData] = strawberry.field(name="rhp")


@strawberry.type
class Contracts(SiaType):
    active: Optional[int] = strawberry.field(name="active")
    rejected: Optional[int] = strawberry.field(name="rejected")
    failed: Optional[int] = strawberry.field(name="failed")
    renewed: Optional[int] = strawberry.field(name="renewed")
    successful: Optional[int] = strawberry.field(name="successful")
    locked_collateral: Optional[Currency] = strawberry.field(name="lockedCollateral")
    risked_collateral: Optional[Currency] = strawberry.field(name="riskedCollateral")


@strawberry.type
class Accounts(SiaType):
    active: Optional[int] = strawberry.field(name="active")
    balance: Optional[Currency] = strawberry.field(name="balance")


@strawberry.type
class Pricing(SiaType):
    contract_price: Optional[Currency] = strawberry.field(name="contractPrice")
    ingress_price: Optional[Currency] = strawberry.field(name="ingressPrice")
    egress_price: Optional[Currency] = strawberry.field(name="egressPrice")
    base_rpc_price: Optional[Currency] = strawberry.field(name="baseRPCPrice")
    sector_access_price: Optional[Currency] = strawberry.field(name="sectorAccessPrice")
    storage_price: Optional[Currency] = strawberry.field(name="storagePrice")
    collateral_multiplier: Optional[float] = strawberry.field(name="collateralMultiplier")


@strawberry.type
class Registry(SiaType):
    entries: Optional[int] = strawberry.field(name="entries")
    max_entries: Optional[int] = strawberry.field(name="maxEntries")
    reads: Optional[int] = strawberry.field(name="reads")
    writes: Optional[int] = strawberry.field(name="writes")


@strawberry.type
class Storage(SiaType):
    total_sectors: Optional[int] = strawberry.field(name="totalSectors")
    physical_sectors: Optional[int] = strawberry.field(name="physicalSectors")
    lost_sectors: Optional[int] = strawberry.field(name="lostSectors")
    contract_sectors: Optional[int] = strawberry.field(name="contractSectors")
    temp_sectors: Optional[int] = strawberry.field(name="tempSectors")
    reads: Optional[int] = strawberry.field(name="reads")
    writes: Optional[int] = strawberry.field(name="writes")
    sector_cache_hits: Optional[int] = strawberry.field(name="sectorCacheHits")
    sector_cache_misses: Optional[int] = strawberry.field(name="sectorCacheMisses")


@strawberry.type
class RevenueMetrics(SiaType):
    potential: Optional[Revenue] = strawberry.field(name="potential")
    earned: Optional[Revenue] = strawberry.field(name="earned")


@strawberry.type
class WalletMetrics(SiaType):
    balance: Optional[Currency] = strawberry.field(name="balance")
    immature_balance: Optional[Currency] = strawberry.field(name="immatureBalance")


@strawberry.type
class Metrics(SiaType):
    accounts: Optional[Accounts] = strawberry.field(name="accounts")
    revenue: Optional[RevenueMetrics] = strawberry.field(name="revenue")
    pricing: Optional[Pricing] = strawberry.field(name="pricing")
    contracts: Optional[Contracts] = strawberry.field(name="contracts")
    storage: Optional[Storage] = strawberry.field(name="storage")
    registry: Optional[Registry] = strawberry.field(name="registry")
    data: Optional[DataMetrics] = strawberry.field(name="data")
    wallet: Optional[WalletMetrics] = strawberry.field(name="wallet")
    timestamp: Optional[datetime.datetime] = strawberry.field(name="timestamp")


# --


@strawberry.type
class Route53Settings(SiaType):
    id: Optional[str] = strawberry.field(name="id")
    secret: Optional[str] = strawberry.field(name="secret")
    zone_id: Optional[str] = strawberry.field(name="zoneID")


@strawberry.type
class NoIPSettings(SiaType):
    email: Optional[str] = strawberry.field(name="email")
    password: Optional[str] = strawberry.field(name="password")


@strawberry.type
class DuckDNSSettings(SiaType):
    token: Optional[str] = strawberry.field(name="token")


@strawberry.type
class CloudflareSettings(SiaType):
    token: Optional[str] = strawberry.field(name="token")
    zone_id: Optional[str] = strawberry.field(name="zoneID")


@strawberry.type
class DNSSettings(SiaType):
    provider: Optional[str] = strawberry.field(name="provider")
    ipv4: Optional[bool] = strawberry.field(name="ipv4")
    ipv6: Optional[bool] = strawberry.field(name="ipv6")
    options: Optional[JSON] = strawberry.field(name="options")


@strawberry.type
class HostSettings(SiaType):
    # Host settings
    accepting_contracts: Optional[bool] = strawberry.field(
        description="Whether the host is accepting new contracts", name="acceptingContracts"
    )
    net_address: Optional[str] = strawberry.field(description="Network address of the host", name="netAddress")
    max_contract_duration: Optional[int] = strawberry.field(
        description="Maximum allowed contract duration in blocks", name="maxContractDuration"
    )
    window_size: Optional[int] = strawberry.field(description="Size of the proof window in blocks", name="windowSize")

    # Pricing
    contract_price: Optional[Currency] = strawberry.field(
        description="Cost to form a contract with the host", name="contractPrice"
    )
    base_rpc_price: Optional[Currency] = strawberry.field(description="Base cost for RPCs", name="baseRPCPrice")
    sector_access_price: Optional[Currency] = strawberry.field(
        description="Cost to access a sector", name="sectorAccessPrice"
    )

    collateral_multiplier: Optional[float] = strawberry.field(
        description="Multiplier for collateral", name="collateralMultiplier"
    )
    max_collateral: Optional[Currency] = strawberry.field(
        description="Maximum collateral per contract", name="maxCollateral"
    )

    storage_price: Optional[Currency] = strawberry.field(
        description="Cost per byte per block of storage", name="storagePrice"
    )
    egress_price: Optional[Currency] = strawberry.field(
        description="Cost per byte of egress bandwidth", name="egressPrice"
    )
    ingress_price: Optional[Currency] = strawberry.field(
        description="Cost per byte of ingress bandwidth", name="ingressPrice"
    )

    price_table_validity: Optional[Duration] = strawberry.field(
        description="Duration a price table remains valid", name="priceTableValidity"
    )

    # Registry settings
    max_registry_entries: Optional[int] = strawberry.field(
        description="Maximum number of registry entries", name="maxRegistryEntries"
    )

    # RHP3 settings
    account_expiry: Optional[Duration] = strawberry.field(
        description="Duration before an account expires", name="accountExpiry"
    )
    max_account_balance: Optional[Currency] = strawberry.field(
        description="Maximum balance allowed in an account", name="maxAccountBalance"
    )

    # Bandwidth limiter settings
    ingress_limit: Optional[int] = strawberry.field(
        description="Maximum ingress bandwidth in bytes per second", name="ingressLimit"
    )
    egress_limit: Optional[int] = strawberry.field(
        description="Maximum egress bandwidth in bytes per second", name="egressLimit"
    )

    # DNS settings
    ddns: Optional[DNSSettings] = strawberry.field(description="Dynamic DNS settings", name="ddns")

    sector_cache_size: Optional[int] = strawberry.field(description="Size of sector cache", name="sectorCacheSize")

    revision: Optional[int] = strawberry.field(description="Settings revision number", name="revision")


@strawberry.type
class ContractIntegrityResponse(SiaType):
    bad_sectors: Optional[List[Hash256]] = strawberry.field(name="badSectors")
    total_sectors: Optional[int] = strawberry.field(name="totalSectors")


@strawberry.type
class AddVolumeRequest(SiaType):
    local_path: Optional[str] = strawberry.field(name="localPath")
    max_sectors: Optional[int] = strawberry.field(name="maxSectors")


@strawberry.type
class VolumeStats(SiaType):
    failed_reads: Optional[int] = strawberry.field(description="Number of failed read operations", name="failedReads")
    failed_writes: Optional[int] = strawberry.field(
        description="Number of failed write operations", name="failedWrites"
    )
    successful_reads: Optional[int] = strawberry.field(
        description="Number of successful read operations", name="successfulReads"
    )
    successful_writes: Optional[int] = strawberry.field(
        description="Number of successful write operations", name="successfulWrites"
    )
    status: Optional[str] = strawberry.field(description="Current status of the volume", name="status")
    errors: Optional[List[str]] = strawberry.field(description="List of error messages", name="errors")


@strawberry.type
class Volume(SiaType):
    id: Optional[int] = strawberry.field(description="Unique identifier for the volume", name="id")
    local_path: Optional[str] = strawberry.field(description="Local filesystem path of the volume", name="localPath")
    used_sectors: Optional[int] = strawberry.field(description="Number of sectors currently in use", name="usedSectors")
    total_sectors: Optional[int] = strawberry.field(
        description="Total number of sectors available", name="totalSectors"
    )
    read_only: Optional[bool] = strawberry.field(description="Whether the volume is read-only", name="readOnly")
    available: Optional[bool] = strawberry.field(
        description="Whether the volume is currently available", name="available"
    )


@strawberry.type
class VolumeMeta(Volume, VolumeStats):
    errors: Optional[List[str]] = strawberry.field(name="errors", description="List of error messages")


@strawberry.type
class UpdateVolumeRequest(SiaType):
    read_only: Optional[bool] = strawberry.field(name="readOnly")


@strawberry.type
class ResizeVolumeRequest(SiaType):
    max_sectors: Optional[int] = strawberry.field(name="maxSectors")


@strawberry.enum
class SectorAction(Enum):
    APPEND = strawberry.enum_value("append", description="Append sector action")
    UPDATE = strawberry.enum_value("update", description="Update sector action")
    SWAP = strawberry.enum_value("swap", description="Swap sector action")
    TRIM = strawberry.enum_value("trim", description="Trim sector action")


@strawberry.enum
class ContractStatus(Enum):
    # Contract has been formed but not yet confirmed on blockchain
    PENDING = strawberry.enum_value(0, description="Contract has been formed but not yet confirmed on blockchain")
    # Contract formation transaction was never confirmed
    REJECTED = strawberry.enum_value(1, description="Contract formation transaction was never confirmed")
    # Contract is confirmed and currently active
    ACTIVE = strawberry.enum_value(2, description="Contract is confirmed and currently active")
    # Storage proof confirmed or contract expired without host burning Siacoin
    SUCCESSFUL = strawberry.enum_value(
        3, description="Storage proof confirmed or contract expired without host burning Siacoin"
    )
    # Contract ended without storage proof and host burned Siacoin
    FAILED = strawberry.enum_value(4, description="Contract ended without storage proof and host burned Siacoin")


@strawberry.enum
class V2ContractStatus(Enum):
    # Contract has been formed but not yet confirmed on blockchain
    PENDING = strawberry.enum_value(
        "pending", description="Contract has been formed but not yet confirmed on blockchain"
    )
    # Contract formation transaction was never confirmed
    REJECTED = strawberry.enum_value("rejected", description="Contract formation transaction was never confirmed")
    # Contract is confirmed and currently active
    ACTIVE = strawberry.enum_value("active", description="Contract is confirmed and currently active")
    # Contract has been renewed
    RENEWED = strawberry.enum_value("renewed", description="Contract has been renewed")
    # Storage proof confirmed or contract expired without host burning Siacoin
    SUCCESSFUL = strawberry.enum_value(
        "successful", description="Storage proof confirmed or contract expired without host burning Siacoin"
    )
    # Contract ended without storage proof and host burned Siacoin
    FAILED = strawberry.enum_value("failed", description="Contract ended without storage proof and host burned Siacoin")


@strawberry.enum
class ContractSortField(Enum):
    STATUS = strawberry.enum_value("status", description="Sort by contract status")
    NEGOTIATION_HEIGHT = strawberry.enum_value("negotiationHeight", description="Sort by negotiation height")
    EXPIRATION_HEIGHT = strawberry.enum_value("expirationHeight", description="Sort by expiration height")


@strawberry.type
class SignedRevision(SiaType):
    revision: Optional[FileContractRevision] = strawberry.field(name="revision")
    host_signature: Optional[Signature] = strawberry.field(name="hostSignature")
    renter_signature: Optional[Signature] = strawberry.field(name="renterSignature")


@strawberry.type
class Usage(SiaType):
    rpc_revenue: Optional[Currency] = strawberry.field(name="rpc")
    storage_revenue: Optional[Currency] = strawberry.field(name="storage")
    egress_revenue: Optional[Currency] = strawberry.field(name="egress")
    ingress_revenue: Optional[Currency] = strawberry.field(name="ingress")
    registry_read: Optional[Currency] = strawberry.field(name="registryRead")
    registry_write: Optional[Currency] = strawberry.field(name="registryWrite")
    account_funding: Optional[Currency] = strawberry.field(name="accountFunding")
    risked_collateral: Optional[Currency] = strawberry.field(name="riskedCollateral")


@strawberry.type
class Proto4Usage(SiaType):
    rpc: Optional[Currency] = strawberry.field(name="rpc")
    storage: Optional[Currency] = strawberry.field(name="storage")
    egress: Optional[Currency] = strawberry.field(name="egress")
    ingress: Optional[Currency] = strawberry.field(name="ingress")
    account_funding: Optional[Currency] = strawberry.field(name="accountFunding")
    risked_collateral: Optional[Currency] = strawberry.field(name="collateral")


@strawberry.type
class V2Contract(V2FileContract):
    id: Optional[FileContractID] = strawberry.field(name="id")
    status: Optional[V2ContractStatus] = strawberry.field(name="status")
    usage: Optional[Proto4Usage] = strawberry.field(name="usage")
    negotiation_height: Optional[int] = strawberry.field(name="negotiationHeight")
    revision_confirmed: Optional[bool] = strawberry.field(name="revisionConfirmed")
    formation_index: Optional[ChainIndex] = strawberry.field(name="formationIndex")
    resolution_index: Optional[ChainIndex] = strawberry.field(name="resolutionHeight")
    renewed_to: Optional[FileContractID] = strawberry.field(name="renewedTo")
    renewed_from: Optional[FileContractID] = strawberry.field(name="renewedFrom")


@strawberry.type
class HostdContract(SignedRevision):
    status: Optional[ContractStatus] = strawberry.field(name="status")
    locked_collateral: Optional[Currency] = strawberry.field(name="lockedCollateral")
    usage: Optional[Usage] = strawberry.field(name="usage")
    negotiation_height: Optional[int] = strawberry.field(name="negotiationHeight")
    formation_confirmed: Optional[bool] = strawberry.field(name="formationConfirmed")
    revision_confirmed: Optional[bool] = strawberry.field(name="revisionConfirmed")
    resolution_height: Optional[int] = strawberry.field(name="resolutionHeight")
    renewed_to: Optional[FileContractID] = strawberry.field(name="renewedTo")
    renewed_from: Optional[FileContractID] = strawberry.field(name="renewedFrom")


@strawberry.type
class ContractFilter(SiaType):
    statuses: Optional[List[ContractStatus]] = strawberry.field(name="statuses")
    contract_ids: Optional[List[FileContractID]] = strawberry.field(name="contractIDs")
    renewed_from: Optional[List[FileContractID]] = strawberry.field(name="renewedFrom")
    renewed_to: Optional[List[FileContractID]] = strawberry.field(name="renewedTo")
    renter_key: Optional[List[PublicKey]] = strawberry.field(name="renterKey")
    min_negotiation_height: Optional[int] = strawberry.field(name="minNegotiationHeight")
    max_negotiation_height: Optional[int] = strawberry.field(name="maxNegotiationHeight")
    min_expiration_height: Optional[int] = strawberry.field(name="minExpirationHeight")
    max_expiration_height: Optional[int] = strawberry.field(name="maxExpirationHeight")
    limit: Optional[int] = strawberry.field(name="limit")
    offset: Optional[int] = strawberry.field(name="offset")
    sort_field: Optional[str] = strawberry.field(name="sortField")
    sort_desc: Optional[bool] = strawberry.field(name="sortDesc")


@strawberry.type
class V2ContractFilter(SiaType):
    statuses: Optional[List[V2ContractStatus]] = strawberry.field(name="statuses")
    contract_ids: Optional[List[FileContractID]] = strawberry.field(name="contractIDs")
    renewed_from: Optional[List[FileContractID]] = strawberry.field(name="renewedFrom")
    renewed_to: Optional[List[FileContractID]] = strawberry.field(name="renewedTo")
    renter_key: Optional[List[PublicKey]] = strawberry.field(name="renterKey")
    min_negotiation_height: Optional[int] = strawberry.field(name="minNegotiationHeight")
    max_negotiation_height: Optional[int] = strawberry.field(name="maxNegotiationHeight")
    min_expiration_height: Optional[int] = strawberry.field(name="minExpirationHeight")
    max_expiration_height: Optional[int] = strawberry.field(name="maxExpirationHeight")
    limit: Optional[int] = strawberry.field(name="limit")
    offset: Optional[int] = strawberry.field(name="offset")
    sort_field: Optional[str] = strawberry.field(name="sortField")
    sort_desc: Optional[bool] = strawberry.field(name="sortDesc")


@strawberry.type
class SectorChange(SiaType):
    action: Optional[SectorAction] = strawberry.field(name="action")
    root: Optional[Hash256] = strawberry.field(name="root")
    a: Optional[int] = strawberry.field(name="a")
    b: Optional[int] = strawberry.field(name="b")


@strawberry.type
class HostdWalletResponse(Balance):
    address: Optional[Address] = strawberry.field(name="address")


@strawberry.type
class WalletSendSiacoinsRequest(SiaType):
    address: Optional[Address] = strawberry.field(name="address")
    amount: Optional[Currency] = strawberry.field(name="amount")
    subtract_miner_fee: Optional[bool] = strawberry.field(name="subtractMinerFee")


@strawberry.type
class Peer(SiaType):
    address: Optional[str] = strawberry.field(name="address")
    inbound: Optional[bool] = strawberry.field(name="inbound")
    version: Optional[str] = strawberry.field(name="version")
    first_seen: Optional[datetime.datetime] = strawberry.field(name="firstSeen")
    connected_since: Optional[datetime.datetime] = strawberry.field(name="connectedSince")
    synced_blocks: Optional[int] = strawberry.field(name="syncedBlocks")
    sync_duration: Optional[Duration] = strawberry.field(name="syncDuration")


@strawberry.type
class SystemDirResponse(SiaType):
    path: Optional[str] = strawberry.field(name="path")
    total_bytes: Optional[int] = strawberry.field(name="totalBytes")
    free_bytes: Optional[int] = strawberry.field(name="freeBytes")
    directories: Optional[List[str]] = strawberry.field(name="directories")


@strawberry.type
class CreateDirRequest(SiaType):
    path: Optional[str] = strawberry.field(name="path")


@strawberry.type
class VerifySectorResponse(SiaType):
    sector_ref: Optional[JSON] = strawberry.field(name="sectorReference")
    error: Optional[str] = strawberry.field(name="error")


@strawberry.type
class RegisterWebHookRequest(SiaType):
    callback_url: Optional[str] = strawberry.field(name="callbackURL")
    scopes: Optional[List[str]] = strawberry.field(name="scopes")


@strawberry.type
class FundingSource(SiaType):
    contract_id: Optional[FileContractID] = strawberry.field(name="contractID")
    account_id: Optional[PublicKey] = strawberry.field(name="accountID")  # rhp3.Account is a PublicKey
    amount: Optional[Currency] = strawberry.field(name="amount")


@strawberry.type
class HostdAccount(SiaType):
    id: Optional[PublicKey] = strawberry.field(name="id")  # rhp3.Account is a PublicKey
    balance: Optional[Currency] = strawberry.field(name="balance")
    expiration: Optional[datetime.datetime] = strawberry.field(name="expiration")


@strawberry.type
class FundAccountWithContract(SiaType):
    account: Optional[PublicKey] = strawberry.field()  # rhp3.Account is a PublicKey
    cost: Optional[Currency] = strawberry.field()
    amount: Optional[Currency] = strawberry.field()
    revision: Optional[SignedRevision] = strawberry.field()
    expiration: Optional[datetime.datetime] = strawberry.field()


@strawberry.type
class IntegrityResult(SiaType):
    expected_root: Optional[Hash256] = strawberry.field(
        description="The expected root hash for this sector", name="expectedRoot"
    )
    actual_root: Optional[Hash256] = strawberry.field(
        description="The actual root hash found during verification", name="actualRoot"
    )
    error: Optional[str] = strawberry.field(description="Error message if verification failed", name="error")


@strawberry.type
class IntegrityCheckResult(SiaType):
    start: Optional[datetime.datetime] = strawberry.field(description="Start time of the integrity check", name="start")
    end: Optional[datetime.datetime] = strawberry.field(description="End time of the integrity check", name="end")
    checked_sectors: Optional[int] = strawberry.field(
        description="Number of sectors that were checked", name="checkedSectors"
    )
    total_sectors: Optional[int] = strawberry.field(
        description="Total number of sectors in the contract", name="totalSectors"
    )
    bad_sectors: Optional[List[IntegrityResult]] = strawberry.field(
        description="List of sectors that failed the integrity check", name="badSectors"
    )


@strawberry.enum
class MetricsInterval(Enum):
    FIVE_MINUTES = strawberry.enum_value("5m", description="5 minute interval")
    FIFTEEN_MINUTES = strawberry.enum_value("15m", description="15 minute interval")
    HOURLY = strawberry.enum_value("hourly", description="1 hour interval")
    DAILY = strawberry.enum_value("daily", description="1 day interval")
    WEEKLY = strawberry.enum_value("weekly", description="1 week interval")
    MONTHLY = strawberry.enum_value("monthly", description="1 month interval")
    YEARLY = strawberry.enum_value("yearly", description="1 year interval")


print(SearchHostsRequest.Input)  # Check if this returns a valid input type
