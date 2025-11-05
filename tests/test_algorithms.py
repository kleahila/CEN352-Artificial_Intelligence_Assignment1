"""
Tests for the search algorithms
"""

import unittest
from graph.city_graph import CityGraph
from search.algorithms import UniformCostSearch, AStarSearch

class TestSearchAlgorithms(unittest.TestCase):
    """Test the search algorithms"""

    def setUp(self):
        """Setup for tests"""
        self.graph = CityGraph()
        self.start = 'A'

    def test_ucs_finds_path_normal_battery(self):
        """UCS should find path with normal battery"""
        battery = 6.0
        ucs = UniformCostSearch(self.graph, self.start, battery)
        result = ucs.search()

        self.assertIsNotNone(result.path)
        self.assertGreater(len(result.path), 1)
        self.assertEqual(result.path[0], self.start)
        self.assertTrue(self.graph.is_charging_station(result.path[-1]))
        self.assertGreater(result.cost, 0)
        self.assertGreater(result.nodes_expanded, 0)

    def test_astar_finds_path_normal_battery(self):
        """A* should find path with normal battery"""
        battery = 6.0
        astar = AStarSearch(self.graph, self.start, battery)
        result = astar.search()

        self.assertIsNotNone(result.path)
        self.assertGreater(len(result.path), 1)
        self.assertEqual(result.path[0], self.start)
        self.assertTrue(self.graph.is_charging_station(result.path[-1]))
        self.assertGreater(result.cost, 0)
        self.assertGreater(result.nodes_expanded, 0)

    def test_ucs_finds_path_high_battery(self):
        """UCS with high battery"""
        battery = 10.0
        ucs = UniformCostSearch(self.graph, self.start, battery)
        result = ucs.search()

        self.assertIsNotNone(result.path)
        self.assertTrue(self.graph.is_charging_station(result.path[-1]))
        self.assertLessEqual(result.cost, battery)  # Cost should not exceed battery

    def test_astar_finds_path_high_battery(self):
        """A* with high battery"""
        battery = 10.0
        astar = AStarSearch(self.graph, self.start, battery)
        result = astar.search()

        self.assertIsNotNone(result.path)
        self.assertTrue(self.graph.is_charging_station(result.path[-1]))
        self.assertLessEqual(result.cost, battery)

    def test_ucs_finds_path_low_battery(self):
        """UCS with low battery - longer path"""
        battery = 4.0
        ucs = UniformCostSearch(self.graph, self.start, battery)
        result = ucs.search()

        self.assertIsNotNone(result.path)
        self.assertTrue(self.graph.is_charging_station(result.path[-1]))
        # With low battery, might need to take longer path
        self.assertGreater(len(result.path), 2)  # Should be more than direct path

    def test_astar_finds_path_low_battery(self):
        """A* with low battery - longer path"""
        battery = 4.0
        astar = AStarSearch(self.graph, self.start, battery)
        result = astar.search()

        self.assertIsNotNone(result.path)
        self.assertTrue(self.graph.is_charging_station(result.path[-1]))
        self.assertGreater(len(result.path), 2)

    def test_impossible_battery_scenario(self):
        """Very low battery - no path found"""
        battery = 2.0
        ucs = UniformCostSearch(self.graph, self.start, battery)
        astar = AStarSearch(self.graph, self.start, battery)

        ucs_result = ucs.search()
        astar_result = astar.search()

        # Both should return empty path (no solution)
        self.assertEqual(len(ucs_result.path), 0)
        self.assertEqual(len(astar_result.path), 0)
        self.assertEqual(ucs_result.cost, float('inf'))
        self.assertEqual(astar_result.cost, float('inf'))

    def test_path_validity_ucs(self):
        """Check UCS paths are valid"""
        battery = 6.0
        ucs = UniformCostSearch(self.graph, self.start, battery)
        result = ucs.search()

        self._validate_path(result.path)

    def test_path_validity_astar(self):
        """Check A* paths are valid"""
        battery = 6.0
        astar = AStarSearch(self.graph, self.start, battery)
        result = astar.search()

        self._validate_path(result.path)

    def test_battery_constraint_enforcement(self):
        """Check battery limits are followed"""
        battery = 5.0
        ucs = UniformCostSearch(self.graph, self.start, battery)
        astar = AStarSearch(self.graph, self.start, battery)

        ucs_result = ucs.search()
        astar_result = astar.search()

        # Verify that each move in the path is within battery capacity
        for result in [ucs_result, astar_result]:
            if result.path:  # Only check if path exists
                for i in range(len(result.path) - 1):
                    current = result.path[i]
                    next_node = result.path[i + 1]
                    # Find the distance between these nodes
                    for neighbor, distance in self.graph.neighbors(current):
                        if neighbor == next_node:
                            self.assertLessEqual(distance, battery,
                                               f"Move {current}->{next_node} exceeds battery: {distance} > {battery}")
                            break

    def test_algorithm_efficiency_comparison(self):
        """A* should expand fewer nodes than UCS"""
        battery = 6.0
        ucs = UniformCostSearch(self.graph, self.start, battery)
        astar = AStarSearch(self.graph, self.start, battery)

        ucs_result = ucs.search()
        astar_result = astar.search()

        # A* should generally expand fewer or equal nodes
        self.assertLessEqual(astar_result.nodes_expanded, ucs_result.nodes_expanded)

    def test_charging_station_reachability(self):
        """All charging stations should be reachable"""
        battery = 15.0  # High battery to ensure reachability
        ucs = UniformCostSearch(self.graph, self.start, battery)
        astar = AStarSearch(self.graph, self.start, battery)

        ucs_result = ucs.search()
        astar_result = astar.search()

        # Both should find paths
        self.assertGreater(len(ucs_result.path), 1)
        self.assertGreater(len(astar_result.path), 1)

        # Both should reach charging stations
        self.assertTrue(self.graph.is_charging_station(ucs_result.path[-1]))
        self.assertTrue(self.graph.is_charging_station(astar_result.path[-1]))

    def test_graph_connectivity(self):
        """Graph should be connected"""
        # Test that all nodes have neighbors
        for node in self.graph.coords.keys():
            neighbors = self.graph.neighbors(node)
            self.assertGreater(len(neighbors), 0, f"Node {node} has no neighbors")

    def test_charging_stations_exist(self):
        """Charging stations should exist"""
        self.assertGreater(len(self.graph.charging_stations), 0, "No charging stations defined")

        # Verify all charging stations exist in the graph
        for station in self.graph.charging_stations:
            self.assertIn(station, self.graph.coords, f"Charging station {station} not in graph")

    def _validate_path(self, path):
        """Helper to check if path is valid"""
        if not path:
            return  # Empty path is valid (no solution)

        # Check that consecutive nodes are connected
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            neighbors = [n for n, _ in self.graph.neighbors(current)]
            self.assertIn(next_node, neighbors, f"Invalid move: {current} -> {next_node}")

        # Check that final node is a charging station
        self.assertTrue(self.graph.is_charging_station(path[-1]),
                       f"Path does not end at charging station: {path[-1]}")

if __name__ == '__main__':
    unittest.main()
