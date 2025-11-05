"""
Makes performance charts for the search algorithms
"""

import matplotlib.pyplot as plt
from utils.performance import SearchResult

class ChartMaker:
    """Makes charts comparing UCS and A*"""

    def compare_performance(self, ucs_result: SearchResult, astar_result: SearchResult):
        """Make a chart comparing nodes expanded, time, and cost"""
        algorithms = ['UCS', 'A*']
        nodes_expanded = [ucs_result.nodes_expanded, astar_result.nodes_expanded]
        runtimes = [ucs_result.runtime, astar_result.runtime]
        costs = [ucs_result.cost, astar_result.cost]

        # Create subplots
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Nodes Expanded
        bars1 = axes[0].bar(algorithms, nodes_expanded, color=['blue', 'orange'])
        axes[0].set_title('Nodes Expanded')
        axes[0].set_ylabel('Count')
        self._add_value_labels(axes[0], bars1)

        # Runtime
        bars2 = axes[1].bar(algorithms, runtimes, color=['blue', 'orange'])
        axes[1].set_title('Runtime (seconds)')
        axes[1].set_ylabel('Time (s)')
        self._add_value_labels(axes[1], bars2)

        # Total Cost
        bars3 = axes[2].bar(algorithms, costs, color=['blue', 'orange'])
        axes[2].set_title('Total Cost (km)')
        axes[2].set_ylabel('Distance (km)')
        self._add_value_labels(axes[2], bars3)

        # Overall title
        fig.suptitle('UCS vs A* Search Performance on EV Routing Problem', fontsize=14)

        # Adjust layout and save
        plt.tight_layout()
        plt.savefig('outputs/performance.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _add_value_labels(self, ax, bars):
        """Add numbers on top of bars"""
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}' if height < 1 else f'{height:.1f}',
                    ha='center', va='bottom')
