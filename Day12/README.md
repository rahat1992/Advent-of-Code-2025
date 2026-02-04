# Day 12: Christmas Tree Farm – Present Packing

This directory contains my solutions for **Advent of Code – Day 12: Christmas Tree Farm**.

The problem is described in `problem.txt` and involves fitting oddly-shaped presents into rectangular regions under Christmas trees.

## Input format

- The input file is `input.txt`.
- **Section 1 – Shape definitions:** Each shape starts with `N:` (0-indexed) followed by lines of `#` (occupied) and `.` (empty) on a grid.
- **Section 2 – Region definitions:** Each line has the form `WxH: c0 c1 c2 ...`, where `W` is width, `H` is height, and `c0 c1 ...` are the counts of each shape needed.
- Shapes can be rotated and flipped. Pieces cannot overlap but can interlock (empty cells within a shape's bounding box don't block).

Example (from `problem.txt`):

```text
0:
###
##.
##.

4:
###
#..
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
```

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will run **Part 1**, printing how many regions can fit all their listed presents. Part 2 is a story-only free star.

## Core helpers

### Parsing

- `parse_input(input_file)`:
  - Reads line-by-line, detecting shape definitions (`N:` followed by grid lines) and region definitions (`WxH: counts`).
  - Returns a dictionary of shapes (each a `frozenset` of `(row, col)` coordinates) and a list of region tuples `(width, height, counts)`.

### Shape orientation

- `normalize(cells)`: Shifts a set of coordinates so the top-left is at `(0, 0)`.
- `get_orientations(cells)`: Generates all unique orientations of a shape by applying 4 rotations and 2 reflections (up to 8 transforms), deduplicating via frozensets. A 2x2 square produces 1 orientation; asymmetric shapes produce up to 8.

### Backtracking solver

- `solve_region_backtrack(width, height, shape_counts, all_orientations)`:
  - Cell-scanning approach with integer bitmask grids for fast conflict detection.
  - Iterates cells left-to-right, top-to-bottom; at each empty cell, tries all piece placements whose leftmost occupied cell is the current cell.
  - For **exact cover** (`total_piece_area == grid_area`), failing to cover a cell prunes immediately.
  - For **partial cover**, uncoverable cells are skipped via loop continuation (not recursive calls), avoiding exponential skip-branching.

## Part 1: How many regions can fit all presents?

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Parse all shapes and regions.
2. Compute the maximum bounding-box size across all shape orientations.
3. For each region, apply checks in order:
   - **Area check:** If `total_piece_area > grid_area`, reject immediately.
   - **Box-tiling fast path:** Every shape fits within a `max_box_size × max_box_size` bounding box (3×3 for all shapes in this puzzle). If `total_pieces <= floor(W/3) * floor(H/3)`, we can tile the grid with non-overlapping boxes and place one piece per box — always feasible.
   - **Backtracking fallback:** For small or tight grids where the box check is too conservative, run the full backtracking solver.

For the actual input (1000 regions, grids 35×35 to 50×50, 121–387 pieces each), all regions are resolved by the area check or box-tiling fast path — no backtracking needed.

For the example, **2** of 3 regions can fit all their presents.

## Part 2: Free star (story only)

No additional computation required. Completing Part 1 awards both stars.

## Tests

`test_solution.py` covers:

- `test_parse_shapes` / `test_parse_regions` – input parsing of shapes and region definitions.
- `test_orientations` – rotation/flip deduplication (square has 1 orientation).
- `test_region1_fits` – 4×4 with 2 interlocking shape-4 pieces fits.
- `test_region2_fits` – 12×5 with 6 mixed pieces fits.
- `test_region3_no_fit` – 12×5 with 7 pieces does NOT fit.
- `test_solve_part1_example` – validates answer of 2 for the example.
- `test_actual_input_part1` – regression test against `input.txt`.

## Files

- `problem.txt` – Full text of the Day 12 puzzle (both parts).
- `input.txt` – Puzzle input (6 shape definitions + 1000 regions).
- `solution.py` – Python implementation with fast box-tiling check and backtracking fallback.
- `test_solution.py` – Unit tests.
- `README.md` – This documentation.
