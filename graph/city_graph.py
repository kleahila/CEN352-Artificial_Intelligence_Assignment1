"""
City Graph Implementation

This module defines the CityGraph class that represents the synthetic city
with nodes, edges, and coordinates for the EV routing problem.
"""

import math
from typing import Dict, List, Tuple, Set

class CityGraph:
    """
    Represents the city graph with nodes, edges, and coordinates.

    Not all nodes are charging stations - only specific ones are.
    """

    def __init__(self):
        """Initialize the city graph with nodes, edges, coordinates, and charging stations."""
        # Graph edges: {node: [(neighbor, distance), ...]}
        self.graph: Dict[str, List[Tuple[str, float]]] = {
            'A': [('B', 3.6), ('C', 5.1)],
            'B': [('A', 3.6), ('C', 3.2), ('D', 4.2), ('F', 2.8)],
            'C': [('A', 5.1), ('B', 3.2), ('D', 4.6), ('E', 3.7), ('G', 4.1)],
            'D': [('B', 4.2), ('C', 4.6), ('E', 2.5), ('H', 3.9)],
            'E': [('C', 3.7), ('D', 2.5), ('I', 4.3)],
            'F': [('B', 2.8), ('G', 3.5), ('J', 4.7)],
            'G': [('C', 4.1), ('F', 3.5), ('H', 2.9), ('K', 3.8)],
            'H': [('D', 3.9), ('G', 2.9), ('I', 3.2)],
            'I': [('E', 4.3), ('H', 3.2), ('J', 2.6)],
            'J': [('F', 4.7), ('I', 2.6), ('K', 3.4)],
            'K': [('G', 3.8), ('J', 3.4)]
        }

        # Node coordinates for visualization and heuristic calculation
        self.coords: Dict[str, Tuple[float, float]] = {
            'A': (0, 0),
            'B': (3.6, 0),
            'C': (5, 3),
            'D': (8.5, 2.5),
            'E': (10, 5),
            'F': (2, -3),
            'G': (7, 0),
            'H': (11, 1),
            'I': (13, 4),
            'J': (5, -5),
            'K': (10, -2)
        }

        # Charging stations - only some nodes have them
        self.charging_stations: Set[str] = {'C', 'E', 'G', 'I', 'K'}

    def neighbors(self, node: str) -> List[Tuple[str, float]]:
        """
        Get the neighbors of a node with their distances.

        Args:
            node: The node to get neighbors for

        Returns:
            List of (neighbor, distance) tuples
        """
        return self.graph.get(node, [])

    def heuristic(self, node: str, goal: str) -> float:
        """
        Calculate the Euclidean distance heuristic from node to goal.

        Args:
            node: Current node
            goal: Goal node

        Returns:
            Euclidean distance between the nodes
        """
        x1, y1 = self.coords[node]
        x2, y2 = self.coords[goal]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def is_charging_station(self, node: str) -> bool:
        """
        Check if a node is a charging station.

        Args:
            node: The node to check

        Returns:
            True if the node is a charging station, False otherwise
        """
        return node in self.charging_stations

    def get_closest_charging_station_heuristic(self, node: str) -> float:
        """
        Calculate heuristic to closest charging station (minimum Euclidean distance).

        Args:
            node: Current node

        Returns:
            Minimum Euclidean distance to any charging station
        """
        if self.is_charging_station(node):
            return 0.0

        min_distance = float('inf')
        for station in self.charging_stations:
            distance = self.heuristic(node, station)
            min_distance = min(min_distance, distance)
        return min_distance
