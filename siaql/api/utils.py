# siaql/api/utils.py
from typing import Dict, List, Optional, Any, Callable, TypeVar, Type
from functools import wraps
import re
import httpx
import inspect

T = TypeVar("T")


class APIError(Exception):
    """Base exception for API errors"""

    pass


def format_operation_name(func_name: str) -> str:
    """Convert function name to human readable operation name"""
    # Remove common prefixes like get_, post_, put_, etc.
    name = re.sub(r"^(get|post|put|delete|patch)_", "", func_name)
    # Split on underscores and convert to space-separated string
    name = " ".join(name.split("_"))
    return name


def handle_api_errors(error_class: Type[Exception] = APIError):
    """
    Decorator for handling API errors consistently.

    Args:
        error_class: The exception class to use for errors. Defaults to APIError.

    Usage:
        @handle_api_errors(MyCustomError)
        async def my_function():
            ...

        # Or use default APIError
        @handle_api_errors()
        async def another_function():
            ...
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            # Get operation name from function name
            operation_name = format_operation_name(func.__name__)

            # Get the qualname (includes class name if it's a method)
            if args and hasattr(args[0], "__class__"):
                # If it's a method, get the class name
                class_name = args[0].__class__.__name__.lower()
                operation_name = f"{class_name} {operation_name}"

            try:
                return await func(*args, **kwargs)
            except httpx.HTTPError as e:
                raise error_class(f"Failed to {operation_name}: HTTP error occurred - {str(e)}") from e
            except Exception as e:
                # Don't wrap our own error class
                if isinstance(e, error_class):
                    raise
                raise error_class(f"Unexpected error while trying to {operation_name}: {str(e)}") from e

        return wrapper

    return decorator
