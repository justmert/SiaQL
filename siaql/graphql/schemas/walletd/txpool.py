# siaql/graphql/schemas/walletd/txpool.py
from typing import List, Optional, Dict, Any
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from strawberry.scalars import JSON
from siaql.graphql.schemas.types import (
    Transaction, 
    V2Transaction, 
    ChainIndex, 
    Currency,
    TxpoolTransactionsResponse
)

@strawberry.type
class TxpoolQueries:
    @strawberry.field
    async def txpool_transactions(self, info: Info) -> TxpoolTransactionsResponse:
        """Get all transactions in the transaction pool"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_txpool_transactions"
        )

    @strawberry.field
    async def txpool_fee(self, info: Info) -> Currency:
        """Get the recommended transaction fee"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_txpool_fee"
        )

@strawberry.type
class TxpoolMutations:
    @strawberry.mutation
    async def txpool_broadcast(
        self,
        info: Info,
        basis: ChainIndex.Input,
        transactions: List[Transaction.Input],
        v2transactions: List[V2Transaction.Input]
    ) -> bool:
        """Broadcast transactions to the network"""
        await WalletdBaseResolver.handle_api_call(
            info,
            "post_txpool_broadcast",
            basis=basis,
            transactions=transactions,
            v2transactions=v2transactions
        )
        return True
