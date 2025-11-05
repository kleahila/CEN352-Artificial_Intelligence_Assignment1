"""
Performance Tracking Utilities

This module provides utilities for tracking search algorithm performance
and defines the SearchResult dataclass.
"""

import time
from dataclasses import dataclass
from typing import List

@dataclass
class SearchResult:
    """
    Data class to store search algorithm results.

    Attributes:
        path: List of nodes in the path from start to goal
        cost: Total cost of the path
        nodes_expanded: Number of nodes expanded during search
        runtime: Execution time in seconds
    """
    path: List[str]
    cost: float
    nodes_expanded: int
    runtime: float

def time_function(func):
    """
    Decorator to measure the execution time of a function.

    Args:
        func: The function to time

    Returns:
        The wrapped function that returns (result, execution_time)
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper
