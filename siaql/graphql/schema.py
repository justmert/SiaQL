# siaql/siaql/graphql/schema.py
import strawberry
from strawberry.tools import merge_types
from typing import Optional
from .schemas.walletd import Query as WalletdQuery

# Merge all queries
@strawberry.type
class Query(WalletdQuery):
    @strawberry.field
    def hello(self) -> str:
        """Simple health check query"""
        return "Welcome to SiaQL!"

# Create the schema
schema = strawberry.Schema(
    query=Query,
    # We'll add mutations later
)