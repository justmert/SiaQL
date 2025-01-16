# siaql/graphql/schemas/walletd/txpool.py
from typing import List, Optional, Dict, Any
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from strawberry.scalars import JSON

from siaql.graphql.schemas.types import (
    Transaction,
    TransactionInput,
    TransactionSignature,
    SiacoinInput,
    UnlockConditions,
    SiacoinOutput,
    Signature,
    CoveredFields,
    BroadcastResponse
)

@strawberry.type
class TransactionPoolQueries(WalletdBaseResolver):
    @strawberry.field
    async def transactions(self, info: Info) -> List[Transaction]:
        """Returns all transactions in the pool"""
        def transform_transactions(data: dict) -> List[Transaction]:
            transactions = []
            for tx in data.get("transactions", []):
                transactions.append(Transaction(
                    siacoin_inputs=[
                        SiacoinInput(
                            parent_id=input["parentID"],
                            unlock_conditions=UnlockConditions(
                                timelock=input["unlockConditions"]["timelock"],
                                public_keys=input["unlockConditions"]["publicKeys"],
                                signatures_required=input["unlockConditions"]["signaturesRequired"]
                            )
                        ) for input in tx.get("siacoinInputs", [])
                    ],
                    siacoin_outputs=[
                        SiacoinOutput(
                            value=output["value"],
                            address=output["address"]
                        ) for output in tx.get("siacoinOutputs", [])
                    ],
                    miner_fees=tx.get("minerFees", []),
                    signatures=[
                        Signature(
                            parent_id=sig["parentID"],
                            public_key_index=sig["publicKeyIndex"],
                            covered_fields=CoveredFields(
                                whole_transaction=sig["coveredFields"]["wholeTransaction"]
                            ),
                            signature=sig["signature"]
                        ) for sig in tx.get("signatures", [])
                    ]
                ))
            return transactions

        data = await WalletdBaseResolver.handle_api_call(
            info,
            "get_txpool_transactions",
            transform_func=transform_transactions
        )
        return data

    @strawberry.field
    async def fee(self, info: Info) -> str:
        """Returns the current transaction fee per byte"""
        return await WalletdBaseResolver.handle_api_call(info, "get_txpool_fee")

@strawberry.type
class TransactionPoolMutations(WalletdBaseResolver):
    @strawberry.field
    async def broadcast_transaction_set(
        self, 
        info: Info,
        transactions: Optional[List[TransactionInput]] = None,
        v2transactions: Optional[List[TransactionInput]] = None
    ) -> BroadcastResponse:
        """Broadcast a set of transactions to the network"""
        try:
            tx_data = [tx.raw_data for tx in (transactions or [])]
            v2tx_data = [tx.raw_data for tx in (v2transactions or [])]
            
            await WalletdBaseResolver.handle_api_call(
                info,
                "broadcast_transaction_set",
                transactions=tx_data,
                v2transactions=v2tx_data
            )
            return BroadcastResponse(success=True)
        except Exception as e:
            return BroadcastResponse(success=False, message=str(e))