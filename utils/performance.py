"""
Search result tracking
"""

import time
from dataclasses import dataclass
from typing import List

@dataclass
class SearchResult:
    """Stores results from search algorithms"""
    path: List[str]  # Path from start to goal
    cost: float      # Total distance
    nodes_expanded: int  # How many nodes checked
    runtime: float   # Time taken in seconds

def time_function(func):
    """Timer decorator for functions"""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper
