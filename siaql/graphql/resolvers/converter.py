# siaql/graphql/resolvers/walletd.py
import enum
import inspect
import logging
from dataclasses import fields
from datetime import datetime
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

import strawberry
from strawberry.exceptions import MissingTypesForGenericError
from strawberry.types import Info
from strawberry.types.base import StrawberryList, StrawberryOptional, StrawberryType
from strawberry.types.enum import EnumDefinition as StrawberryEnum
from strawberry.types.lazy_type import LazyType
from strawberry.types.scalar import ScalarDefinition, ScalarWrapper
from strawberry.types.union import StrawberryUnion
from dateutil import parser


logger = logging.getLogger("siaql.resolvers.converter")


class TypeConverter:
    @staticmethod
    def parse_datetime(value: str) -> datetime:
        """
        Parse datetime strings with various formats.
        Uses python-dateutil for maximum compatibility.
        """
        if not isinstance(value, str):
            raise ValueError(f"Expected string for datetime parsing, got {type(value)}")

        try:
            # First try direct fromisoformat
            return datetime.fromisoformat(value)
        except ValueError:
            try:
                # If that fails, try with dateutil parser
                return parser.parse(value)
            except (ValueError, TypeError) as e:
                # If all parsing attempts fail
                raise ValueError(f"Unable to parse datetime string: {value}")

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
        elif hasattr(type_obj, "of_type"):
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
        elif hasattr(type_obj, "of_type") and not isinstance(type_obj, StrawberryOptional):
            return cls.get_wrapped_type(type_obj.of_type)
        return type_obj

    @classmethod
    def convert_value(cls, value: Any, target_type: Type) -> Any:
        """Convert a value to the target type, handling nested structures"""
        if value is None:
            return None

        if isinstance(target_type, StrawberryOptional):
            return cls.convert_value(value, target_type.of_type)  # Unwrap optional

        # Handle StrawberryList
        if isinstance(target_type, StrawberryList):
            if value is None:
                return None

            if not isinstance(value, (list, tuple)):
                return None
            # Convert each item in the list using the list's element type
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
            inspect.isclass(base_type) and issubclass(base_type, enum.Enum)
        ):
            if isinstance(value, str):
                try:
                    return base_type[value.upper()]
                except KeyError:
                    # Try by value if name lookup fails
                    return next((member for member in base_type if member.value == value), value)
            if isinstance(value, (int, float)):
                try:
                    return base_type(value)
                except ValueError:
                    return value
            return value

        # Handle Strawberry Scalars
        if isinstance(wrapped_type, ScalarWrapper):
            if hasattr(wrapped_type, "parse_value"):
                return wrapped_type.parse_value(value)
            return base_type(value)

        # Handle SiaType subclasses and other Strawberry types
        if isinstance(value, dict) and (
            hasattr(base_type, "__strawberry_definition__")
            or (inspect.isclass(base_type) and issubclass(base_type, strawberry.type))
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
                    return cls.parse_datetime(value)
                elif issubclass(base_type, enum.Enum):
                    if isinstance(value, str):
                        try:
                            return base_type[value.upper()]
                        except KeyError:
                            return next((member for member in base_type if member.value == value), value)
                    return base_type(value)
            except TypeError:
                pass

        return value

    @classmethod
    def get_all_fields(cls, target_type: Type) -> Dict[str, Any]:
        """Get all fields including inherited ones"""
        all_fields = {}

        # Get fields from base classes
        for base in getattr(target_type, "__mro__", [])[1:]:
            if hasattr(base, "__annotations__"):
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
        python_name = field.python_name if hasattr(field, "python_name") else field.name
        json_name = field.graphql_name if hasattr(field, "graphql_name") else field.name
        return python_name, json_name

    @classmethod
    def convert_to_strawberry_type(cls, data: Dict[str, Any], target_type: Type) -> Any:
        """Convert a dictionary to a Strawberry type, handling nested fields"""
        if not isinstance(data, dict):
            return data

        if isinstance(target_type, ScalarWrapper):
            return target_type.parse_value(data)

        field_mappings = {}  # JSON name -> (Python name, field)
        all_fields = cls.get_all_fields(target_type)

        for field in all_fields.values():
            python_name, json_name = cls.get_field_name_mapping(field)
            field_mappings[json_name] = (python_name, field)
            if python_name != json_name:
                field_mappings[python_name] = (python_name, field)

        result = {}

        for key, value in data.items():
            if key in field_mappings:
                python_name, field = field_mappings[key]
                field_type = field.type if hasattr(field, "type") else field
                try:
                    converted_value = cls.convert_value(value, field_type)
                    result[python_name] = converted_value
                except Exception as e:
                    logger.error("Error converting field %s: %s", key, str(e))
                    result[python_name] = None
            else:
                logger.warning("No mapping found for %s", key)

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
            is_optional = isinstance(field_type, StrawberryOptional) or (
                get_origin(field_type) is Union and type(None) in get_args(field_type)
            )

            # Always use python_name for the initialization
            result[python_name] = None if is_optional else getattr(field, "default", None)

        return result

    @classmethod
    def convert(cls, value: Any, target_type: Type) -> Any:
        """Main entry point for type conversion"""
        return cls.convert_value(value, target_type)
