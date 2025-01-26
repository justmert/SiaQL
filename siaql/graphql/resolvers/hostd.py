from typing import Any, Callable, Dict, Optional, TypeVar
from strawberry.types import Info
from siaql.graphql.resolvers.converter import TypeConverter
from siaql.graphql.resolvers.filter import FilterInput, SortInput, PaginationInput, QueryFiltering
from functools import wraps
import logging

T = TypeVar("T")

logger = logging.getLogger("siaql.resolvers.hostd")


class HostdBaseResolver:
    """Base resolver class for Hostd API"""

    @classmethod
    async def handle_api_call(
        cls,
        info: Info,
        method: str,
        transform_func: Optional[Callable[[Dict], T]] = None,
        filter_input: Optional[FilterInput] = None,
        sort_input: Optional[SortInput] = None,
        pagination_input: Optional[PaginationInput] = None,
        *args,
        **kwargs,
    ) -> Any:
        """Generic method to handle API calls with error handling"""
        # Check if endpoint is skipped
        if info.context["skipped_endpoints"].get("hostd", False):
            raise Exception("Hostd endpoint was skipped during configuration. This query is not available.")

        client = info.context["hostd_client"]
        method_func = getattr(client, method)
        try:
            # 1. Get raw data from API
            result = await method_func(*args, **kwargs)
            logger.debug("Executing method: %s", method_func)

            # 2. Apply any custom transformations
            if transform_func:
                result = transform_func(result)

            # 3. Convert to proper GraphQL types if this is a typed field
            if hasattr(info, "_field"):
                field_type = info._field.type
                # Convert the entire result to proper GraphQL types
                result = TypeConverter.convert(result, field_type)

            # 4. Apply filtering, sorting, and pagination AFTER type conversion
            if isinstance(result, list):
                if filter_input:
                    # Now the data is in proper GraphQL types, making it easier to filter
                    result = QueryFiltering.apply_filter(result, filter_input)
                if sort_input:
                    result = QueryFiltering.apply_sort(result, sort_input)
                if pagination_input:
                    result = QueryFiltering.apply_pagination(result, pagination_input)

            return result
        except Exception as e:
            logger.error("Error in handle_api_call: %s", e)
            raise e
