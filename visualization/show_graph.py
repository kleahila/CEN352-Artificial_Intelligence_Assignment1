"""
Graph Visualization Module

This module provides visualization of the city graph with the optimal path highlighted.
"""

import networkx as nx
import matplotlib.pyplot as plt
from graph.city_graph import CityGraph

class GraphVisualizer:
    """
    Visualizes the city graph and highlights the optimal path.
    """

    def __init__(self, graph: CityGraph):
        """
        Initialize the visualizer with a city graph.

        Args:
            graph: The city graph to visualize
        """
        self.graph = graph

    def draw_graph(self, ucs_path: list = None, astar_path: list = None):
        """
        Draw the city graph with charging stations and the optimal paths highlighted.

        Args:
            ucs_path: The UCS path to highlight (optional)
            astar_path: The A* path to highlight (optional)
        """
        # Suppress matplotlib warnings
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

        # Create NetworkX graph
        G = nx.Graph()

        # Add nodes with positions
        for node, pos in self.graph.coords.items():
            G.add_node(node, pos=pos)

        # Add edges
        for node, neighbors in self.graph.graph.items():
            for neighbor, distance in neighbors:
                G.add_edge(node, neighbor, weight=distance)

        # Get positions
        pos = nx.get_node_attributes(G, 'pos')

        # Create figure
        plt.figure(figsize=(12, 8))

        # Draw all edges with labels
        edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edges(G, pos, edge_color='black', width=2)
        # Only draw edge labels if we have valid positions
        try:
            nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
        except:
            pass  # Skip edge labels if there are positioning issues

        # Highlight paths - handle identical paths specially
        paths_identical = (ucs_path == astar_path) and ucs_path is not None and len(ucs_path) > 1

        if paths_identical:
            # When paths are identical, show only A* path with a note in title
            if astar_path and len(astar_path) > 1:
                astar_edges = [(astar_path[i], astar_path[i+1]) for i in range(len(astar_path)-1)]
                valid_astar_edges = [(u, v) for u, v in astar_edges if u in pos and v in pos]
                if valid_astar_edges:
                    try:
                        nx.draw_networkx_edges(G, pos, edgelist=valid_astar_edges, edge_color='red', width=3)
                    except:
                        pass  # Skip drawing if there are issues
        else:
            # When paths differ, show both
            # Highlight UCS path in blue (dashed)
            if ucs_path and len(ucs_path) > 1:
                ucs_edges = [(ucs_path[i], ucs_path[i+1]) for i in range(len(ucs_path)-1)]
                valid_ucs_edges = [(u, v) for u, v in ucs_edges if u in pos and v in pos]
                if valid_ucs_edges:
                    try:
                        nx.draw_networkx_edges(G, pos, edgelist=valid_ucs_edges, edge_color='blue',
                                             width=3, style='dashed')
                    except:
                        pass  # Skip drawing if there are issues

            # Highlight A* path in red (solid)
            if astar_path and len(astar_path) > 1:
                astar_edges = [(astar_path[i], astar_path[i+1]) for i in range(len(astar_path)-1)]
                valid_astar_edges = [(u, v) for u, v in astar_edges if u in pos and v in pos]
                if valid_astar_edges:
                    try:
                        nx.draw_networkx_edges(G, pos, edgelist=valid_astar_edges, edge_color='red', width=3)
                    except:
                        pass  # Skip drawing if there are issues

        # Draw regular nodes (non-charging stations) in light gray
        regular_nodes = [node for node in G.nodes() if not self.graph.is_charging_station(node)]
        try:
            nx.draw_networkx_nodes(G, pos, nodelist=regular_nodes, node_color='lightgray',
                                 node_size=600, edgecolors='gray', linewidths=1)
        except:
            pass  # Skip node drawing if there are issues

        # Draw charging station nodes in green
        charging_nodes = [node for node in G.nodes() if self.graph.is_charging_station(node)]
        try:
            nx.draw_networkx_nodes(G, pos, nodelist=charging_nodes, node_color='lightgreen',
                                 node_size=800, edgecolors='darkgreen', linewidths=2)
        except:
            pass  # Skip node drawing if there are issues

        # Draw labels
        try:
            nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        except:
            pass  # Skip label drawing if there are issues

        # Add title and legend
        if paths_identical:
            plt.title("EV Charging Station Route (UCS and A* found identical path)", fontsize=14, pad=20)
        else:
            plt.title("EV Charging Station Routes (UCS vs A*)", fontsize=14, pad=20)
        plt.axis('off')

        # Create legend
        import matplotlib.patches as mpatches
        import matplotlib.lines as mlines
        gray_patch = mpatches.Patch(color='lightgray', label='Regular Node')
        green_patch = mpatches.Patch(color='lightgreen', label='Charging Station')

        legend_handles = [gray_patch, green_patch]

        # Add path legends based on what was drawn
        if paths_identical:
            # When paths are identical, only A* path is shown
            if astar_path and len(astar_path) > 1 and all(node in pos for node in astar_path):
                red_line = mlines.Line2D([], [], color='red', linewidth=3, label='Optimal Path (UCS = A*)')
                legend_handles.append(red_line)
        else:
            # When paths differ, show both legends
            if ucs_path and len(ucs_path) > 1 and all(node in pos for node in ucs_path):
                blue_line = mlines.Line2D([], [], color='blue', linewidth=3, linestyle='--', label='UCS Path')
                legend_handles.append(blue_line)

            if astar_path and len(astar_path) > 1 and all(node in pos for node in astar_path):
                red_line = mlines.Line2D([], [], color='red', linewidth=3, label='A* Path')
                legend_handles.append(red_line)

        plt.legend(handles=legend_handles, loc='upper left')

        # Save the figure
        plt.tight_layout()
        plt.savefig('outputs/graph.png', dpi=300, bbox_inches='tight')
        plt.close()
