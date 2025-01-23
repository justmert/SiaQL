# siaql/graphql/schemas/walletd/txpool.py
from typing import List, Optional, Dict, Any
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from strawberry.scalars import JSON
from siaql.graphql.schemas.types import Transaction, V2Transaction, ChainIndex, Currency, TxpoolTransactionsResponse


@strawberry.type
class TxpoolQueries:
    @strawberry.field
    async def txpool_parents(self, info: Info, transaction: Transaction) -> List[Transaction]:
        """Get parent transactions from pool"""
        return await self.handle_api_call(info, "get_txpool_parents", transaction=transaction)

    @strawberry.field
    async def txpool_transactions(self, info: Info) -> TxpoolTransactionsResponse:
        """Get all transactions in the transaction pool"""
        return await WalletdBaseResolver.handle_api_call(info, "get_txpool_transactions")

    @strawberry.field
    async def txpool_fee(self, info: Info) -> Currency:
        """Get the recommended transaction fee"""
        return await WalletdBaseResolver.handle_api_call(info, "get_txpool_fee")


@strawberry.type
class TxpoolMutations:
    @strawberry.mutation
    async def txpool_broadcast(self, info: Info, transactions: List[Transaction]) -> bool:
        """Broadcast transactions to network"""
        await self.handle_api_call(info, "post_txpool_broadcast", transactions=transactions)
        return True
