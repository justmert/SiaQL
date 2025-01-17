# siaql/graphql/resolvers/walletd.py
from typing import Any, Dict, Optional, TypeVar, Callable
from strawberry.types import Info

T = TypeVar('T')

class RenterdBaseResolver:
    """Base resolver class for Renterd API"""
    
    def __init__(self):
        """Initialize the resolver"""
        pass  # We could add shared initialization here if needed
        
    @classmethod
    async def handle_api_call(
        cls,
        info: Info, 
        method: str, 
        transform_func: Optional[Callable[[Dict], T]] = None,
        *args, 
        **kwargs
    ) -> Any:
        """Generic method to handle API calls with error handling"""
        client = info.context["renterd_client"]
        method_func = getattr(client, method)
        try:
            result = await method_func(*args, **kwargs)
            if transform_func:
                return transform_func(result)
            return result
        except Exception as e:
            # TODO: Add proper error handling/logging
            raise e