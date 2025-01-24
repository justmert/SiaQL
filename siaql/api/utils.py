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


def handle_api_errors(error_class: Type[Exception] = APIError):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            # Get operation name from function name
            # Get the qualname (includes class name if it's a method)
            if args and hasattr(args[0], "__class__"):
                # If it's a method, get the class name
                class_name = args[0].__class__.__name__.lower()
                operation_name = f"{class_name}::{func.__name__}"

            try:
                return await func(*args, **kwargs)
            except httpx.HTTPError as e:
                cleaned_message = re.sub(r"For more information.*", "", str(e), flags=re.DOTALL)
                newline_removed = re.sub(r"\n", "", cleaned_message, flags=re.DOTALL)
                raise error_class(f"Failed to {operation_name}: {newline_removed}") from e
            except Exception as e:
                # Don't wrap our own error class
                if isinstance(e, error_class):
                    raise
                raise error_class(f"Unexpected error while trying to {operation_name}: {str(e)}") from e

        return wrapper

    return decorator
