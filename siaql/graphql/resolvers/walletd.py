# siaql/graphql/resolvers/walletd.py
from dataclasses import fields
from typing import Any, Dict, Optional, TypeVar, Callable, get_origin, get_args
from strawberry.types import Info
from typing import Any, Dict, Optional, TypeVar, Callable, Type, get_type_hints, List
from strawberry.types import Info
import inspect
from functools import wraps
from strawberry.type import StrawberryList
from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin
from dataclasses import fields
import strawberry
from strawberry.type import StrawberryType, StrawberryList, StrawberryOptional
from strawberry.custom_scalar import ScalarWrapper

from datetime import datetime

T = TypeVar('T')

class DictFieldResolver:
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getattr__(self, name: str) -> Any:
        # Get the original field name from the class definition
        cls = type(self)
        if hasattr(cls, name):
            field = getattr(cls, name)
            if hasattr(field, 'graphql_name'):
                original_name = field.graphql_name
                if original_name in self._data:
                    return self._data[original_name]
        
        # Fallback to direct lookup
        if name in self._data:
            return self._data[name]
            
        return None

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

class TypeConverter:
    @classmethod
    def get_base_type(cls, type_obj: Any) -> Type:
        """Extract the base type from Strawberry type wrappers"""
        if isinstance(type_obj, StrawberryOptional):
            return cls.get_base_type(type_obj.of_type)
        elif isinstance(type_obj, StrawberryList):
            return cls.get_base_type(type_obj.of_type)
        elif isinstance(type_obj, ScalarWrapper):
            return type_obj.wrap
        elif hasattr(type_obj, 'of_type'):
            return cls.get_base_type(type_obj.of_type)
        return type_obj

    @classmethod
    def get_wrapped_type(cls, type_obj: Any) -> Type:
        """Get the wrapped type without unwrapping Optional"""
        if isinstance(type_obj, StrawberryList):
            return cls.get_wrapped_type(type_obj.of_type)
        elif isinstance(type_obj, ScalarWrapper):
            return type_obj
        elif hasattr(type_obj, 'of_type') and not isinstance(type_obj, StrawberryOptional):
            return cls.get_wrapped_type(type_obj.of_type)
        return type_obj

    @classmethod
    def convert_value(cls, value: Any, target_type: Type) -> Any:
        """Convert a value to the target type, handling nested structures"""
        if value is None:
            return None

        # Handle StrawberryList
        if isinstance(target_type, StrawberryList):
            if not isinstance(value, list):
                return None
            return [cls.convert_value(item, target_type.of_type) for item in value]

        # Get the wrapped type (preserving Optional wrapper)
        wrapped_type = cls.get_wrapped_type(target_type)
        # Get the actual base type (removing all wrappers)
        base_type = cls.get_base_type(target_type)

        # Handle Strawberry Scalars
        if isinstance(wrapped_type, ScalarWrapper):
            if hasattr(wrapped_type, 'parse_value'):
                return wrapped_type.parse_value(value)
            return base_type(value)

        # Handle SiaType subclasses and other Strawberry types
        if isinstance(value, dict) and (hasattr(base_type, '__strawberry_definition__') or 
                                      (inspect.isclass(base_type) and issubclass(base_type, strawberry.type))):
            converted = cls.convert_to_strawberry_type(value, base_type)
            # Create an instance if needed
            if inspect.isclass(base_type) and not isinstance(converted, base_type):
                # Get all required fields with their default values (None for Optional)
                required_fields = cls.get_required_fields(base_type)
                # Merge converted data with required fields
                print(f"converted: {converted}")
                all_fields = {**required_fields, **converted}
                return base_type(**all_fields)
            return converted

        # Handle basic types
        if isinstance(base_type, type):
            try:
                if issubclass(base_type, str):
                    return str(value)
                elif issubclass(base_type, (int, float)):
                    return base_type(value)
                elif issubclass(base_type, datetime) and isinstance(value, str):
                    return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except TypeError:
                pass

        return value

    @classmethod
    def convert_to_strawberry_type(cls, data: Dict[str, Any], target_type: Type) -> Any:
        """Convert a dictionary to a Strawberry type, handling nested fields"""
        if not isinstance(data, dict):
            return data

        if isinstance(target_type, ScalarWrapper):
            return target_type.parse_value(data)

        result = {}
        
        # Get field mappings both ways (JSON name -> field and field name -> field)
        field_mappings = {}
        try:
            for field in fields(target_type):
                # Get the JSON name from metadata
                json_name = field.metadata.get('strawberry', {}).get('name', field.name)
                # Map both the JSON name and Python name to the field
                field_mappings[json_name] = field
                field_mappings[field.name] = field
        except (TypeError, AttributeError):
            field_mappings = getattr(target_type, '__annotations__', {})

        # Process each field in the input data
        for key, value in data.items():
            field = field_mappings.get(key)
            if field is None:
                continue

            if hasattr(field, 'type'):
                # Use the Python name for storing in the result
                python_name = field.name
                field_type = field.type
            else:
                python_name = key
                field_type = field

            converted_value = cls.convert_value(value, field_type)
            result[python_name] = converted_value

        return result

    @classmethod
    def get_required_fields(cls, target_type: Type) -> Dict[str, Any]:
        """Get all fields of a type with None as default for Optional fields"""
        result = {}
        try:
            for field in fields(target_type):
                # Use Python name for the result dict
                python_name = field.name
                field_type = field.type
                
                # Check if field is Optional
                is_optional = (
                    isinstance(field_type, StrawberryOptional) or
                    (get_origin(field_type) is Union and type(None) in get_args(field_type))
                )
                result[python_name] = None if is_optional else field.default
        except TypeError:
            # If not a dataclass, try getting annotations
            for name, field_type in getattr(target_type, '__annotations__', {}).items():
                is_optional = (
                    isinstance(field_type, StrawberryOptional) or
                    (get_origin(field_type) is Union and type(None) in get_args(field_type))
                )
                result[name] = None if is_optional else getattr(target_type, name, None)
        
        return result

    @classmethod
    def convert(cls, value: Any, target_type: Type) -> Any:
        """Main entry point for type conversion"""
        return cls.convert_value(value, target_type)
