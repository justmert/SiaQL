from typing import Any, Callable, Dict, Optional, TypeVar
from strawberry.types import Info
from siaql.graphql.resolvers.converter import TypeConverter

T = TypeVar('T')

class RenterdBaseResolver:
    """Base resolver class for Renterd API"""
        
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

            if hasattr(info, '_field'):
                field_type = info._field.type
                return TypeConverter.convert(result, field_type)

            return result
        except Exception as e:
            print(f"Error in handle_api_call: {e}")
            raise e