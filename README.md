# EV Charging Station Finder

A Python project demonstrating Uniform Cost Search (UCS) and A* Search algorithms for electric vehicle routing with battery constraints.

## Quick Start

```bash
git clone <https://github.com/kleahila/CEN352-Artificial_Intelligence_Assignment1.git>
cd ev-charging-station-finder
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## What It Does

Finds the shortest path from any starting point to the nearest charging station while respecting battery limitations. Compares UCS vs A* performance on a realistic city graph.

## Requirements

- Python 3.9+
- pip

## Installation

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate    # macOS/Linux
# OR
.venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Command
```bash
python main.py
```
Runs with random start location and battery level.

### Options
```bash
python main.py [OPTIONS]

Options:
  --start NODE, -s NODE        Start at specific node (A-K)
  --battery KM, -b KM          Set battery capacity in km
  --help, -h                   Show help
```

### Examples
```bash
# Random everything
python main.py

# Set battery only
python main.py --battery 5.5

# Set start only
python main.py --start B

# Set both
python main.py --start F --battery 8.0
```

## Output

**Terminal:**
- Search results from both algorithms
- Path found, distance, nodes explored, runtime
- Error if no charging station is reachable

**Files** (when solution exists):
- `outputs/graph.png` - City map with path highlighted
- `outputs/performance.png` - Algorithm comparison chart

## How It Works

**Problem Setup:**
- City with 11 locations (A-K)
- 5 charging stations (C, E, G, I, K)
- EV can only travel distances ≤ current battery
- Battery recharges at every stop

**Algorithms:**
- **UCS**: Explores by total distance from start
- **A***: Uses straight-line distance heuristic to nearest charger

Both guarantee optimal paths but A* is usually faster.

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=.
```

Includes 14 tests covering:
- Path finding accuracy
- Battery constraint enforcement
- Edge cases (insufficient charge)
- Algorithm performance comparison

## Project Structure

```
├── main.py                    # CLI entry point
├── graph/city_graph.py        # City layout & connections
├── search/algorithms.py       # UCS & A* implementations
├── visualization/             # Graph & chart generation
├── utils/performance.py       # Result tracking
├── tests/test_algorithms.py   # Unit tests
└── outputs/                   # Generated images
```

## Key Features

- Random or specified start locations
- Realistic battery constraints
- Side-by-side algorithm comparison
- Visual path and performance outputs
- Comprehensive test suite
- Clear error messages for impossible routes
