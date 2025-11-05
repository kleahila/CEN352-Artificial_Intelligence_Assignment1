"""
Search Algorithms Implementation

This module implements Uniform Cost Search (UCS) and A* Search algorithms
for the Electric Vehicle routing problem.
"""

import heapq
import time
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from graph.city_graph import CityGraph
from utils.performance import SearchResult

class SearchAlgorithm(ABC):
    """
    Abstract base class for search algorithms.
    """

    def __init__(self, graph: CityGraph, start: str, initial_battery: float):
        """
        Initialize the search algorithm.

        Args:
            graph: The city graph
            start: Starting node
            initial_battery: Initial battery capacity in km
        """
        self.graph = graph
        self.start = start
        self.initial_battery = initial_battery
        self.max_battery = initial_battery  # Battery resets to this value at each node

    @abstractmethod
    def search(self) -> SearchResult:
        """
        Perform the search and return the result.

        Returns:
            SearchResult containing path, cost, nodes expanded, and runtime
        """
        pass

    def _is_valid_move(self, current_battery: float, distance: float) -> bool:
        """
        Check if a move is valid given current battery and distance.

        Args:
            current_battery: Current battery level
            distance: Distance to travel

        Returns:
            True if the move is valid, False otherwise
        """
        return distance <= current_battery

    def _is_goal(self, node: str) -> bool:
        """
        Check if a node is a goal (charging station).

        Args:
            node: The node to check

        Returns:
            True if the node is a charging station, False otherwise
        """
        return self.graph.is_charging_station(node)

class UniformCostSearch(SearchAlgorithm):
    """
    Uniform Cost Search implementation for EV routing.
    Expands nodes in order of increasing path cost to find closest charging station.
    """

    def __init__(self, graph: CityGraph, start: str, initial_battery: float):
        """
        Initialize Uniform Cost Search.

        Args:
            graph: The city graph
            start: Starting node
            initial_battery: Initial battery capacity in km
        """
        super().__init__(graph, start, initial_battery)

    def search(self) -> SearchResult:
        """
        Perform Uniform Cost Search to find closest charging station.

        Returns:
            SearchResult with the optimal path and statistics
        """
        start_time = time.perf_counter()

        # Priority queue: (cost, node, battery, path)
        frontier = [(0, self.start, self.initial_battery, [self.start])]
        visited = set()  # (node, battery) states
        nodes_expanded = 0

        while frontier:
            cost, current, battery, path = heapq.heappop(frontier)
            nodes_expanded += 1

            # Check if goal reached (charging station)
            if self._is_goal(current):
                runtime = time.perf_counter() - start_time
                return SearchResult(path, cost, nodes_expanded, runtime)

            state = (current, battery)
            if state in visited:
                continue
            visited.add(state)

            # Explore neighbors
            for neighbor, distance in self.graph.neighbors(current):
                if self._is_valid_move(battery, distance):
                    new_cost = cost + distance
                    new_battery = self.max_battery  # Recharge at each node
                    new_path = path + [neighbor]
                    new_state = (neighbor, new_battery)

                    if new_state not in visited:
                        heapq.heappush(frontier, (new_cost, neighbor, new_battery, new_path))

        # No path found
        runtime = time.perf_counter() - start_time
        return SearchResult([], float('inf'), nodes_expanded, runtime)

class AStarSearch(SearchAlgorithm):
    """
    A* Search implementation for EV routing.
    Uses f(n) = g(n) + h(n) where h(n) is the distance to closest charging station.
    """

    def __init__(self, graph: CityGraph, start: str, initial_battery: float):
        """
        Initialize A* Search.

        Args:
            graph: The city graph
            start: Starting node
            initial_battery: Initial battery capacity in km
        """
        super().__init__(graph, start, initial_battery)

    def search(self) -> SearchResult:
        """
        Perform A* Search to find closest charging station.

        Returns:
            SearchResult with the optimal path and statistics
        """
        start_time = time.perf_counter()

        # Priority queue: (f_cost, g_cost, node, battery, path)
        frontier = [(0, 0, self.start, self.initial_battery, [self.start])]
        visited = set()  # (node, battery) states
        nodes_expanded = 0

        while frontier:
            f_cost, g_cost, current, battery, path = heapq.heappop(frontier)
            nodes_expanded += 1

            # Check if goal reached (charging station)
            if self._is_goal(current):
                runtime = time.perf_counter() - start_time
                return SearchResult(path, g_cost, nodes_expanded, runtime)

            state = (current, battery)
            if state in visited:
                continue
            visited.add(state)

            # Explore neighbors
            for neighbor, distance in self.graph.neighbors(current):
                if self._is_valid_move(battery, distance):
                    new_g_cost = g_cost + distance
                    heuristic = self.graph.get_closest_charging_station_heuristic(neighbor)
                    new_f_cost = new_g_cost + heuristic
                    new_battery = self.max_battery  # Recharge at each node
                    new_path = path + [neighbor]
                    new_state = (neighbor, new_battery)

                    if new_state not in visited:
                        heapq.heappush(frontier, (new_f_cost, new_g_cost, neighbor, new_battery, new_path))

        # No path found
        runtime = time.perf_counter() - start_time
        return SearchResult([], float('inf'), nodes_expanded, runtime)
