# InbentoSolver

Solves a given puzzle from the game "Inbento".

## Installation

To install,

```bash
python3 -m venv .venv			# create virtual environment
source .venv/bin/activate		# use virtual environment
pip3 install uv
uv sync
```

## Usage

Check the available commands with
```bash
python3 main.py --help
```

To find the steps to solve a particular level (say level 1-1), run the following command:
```bash
python3 main.py inbento_solver/data/level011.json
```

Level information is stored in JSON files in `inbento_solver/data/`.
