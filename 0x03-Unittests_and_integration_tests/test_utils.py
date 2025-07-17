#!/usr/bin/env python3
"""
A module with utility functions.
"""
import requests
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


def get_json(url: str) -> Mapping:
    """
    Performs a GET request to a URL and returns the JSON response.

    Args:
        url (str): The URL to send the request to.

    Returns:
        Mapping: The JSON payload of the response as a dictionary.
    """
    response = requests.get(url)
    return response.json()

