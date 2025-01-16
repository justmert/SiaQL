from datetime import datetime
from typing import Any, Dict, List, Optional

import strawberry
from strawberry.types import Info

from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from siaql.graphql.schemas.types import (
    AddWalletAddressInput,
    AddWalletAddressResponse,
    AddWalletInput,
    BlockIndex,
    ConstructedTransaction,
    DeleteWalletAddressResponse,
    DeleteWalletResponse,
    FundTransactionResponse,
    MerkleProof,
    ReleaseUTXOsResponse,
    ReserveUTXOsResponse,
    SiacoinInput,
    SiacoinOutput,
    SiacoinRecipientInput,
    SiacoinUTXO,
    SiafundOutput,
    SiafundRecipientInput,
    SiafundUTXO,
    Transaction,
    TransactionBasis,
    TransactionData,
    TransactionInput,
    TransactionSignature,
    UnlockConditions,
    V1Transaction,
    Wallet,
    WalletAddress,
    WalletBalance,
    WalletEvent,
)


@strawberry.type
class WalletQueries(WalletdBaseResolver):
    @strawberry.field
    async def wallets(self, info: Info) -> List[Wallet]:
        """Returns a list of all created wallets"""
        data = await WalletdBaseResolver.handle_api_call(info, "get_wallets")
        return [
            Wallet(
                id=wallet["id"],
                name=wallet["name"],
                description=wallet["description"],
                date_created=datetime.fromisoformat(wallet["dateCreated"].replace("Z", "+00:00")),
                last_updated=datetime.fromisoformat(wallet["lastUpdated"].replace("Z", "+00:00")),
                metadata=wallet.get("metadata"),
            )
            for wallet in data
        ]

    @strawberry.field
    async def wallet_addresses(self, info: Info, wallet_id: str) -> List[WalletAddress]:
        """Returns a list of addresses associated with the wallet"""
        data = await WalletdBaseResolver.handle_api_call(info, "get_wallet_addresses", wallet_id=wallet_id)
        return [
            WalletAddress(address=addr["address"], description=addr["description"], metadata=addr.get("metadata"))
            for addr in data
        ]

    @strawberry.field
    async def wallet_balance(self, info: Info, wallet_id: str) -> WalletBalance:
        """Returns the current balance of the wallet"""
        data = await WalletdBaseResolver.handle_api_call(info, "get_wallet_balance", wallet_id=wallet_id)
        return WalletBalance(
            siacoins=data["siacoins"], immature_siacoins=data["immatureSiacoins"], siafunds=data["siafunds"]
        )

    @strawberry.field
    async def wallet_siacoin_utxos(
        self, info: Info, wallet_id: str, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[SiacoinUTXO]:
        """Returns a paginated list of Siacoin UTXOs for the wallet.

        Args:
            wallet_id: ID of the wallet to get UTXOs for
            limit: Maximum number of UTXOs to return
            offset: Number of UTXOs to skip
        """
        data = await WalletdBaseResolver.handle_api_call(
            info, "get_wallet_siacoin_utxos", wallet_id=wallet_id, limit=limit, offset=offset
        )
        return [
            SiacoinUTXO(
                id=utxo["id"],
                leaf_index=utxo["leafIndex"],
                merkle_proof=MerkleProof(hashes=utxo["merkleProof"]),
                siacoin_output=SiacoinOutput(
                    value=utxo["siacoinOutput"]["value"], address=utxo["siacoinOutput"]["address"]
                ),
                maturity_height=utxo["maturityHeight"],
            )
            for utxo in data
        ]

    @strawberry.field
    async def wallet_siafund_utxos(
        self, info: Info, wallet_id: str, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[SiafundUTXO]:
        """Returns a paginated list of Siafund UTXOs for the wallet, sorted by value descending.

        Args:
            wallet_id: ID of the wallet to get UTXOs for
            limit: Maximum number of UTXOs to return
            offset: Number of UTXOs to skip
        """
        data = await WalletdBaseResolver.handle_api_call(
            info, "get_wallet_siafund_utxos", wallet_id=wallet_id, limit=limit, offset=offset
        )
        return [
            SiafundUTXO(
                id=utxo["id"],
                leaf_index=utxo["leafIndex"],
                merkle_proof=MerkleProof(hashes=utxo["merkleProof"]),
                siafund_output=SiafundOutput(
                    value=utxo["siafundOutput"]["value"], address=utxo["siafundOutput"]["address"]
                ),
                claim_start=utxo["claimStart"],
            )
            for utxo in data
        ]

    @strawberry.field
    async def unconfirmed_events(self, info: Info, wallet_id: str) -> List[WalletEvent]:
        """Returns any unconfirmed events relevant to the wallet"""
        data = await WalletdBaseResolver.handle_api_call(info, "get_unconfirmed_events", wallet_id=wallet_id)
        return [
            WalletEvent(
                id=event["id"],
                index=BlockIndex(height=event["index"]["height"], id=event["index"]["id"]),
                timestamp=datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00")),
                maturity_height=event["maturityHeight"],
                type=event["type"],
                data=TransactionData(
                    transaction=V1Transaction(
                        siacoin_inputs=[
                            SiacoinInput(parent_id=input["parentID"], unlock_conditions=input["unlockConditions"])
                            for input in event["data"]["transaction"]["siacoinInputs"]
                        ],
                        siacoin_outputs=[
                            SiacoinOutput(value=output["value"], address=output["address"])
                            for output in event["data"]["transaction"]["siacoinOutputs"]
                        ],
                        miner_fees=event["data"]["transaction"]["minerFees"],
                        signatures=[
                            TransactionSignature(
                                parent_id=sig["parentID"],
                                public_key_index=sig["publicKeyIndex"],
                                covered_fields=sig["coveredFields"],
                                signature=sig["signature"],
                            )
                            for sig in event["data"]["transaction"]["signatures"]
                        ],
                    ),
                    spent_siacoin_elements=event["data"].get("spentSiacoinElements"),
                    spent_siafund_elements=event["data"].get("spentSiafundElements"),
                ),
                relevant=event["relevant"],
            )
            for event in data
        ]


@strawberry.type
class WalletMutations(WalletdBaseResolver):
    @strawberry.mutation
    async def delete_wallet(self, info: Info, wallet_id: str) -> DeleteWalletResponse:
        """Removes a wallet from walletd.

        Note: Addresses that were previously added will continue to be tracked
        even if they are no longer connected to any wallets.
        """
        try:
            await WalletdBaseResolver.handle_api_call(info, "delete_wallet", wallet_id=wallet_id)
            return DeleteWalletResponse(success=True)
        except Exception as e:
            return DeleteWalletResponse(success=False, message=str(e))

    @strawberry.mutation
    async def delete_wallet_address(self, info: Info, wallet_id: str, address: str) -> DeleteWalletAddressResponse:
        """Removes an address from a wallet.

        This will disassociate any events or UTXOs not referencing another address.
        The address will continue to be tracked even if not registered to another wallet.
        """
        try:
            await WalletdBaseResolver.handle_api_call(
                info, "delete_wallet_address", wallet_id=wallet_id, address=address
            )
            return DeleteWalletAddressResponse(success=True)
        except Exception as e:
            return DeleteWalletAddressResponse(success=False, message=str(e))

    @strawberry.mutation
    async def add_wallet(self, info: Info, input: AddWalletInput) -> Wallet:
        """Adds a new wallet with optional metadata"""
        data = await WalletdBaseResolver.handle_api_call(
            info, "add_wallet", name=input.name, description=input.description, metadata=input.metadata
        )

        return Wallet(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            date_created=datetime.fromisoformat(data["dateCreated"].replace("Z", "+00:00")),
            last_updated=datetime.fromisoformat(data["lastUpdated"].replace("Z", "+00:00")),
            metadata=data.get("metadata"),
        )

    @strawberry.mutation
    async def add_wallet_address(
        self, info: Info, wallet_id: str, input: AddWalletAddressInput
    ) -> AddWalletAddressResponse:
        """Adds an address for the wallet to watch.

        Note: After registering one or more addresses, the blockchain may need
        to be rescanned using the subscribe endpoint.
        """
        try:
            await WalletdBaseResolver.handle_api_call(
                info,
                "add_wallet_address",
                wallet_id=wallet_id,
                address=input.address,
                description=input.description,
                spend_policy=input.spend_policy,
                metadata=input.metadata,
            )
            return AddWalletAddressResponse(success=True)
        except Exception as e:
            return AddWalletAddressResponse(success=False, message=str(e))

    @strawberry.mutation
    async def construct_transaction(
        self,
        info: Info,
        wallet_id: str,
        siacoins: Optional[List[SiacoinRecipientInput]] = None,
        siafunds: Optional[List[SiafundRecipientInput]] = None,
        change_address: str = strawberry.field(name="changeAddress"),
    ) -> ConstructedTransaction:
        """Constructs a transaction sending siacoins and siafunds to the recipients"""
        payload = {
            "siacoins": [{"address": sc.address, "value": sc.value} for sc in (siacoins or [])],
            "siafunds": [{"address": sf.address, "value": sf.value} for sf in (siafunds or [])],
            "changeAddress": change_address,
        }

        data = await WalletdBaseResolver.handle_api_call(info, "construct_transaction", wallet_id=wallet_id, **payload)

        return ConstructedTransaction(
            basis=TransactionBasis(height=data["basis"]["height"], id=data["basis"]["id"]),
            id=data["id"],
            transaction=data["transaction"],
            estimated_fee=data["estimatedFee"],
        )

    @strawberry.mutation
    async def construct_v2_transaction(
        self,
        info: Info,
        wallet_id: str,
        siacoins: Optional[List[SiacoinRecipientInput]] = None,
        siafunds: Optional[List[SiafundRecipientInput]] = None,
        change_address: str = strawberry.field(name="changeAddress"),
    ) -> ConstructedTransaction:
        """Constructs a V2 transaction sending siacoins and siafunds to the recipients"""
        payload = {
            "siacoins": [{"address": sc.address, "value": sc.value} for sc in (siacoins or [])],
            "siafunds": [{"address": sf.address, "value": sf.value} for sf in (siafunds or [])],
            "changeAddress": change_address,
        }

        data = await WalletdBaseResolver.handle_api_call(
            info, "construct_v2_transaction", wallet_id=wallet_id, **payload
        )

        return ConstructedTransaction(
            basis=TransactionBasis(height=data["basis"]["height"], id=data["basis"]["id"]),
            id=data["id"],
            transaction=data["transaction"],
            estimated_fee=data["estimatedFee"],
        )

    @strawberry.mutation
    async def fund_transaction(
        self,
        info: Info,
        wallet_id: str,
        transaction: TransactionInput,
        amount: str,
        change_address: str = strawberry.field(name="changeAddress"),
    ) -> FundTransactionResponse:
        """Funds a transaction using UTXOs from the wallet.

        The UTXOs are locked for future use. If the transaction is not going to be broadcast,
        call the release endpoint to free the UTXOs. Signatures must be added externally
        in order to broadcast the transaction.

        Args:
            wallet_id: ID of the wallet to use for funding
            transaction: The transaction to fund
            amount: Total amount needed for the transaction (including fees)
            change_address: Address to send any remaining funds to
        """
        # Convert input types to dict for API
        transaction_dict = {
            "siacoinOutputs": [
                {"value": output.value, "address": output.address} for output in transaction.siacoin_outputs
            ],
            "minerFees": transaction.miner_fees,
        }

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "fund_transaction",
            wallet_id=wallet_id,
            transaction=transaction_dict,
            amount=amount,
            change_address=change_address,
        )

        # Convert API response to GraphQL types
        tx = data["transaction"]
        siacoin_inputs = None
        if "siacoinInputs" in tx:
            siacoin_inputs = [
                SiacoinInput(
                    parent_id=input["parentID"],
                    unlock_conditions=UnlockConditions(
                        timelock=input["unlockConditions"]["timelock"],
                        public_keys=input["unlockConditions"].get("publicKeys"),
                        signatures_required=input["unlockConditions"]["signaturesRequired"],
                    ),
                )
                for input in tx["siacoinInputs"]
            ]

        return FundTransactionResponse(
            transaction=Transaction(
                siacoin_inputs=siacoin_inputs,
                siacoin_outputs=[
                    SiacoinOutput(value=output["value"], address=output["address"]) for output in tx["siacoinOutputs"]
                ],
                miner_fees=tx["minerFees"],
            ),
            to_sign=data["toSign"],
            depends_on=data.get("dependsOn"),
        )

    @strawberry.mutation
    async def reserve_utxos(
        self,
        info: Info,
        wallet_id: str,
        siacoin_outputs: List[str] = strawberry.field(name="siacoinOutputs"),
        siafund_outputs: List[str] = strawberry.field(name="siafundOutputs", default_factory=list),
        duration: Optional[int] = None,
    ) -> ReserveUTXOsResponse:
        """Reserves UTXOs preventing them from being used by the fund endpoint.

        To unlock the UTXOs and allow other transactions to use them, call the release endpoint.
        Duration is the time to lock the UTXOs in nanoseconds. If duration is zero or None,
        the outputs will be locked for 10 minutes.

        Args:
            wallet_id: ID of the wallet
            siacoin_outputs: List of siacoin output IDs to reserve
            siafund_outputs: List of siafund output IDs to reserve (optional)
            duration: Time to lock the UTXOs in nanoseconds. If None or 0, defaults to 10 minutes
        """
        try:
            await WalletdBaseResolver.handle_api_call(
                info,
                "reserve_utxos",
                wallet_id=wallet_id,
                siacoin_outputs=siacoin_outputs,
                siafund_outputs=siafund_outputs,
                duration=duration,
            )
            return ReserveUTXOsResponse(success=True)
        except Exception as e:
            return ReserveUTXOsResponse(success=False, message=str(e))

    @strawberry.mutation
    async def release_utxos(
        self,
        info: Info,
        wallet_id: str,
        siacoin_outputs: List[str] = strawberry.field(name="siacoinOutputs"),
        siafund_outputs: List[str] = strawberry.field(name="siafundOutputs", default_factory=list),
    ) -> ReleaseUTXOsResponse:
        """Release unlocks UTXOs so they can be used to fund transactions.

        This endpoint unlocks previously reserved UTXOs, making them available
        for use with the fund endpoint.

        Args:
            wallet_id: ID of the wallet
            siacoin_outputs: List of siacoin output IDs to release
            siafund_outputs: List of siafund output IDs to release (optional)
        """
        try:
            await WalletdBaseResolver.handle_api_call(
                info,
                "release_utxos",
                wallet_id=wallet_id,
                siacoin_outputs=siacoin_outputs,
                siafund_outputs=siafund_outputs,
            )
            return ReleaseUTXOsResponse(success=True)
        except Exception as e:
            return ReleaseUTXOsResponse(success=False, message=str(e))