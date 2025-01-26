# siaql/graphql/schemas/walletd/txpool.py
from typing import List, Optional, Dict, Any
import strawberry
from strawberry.types import Info
from siaql.graphql.resolvers.walletd import WalletdBaseResolver
from strawberry.scalars import JSON
from siaql.graphql.schemas.types import (
    Transaction,
    TxpoolBroadcastRequest,
    V2Transaction,
    ChainIndex,
    Currency,
    TxpoolTransactionsResponse,
)
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput


@strawberry.type
class TxpoolQueries:
    @strawberry.field
    async def walletd_txpool_parents(
        self,
        info: Info,
        transaction: Transaction.Input,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> List[Transaction]:
        """Get parent transactions from pool"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_txpool_parents",
            transaction=transaction,
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def walletd_txpool_transactions(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> TxpoolTransactionsResponse:
        """Get all transactions in the transaction pool"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_txpool_transactions",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )

    @strawberry.field
    async def walletd_txpool_fee(
        self,
        info: Info,
        filter: Optional[FilterInput] = None,
        sort: Optional[SortInput] = None,
        pagination: Optional[PaginationInput] = None,
    ) -> Currency:
        """Get the recommended transaction fee"""
        return await WalletdBaseResolver.handle_api_call(
            info,
            "get_txpool_fee",
            filter_input=filter,
            sort_input=sort,
            pagination_input=pagination,
        )


@strawberry.type
class TxpoolMutations:
    @strawberry.mutation
    async def walletd_txpool_broadcast(self, info: Info, req: TxpoolBroadcastRequest.Input) -> bool:
        """Broadcast transactions to network"""
        await WalletdBaseResolver.handle_api_call(info, "txpool_broadcast", req=req)
        return True
