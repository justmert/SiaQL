# siaql/graphql/filtering.py

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar, Union

import strawberry
from dateutil import parser
from strawberry.scalars import JSON


@strawberry.enum
class FilterOperator(Enum):
    """Supported filter operations"""

    EQ = "eq"  # Equal to
    NEQ = "neq"  # Not equal to
    GT = "gt"  # Greater than
    LT = "lt"  # Less than
    GTE = "gte"  # Greater than or equal to
    LTE = "lte"  # Less than or equal to
    CONTAINS = "contains"  # String contains
    IN = "in"  # Value in list
    NIN = "nin"  # Value not in list
    EXISTS = "exists"  # Field exists


@strawberry.enum
class SortDirection(Enum):
    """Sort direction options"""

    ASC = "asc"
    DESC = "desc"


@strawberry.scalar
class FilterValue:
    """Custom scalar for filter values"""

    @staticmethod
    def serialize(value: Any) -> str:
        if value is None:
            return None
        return str(value)

    @staticmethod
    def parse_value(value: Any) -> Any:
        return value


@strawberry.input
class FilterInput:
    """Filter input type"""

    field: str
    operator: FilterOperator
    value: Optional[str] = 0


@strawberry.input
class SortInput:
    """Sort input type"""

    field: str
    direction: SortDirection = SortDirection.ASC


@strawberry.input
class PaginationInput:
    """Pagination input type"""

    offset: int = 0
    limit: int = 100


class QueryFiltering:
    @staticmethod
    def get_field_mapping(obj: Any) -> Dict[str, str]:
        """Get mapping of GraphQL names to Python names"""
        mapping = {}

        # Handle Strawberry types
        if hasattr(obj, "__strawberry_definition__"):
            for field in obj.__strawberry_definition__.fields:
                graphql_name = field.graphql_name or field.name
                python_name = field.python_name or field.name
                mapping[graphql_name] = python_name

        return mapping

    @staticmethod
    def get_field_value(obj: Any, field_path: str) -> Any:
        """Get nested field value using dot notation"""
        if not field_path or obj is None:
            return obj

        parts = field_path.split(".")
        current = obj

        for part in parts:
            if current is None:
                return None

            # Get field mapping for current object
            mapping = QueryFiltering.get_field_mapping(current)

            # Use mapped python name if available
            python_name = mapping.get(part, part)

            # Handle dictionary access
            if isinstance(current, dict):
                # Try original name first, then mapped name
                current = current.get(part, current.get(python_name))
            # Handle object attribute access
            elif hasattr(current, python_name):
                current = getattr(current, python_name)
            # If all else fails, try original name
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return None

        return current

    @classmethod
    def convert_value_for_comparison(cls, value: Any) -> Any:
        """Convert value to comparable type"""
        if value is None:
            return None

        # Try to convert to float if it's numeric
        try:
            return float(value)
        except (ValueError, TypeError):
            pass

        # Handle boolean values
        if isinstance(value, bool) or str(value).lower() in ("true", "false"):
            return str(value).lower() == "true"

        # Handle datetime strings
        try:
            parsed_date = parser.parse(str(value))
            return parsed_date.timestamp()
        except (ValueError, TypeError):
            pass

        # Default to string comparison
        return str(value).lower()

    @classmethod
    def compare_values(cls, field_value: Any, filter_value: Any, operator: FilterOperator) -> bool:
        """Compare values based on operator"""
        if operator == FilterOperator.EXISTS:
            exists_check = field_value is not None
            if filter_value is not None:
                return exists_check == (str(filter_value).lower() == "true")
            return exists_check

        if field_value is None:
            return False

        field_val = cls.convert_value_for_comparison(field_value)
        filter_val = cls.convert_value_for_comparison(filter_value)

        try:
            if operator == FilterOperator.EQ:
                return field_val == filter_val
            elif operator == FilterOperator.NEQ:
                return field_val != filter_val
            elif operator == FilterOperator.GT:
                return field_val > filter_val
            elif operator == FilterOperator.LT:
                return field_val < filter_val
            elif operator == FilterOperator.GTE:
                return field_val >= filter_val
            elif operator == FilterOperator.LTE:
                return field_val <= filter_val
            elif operator == FilterOperator.CONTAINS:
                return str(filter_val).lower() in str(field_val).lower()
            elif operator == FilterOperator.IN:
                if isinstance(filter_value, str):
                    values = [v.strip() for v in filter_value.split(",")]
                else:
                    values = [filter_value]
                return str(field_val).lower() in [str(v).lower() for v in values]
            elif operator == FilterOperator.NIN:
                if isinstance(filter_value, str):
                    values = [v.strip() for v in filter_value.split(",")]
                else:
                    values = [filter_value]
                return str(field_val).lower() not in [str(v).lower() for v in values]
        except (ValueError, TypeError):
            return False

        return False

    @classmethod
    def apply_filter(cls, items: List[Any], filter_input: Optional[FilterInput]) -> List[Any]:
        """Apply filter to list of items"""
        if not filter_input or not items:
            return items

        return [
            item
            for item in items
            if cls.compare_values(
                cls.get_field_value(item, filter_input.field), filter_input.value, filter_input.operator
            )
        ]

    @classmethod
    def apply_sort(cls, items: List[Any], sort_input: Optional[SortInput]) -> List[Any]:
        """Apply sorting to list of items"""
        if not sort_input or not items:
            return items

        def get_sort_key(item: Any) -> Any:
            value = cls.get_field_value(item, sort_input.field)
            if value is None:
                return (1, "") if sort_input.direction == SortDirection.ASC else (1, "zzz")

            converted_value = cls.convert_value_for_comparison(value)
            return (0, converted_value)

        reverse = sort_input.direction == SortDirection.DESC
        return sorted(items, key=get_sort_key, reverse=reverse)

    @staticmethod
    def apply_pagination(items: List[Any], pagination_input: Optional[PaginationInput]) -> List[Any]:
        """Apply pagination to list of items"""
        if not pagination_input or not items:
            return items

        start = max(0, pagination_input.offset)
        if pagination_input.limit is not None:
            end = start + pagination_input.limit
            return items[start:end]
        return items[start:]

    @classmethod
    def process_query(
        cls,
        items: List[Any],
        filter_input: Optional[FilterInput] = None,
        sort_input: Optional[SortInput] = None,
        pagination_input: Optional[PaginationInput] = None,
    ) -> List[Any]:
        """Process query with filtering, sorting, and pagination"""
        result = items

        # Apply operations in order
        if filter_input:
            result = cls.apply_filter(result, filter_input)
        if sort_input:
            result = cls.apply_sort(result, sort_input)
        if pagination_input:
            result = cls.apply_pagination(result, pagination_input)

        return result
