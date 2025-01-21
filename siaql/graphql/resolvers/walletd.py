# siaql/graphql/resolvers/walletd.py
from dataclasses import fields
from typing import Any, Dict, Optional, TypeVar, Callable, get_origin, get_args
from strawberry.types import Info
from typing import Any, Dict, Optional, TypeVar, Callable, Type, get_type_hints, List
from strawberry.types import Info
import inspect
from functools import wraps
# from strawberry.types import StrawberryList
from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin
from dataclasses import fields
import strawberry
from strawberry.types.base import StrawberryList, StrawberryType, StrawberryOptional
from strawberry.types.scalar import ScalarWrapper, ScalarDefinition
from strawberry.types.enum import EnumDefinition as StrawberryEnum
from strawberry.types.union import StrawberryUnion

from strawberry.types.lazy_type import LazyType
from strawberry.exceptions import MissingTypesForGenericError
from siaql.graphql.resolvers.converter import TypeConverter

# from strawberry.types
# from strawberry.types import StrawberryType, StrawberryList, StrawberryOptional
# from strawberry.types.custom_scalar import ScalarWrapper
# from strawberry.types.enum import StrawberryEnum
from datetime import datetime
# from strawberry.lazy_type import LazyType

import inspect
import enum

from datetime import datetime
T = TypeVar('T')

class WalletdBaseResolver:
    """Base resolver class for Walletd API"""
        
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
        client = info.context["walletd_client"]
        method_func = getattr(client, method)
        try:
            result = await method_func(*args, **kwargs)
            
            if transform_func:
                return transform_func(result)

            if hasattr(info, '_field'):
                field_type = info._field.type
                # Use the TypeConverter directly
                return TypeConverter.convert(result, field_type)

            return result
        except Exception as e:
            print(f"Error in handle_api_call: {e}")
            raise e


