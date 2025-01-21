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
        elif isinstance(type_obj, LazyType):
            return cls.get_base_type(type_obj.resolve_type())
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
        elif isinstance(type_obj, LazyType):
            return cls.get_wrapped_type(type_obj.resolve_type())
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

        # Handle LazyType
        if isinstance(target_type, LazyType):
            return cls.convert_value(value, target_type.resolve_type())

        # Get the wrapped type (preserving Optional wrapper)
        wrapped_type = cls.get_wrapped_type(target_type)
        # Get the actual base type (removing all wrappers)
        base_type = cls.get_base_type(target_type)

        # Handle Union types
        if get_origin(base_type) is Union:
            possible_types = [t for t in get_args(base_type) if t is not type(None)]
            # Try each possible type until one works
            for possible_type in possible_types:
                try:
                    return cls.convert_value(value, possible_type)
                except (ValueError, TypeError):
                    continue
            return value

        # Handle Strawberry Enums
        if isinstance(wrapped_type, StrawberryEnum) or (
            inspect.isclass(base_type) and issubclass(base_type, enum.Enum)):
            if isinstance(value, str):
                try:
                    return base_type[value.upper()]
                except KeyError:
                    # Try by value if name lookup fails
                    return next(
                        (member for member in base_type 
                         if member.value == value),
                        value
                    )
            if isinstance(value, (int, float)):
                try:
                    return base_type(value)
                except ValueError:
                    return value
            return value

        # Handle Strawberry Scalars
        if isinstance(wrapped_type, ScalarWrapper):
            if hasattr(wrapped_type, 'parse_value'):
                return wrapped_type.parse_value(value)
            return base_type(value)

        # Handle SiaType subclasses and other Strawberry types
        if isinstance(value, dict) and (
            hasattr(base_type, '__strawberry_definition__') or 
            (inspect.isclass(base_type) and issubclass(base_type, strawberry.type))
        ):
            converted = cls.convert_to_strawberry_type(value, base_type)
            # Create an instance if needed
            if inspect.isclass(base_type) and not isinstance(converted, base_type):
                # Get all required fields with their default values
                required_fields = cls.get_required_fields(base_type)
                # Merge converted data with required fields
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
                elif issubclass(base_type, enum.Enum):
                    if isinstance(value, str):
                        try:
                            return base_type[value.upper()]
                        except KeyError:
                            return next(
                                (member for member in base_type 
                                 if member.value == value),
                                value
                            )
                    return base_type(value)
            except TypeError:
                pass

        return value

    @classmethod
    def get_all_fields(cls, target_type: Type) -> Dict[str, Any]:
        """Get all fields including inherited ones"""
        all_fields = {}
        
        # Get fields from base classes
        for base in getattr(target_type, '__mro__', [])[1:]:
            if hasattr(base, '__annotations__'):
                try:
                    for field in fields(base):
                        all_fields[field.name] = field
                except TypeError:
                    continue

        # Get fields from the class itself
        try:
            for field in fields(target_type):
                all_fields[field.name] = field
        except TypeError:
            pass

        return all_fields

    @classmethod
    def get_field_name_mapping(cls, field: Any) -> tuple[str, str]:
        """Get both Python name and JSON name for a field"""
        python_name = field.python_name if hasattr(field, 'python_name') else field.name
        json_name = field.graphql_name if hasattr(field, 'graphql_name') else field.name
        return python_name, json_name


    @classmethod
    def convert_to_strawberry_type(cls, data: Dict[str, Any], target_type: Type) -> Any:
        """Convert a dictionary to a Strawberry type, handling nested fields"""
        if not isinstance(data, dict):
            return data

        if isinstance(target_type, ScalarWrapper):
            return target_type.parse_value(data)

        # Get field mappings including inherited fields
        field_mappings = {}  # JSON name -> (Python name, field)
        all_fields = cls.get_all_fields(target_type)
        
        # Build field mappings
        for field in all_fields.values():
            python_name, json_name = cls.get_field_name_mapping(field)
            field_mappings[json_name] = (python_name, field)
            
            # Also map the Python name if different
            if python_name != json_name:
                field_mappings[python_name] = (python_name, field)
        
        result = {}
        
        # Process each field in the input data
        for key, value in data.items():
            if key in field_mappings:
                python_name, field = field_mappings[key]
                field_type = field.type if hasattr(field, 'type') else field
                converted_value = cls.convert_value(value, field_type)
                result[python_name] = converted_value
            else:
                print(f"No mapping found for {key}. Available mappings: {list(field_mappings.keys())}")

        return result

    @classmethod
    def get_required_fields(cls, target_type: Type) -> Dict[str, Any]:
        """Get all fields of a type with None as default for Optional fields"""
        result = {}
        all_fields = cls.get_all_fields(target_type)
        
        for field in all_fields.values():
            python_name, _ = cls.get_field_name_mapping(field)
            field_type = field.type
            
            # Check if field is Optional
            is_optional = (
                isinstance(field_type, StrawberryOptional) or
                (get_origin(field_type) is Union and type(None) in get_args(field_type))
            )
            
            # Always use python_name for the initialization
            result[python_name] = None if is_optional else getattr(field, 'default', None)
        
        return result

    @classmethod
    def convert(cls, value: Any, target_type: Type) -> Any:
        """Main entry point for type conversion"""
        return cls.convert_value(value, target_type)
