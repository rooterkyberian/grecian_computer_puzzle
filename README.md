# Grecian Computer Puzzle Solver

A solver for the Grecian Computer puzzle, which consists of 4 rotating discs stacked on top of each other with numbers that need to sum to a target value.

In theory

## Setup

```bash
uv sync
```

## Usage

### 1. Prepare input template

Generate a CSV file template for your puzzle input:

```bash
uv run python prepare_input_file.py -o input.csv
```

### 2. Fill in values

Mark first column (x=0) on each disc with some tape as a reference point if not already marked.
Edit the generated CSV file and fill in the `value` column with numbers from your puzzle.
Use `n` for empty cells.

File goes from bottom disc (z=0) to top disc (z=4), from outermost ring (y=0) to innermost ring (y=3), and from reference point (x=0) clockwise to x=11.
So you first fill in outermost ring of bottom disc, then next inner ring of bottom disc, and so on for all discs.

It doesn't matter where you mark x=0 or y=0 (outermost or innermost ring), as long as you are consistent.

### 3. Solve

```bash
uv run python solve.py input.csv
```

## File Format

The input CSV has 4 columns:
- `x`: column position (0-11)
- `y`: row position (0-3)
- `z`: disc layer (0-4, where 0 is bottom)
- `value`: the number at that position, or `n` for hidden cells