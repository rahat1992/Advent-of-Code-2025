# Day 4: Printing Department – Paper Rolls

This directory contains my solutions for **Advent of Code – Day 4: Printing Department**.

The problem is described in `problem.txt` and involves forklifts moving large rolls of paper around a grid. Each roll of paper is represented by `@`, and empty floor is represented by `.`. The forklifts can only access rolls that are not too crowded by neighboring rolls.

Part 1 asks you to count how many rolls are accessible in the initial configuration. Part 2 asks how many rolls can be removed in total if you repeatedly remove accessible rolls and then re-evaluate accessibility.

## Input format

- The input file is `input.txt`.
- Each **line** is a row of the grid.
- Each character is either:
  - `@` – a roll of paper.
  - `.` – empty space.
- All rows are the same length; there are no separators other than newlines.
- Blank lines are ignored.

For example:

```text
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
```

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, printing the number of rolls accessible to a forklift in the initial grid.
- Run **Part 2**, printing the total number of rolls that can be removed by repeatedly removing accessible rolls until no more can be removed.

If you want to use a different input file, you can modify the `input_file` argument in the `__main__` block of `solution.py`.

## Core helpers

The solution is built around four helper functions in `solution.py`:

- `count_adjacent_rolls(grid, row, col)`
  - Given a grid and a position `(row, col)`, counts how many rolls (`@`) are in the **8 immediately adjacent cells** (up, down, left, right, and the four diagonals).
  - Does **not** require that the position itself contain a roll; it can be used to query adjacency for any cell.

- `count_accessible_rolls(grid)`
  - Iterates over all cells in the grid.
  - For each roll (`@`), calls `count_adjacent_rolls` to compute the number of neighboring rolls.
  - A roll is **accessible** if it has **fewer than 4** adjacent rolls.
  - Returns the total number of accessible rolls in the grid.

- `remove_accessible_rolls(grid)`
  - Identifies all accessible rolls in the current grid using the same rule as Part 1 (fewer than 4 adjacent rolls).
  - Produces a **new grid** in which all accessible rolls for this pass have been replaced by `.`.
  - Returns a tuple `(new_grid, removed_count)`, where `removed_count` is the number of rolls removed in that pass.

- `count_total_removable_rolls(grid)`
  - Repeatedly calls `remove_accessible_rolls` starting from the initial grid.
  - Accumulates the count of removed rolls across all passes.
  - Stops once a pass removes **0** rolls, meaning no more rolls are accessible.
  - Returns the total number of rolls removed across all iterations.

These helpers directly support the two puzzle parts.

## Part 1: Accessible rolls in the initial grid

In **Part 1**, a roll of paper is considered accessible if it has **fewer than four** neighboring rolls in the 8 adjacent cells.

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Read all non-empty lines from `input_file` into a list of strings `grid`.
2. Call `count_accessible_rolls(grid)` to count how many `@` cells have fewer than 4 adjacent rolls.
3. Return this count as the Part 1 answer.

On the sample grid from `problem.txt`, `count_accessible_rolls` finds **13** accessible rolls. For the full puzzle input, the total accessible rolls are **1428**.

## Part 2: Total rolls removable by repeated passes

In **Part 2**, you repeatedly remove accessible rolls and then re-evaluate accessibility after each removal:

1. Compute which rolls are currently accessible (fewer than 4 adjacent rolls).
2. Remove all of them simultaneously.
3. Repeat from step 1 on the new grid until no more rolls are accessible.

Implementation: `solve_part2(input_file)`.

High-level approach:

1. Read all non-empty lines from `input_file` into `grid`.
2. Call `count_total_removable_rolls(grid)`, which:
   - Uses `remove_accessible_rolls` in a loop to peel away accessible rolls layer by layer.
   - Sums `removed_count` across all passes until a pass removes zero rolls.
3. Return the final total as the Part 2 answer.

On the sample grid from `problem.txt`, this process removes **43** rolls in total. For the full puzzle input, the total removable rolls are **8936**.

## Files

- `problem.txt` – Full text of the Day 4 puzzle (both parts).
- `input.txt` – Puzzle input (grid of `@` and `.` characters).
- `solution.py` – Python implementation with:
  - `count_adjacent_rolls(grid, row, col)` – counts neighboring rolls.
  - `count_accessible_rolls(grid)` – counts accessible rolls in a static grid.
  - `remove_accessible_rolls(grid)` – removes all currently accessible rolls in one pass.
  - `count_total_removable_rolls(grid)` – repeatedly removes accessible rolls until none remain.
  - `solve_part1(input_file)` – Part 1 solver.
  - `solve_part2(input_file)` – Part 2 solver.
- `test_solution.py` – Unit tests covering:
  - Adjacency counting (corners, edges, center, isolated rolls, and non-roll cells).
  - Accessibility logic on various patterns (example grid, dense clusters, lines, crosses, sparse configurations, and boundary cases for 3 vs 4 neighbors).
  - The iterative removal process across one or multiple passes, including the example where 43 rolls are removed.
  - Optional regression checks against the real `input.txt` for both parts.
- `README.md` – This documentation.
