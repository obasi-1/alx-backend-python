#!/usr/bin/env python3
"""
A module with a utility function for accessing nested maps.
"""
from typing import Mapping, Sequence, Any, TypeVar

T = TypeVar('T')


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access a value in a nested map using a sequence of keys.

    Args:
        nested_map (Mapping): The nested dictionary to access.
        path (Sequence): A sequence of keys representing the path to the value.

    Returns:
        Any: The value at the specified path within the nested map.

    Example:
        >>> nested_map = {"a": {"b": {"c": 1}}}
        >>> access_nested_map(nested_map, ["a", "b", "c"])
        1
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map

