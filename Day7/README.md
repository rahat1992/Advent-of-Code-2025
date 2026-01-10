# Day 7: Laboratories – Tachyon Manifold

This directory contains my solutions for **Advent of Code – Day 7: Laboratories**.

The problem is described in `problem.txt` and models a tachyon manifold inside a teleporter. A tachyon beam enters the manifold at a starting position `S` and always moves **downward**. Empty space is represented by `.`, and **splitters** are represented by `^`.

In Part 1, you track a classical beam as it is repeatedly split by `^` tiles and count the total number of splits. In Part 2, you apply a many-worlds / quantum interpretation where a single tachyon particle takes **both** paths at every splitter, and you count how many distinct timelines result.

## Input format

- The input file is `input.txt`.
- It is a rectangular grid of characters where each character is:
  - `S` – the starting location of the incoming beam (there is a single `S`).
  - `^` – a splitter.
  - `.` – empty space.
- The beam always starts at row `S` and then moves **downward** one row at a time.

Example (from `problem.txt`):

```text
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
```

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, printing the total number of beam splits.
- Run **Part 2**, printing the total number of distinct timelines for a single quantum tachyon particle.

If you want to use a different input file, you can modify the `input_file` argument in the `__main__` block of `solution.py`.

## Core helpers

### `parse_manifold(input_file)`

- Reads the grid from `input_file`.
- Finds the position of `S` by scanning rows and columns.
- Returns a tuple `(grid, start_row, start_col)` where `grid` is a list of strings.

### `simulate_beams(grid, start_row, start_col)` – classical beam, Part 1

This function simulates **classical** tachyon beams that move downward and split at `^` tiles.

- Maintains a list `active_beams` of beam positions `(row, col)`.
- On each step:
  - Each beam moves one row down.
  - If the next position is **outside** the grid, that beam exits and is removed.
  - If the next cell contains a splitter `^`:
    - The **incoming beam stops**.
    - The splitter produces **two new beams**:
      - One starting at the cell immediately to the left of the splitter.
      - One starting at the cell immediately to the right.
    - The function increments `total_splits` **once per splitter cell**, even if multiple beams arrive at that same cell over time.
      - This is tracked by `split_positions` (a set of `(row, col)` where we’ve already counted a split).
  - If the next cell is `.`, the beam continues downward at the same column.
- Returns `total_splits`.

This corresponds to Part 1’s definition: "how many times will the beam be split?" and correctly handles cases where later beams revisit the same splitter location (that split is only counted once).

### `simulate_quantum_particle(grid, start_row, start_col)` – quantum particle, Part 2

This function simulates a **single** tachyon particle in a quantum manifold using a many-worlds interpretation:

- Instead of individual beams, it tracks a mapping `current_positions` from positions `(row, col)` to the **number of distinct paths** (timelines) that arrive there.
- Iterates row by row from the starting row downwards.
- For each `(row, col)` at the current row with `num_paths` timelines:
  - The particle "moves" down one row.
  - If moving down exits the grid (next row is beyond the last row):
    - All `num_paths` timelines are considered **completed** and added to a `total_exited` counter.
  - If the next cell is a splitter `^`:
    - The particle takes **both** branches:
      - One path continues to the left neighbor cell.
      - One path continues to the right neighbor cell.
    - Both branches inherit the same `num_paths` (i.e., path counts are added into `next_positions` for those neighbor cells).
  - If the next cell is `.`, all `num_paths` simply continue straight down.
- Accumulates paths in `next_positions` for the next row, merging counts if multiple parent paths converge to the same cell.
- At the end, returns `total_exited`, the total number of distinct timelines that have exited the manifold.

This implements the Part 2 semantics: at each splitter the universe branches, and we count the total number of resulting timelines when the particle is done.

## Part 1: Beam splits

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Call `parse_manifold(input_file)` to obtain the grid and starting coordinates.
2. Call `simulate_beams(grid, start_row, start_col)` to simulate the classical beams.
3. Return the total number of splits.

For the sample manifold in `problem.txt`, the total number of splits is **21**. For the actual `input.txt`, the Part 1 answer is **1672**.

## Part 2: Quantum timelines

Implementation: `solve_part2(input_file)`.

High-level approach:

1. Call `parse_manifold(input_file)`.
2. Call `simulate_quantum_particle(grid, start_row, start_col)`.
3. Return the resulting `total_exited` as the total number of timelines.

For the sample manifold, there are **40** distinct timelines. For the actual `input.txt`, the Part 2 answer is **231229866702355**.

## Test coverage (overview)

The tests in `test_solution.py` cover:

- **Parsing**:
  - Simple manifolds and mid-grid `S` positions.
- **Classical beams / Part 1**:
  - Single splitter, no splitters, beam exiting the grid.
  - Cascading and asymmetric splitter arrangements.
  - Edge splitters where only one branch is valid.
  - The full example from the problem (21 splits).
  - A wide manifold and the real `input.txt` (regression for 1672 splits).
- **Quantum particle / Part 2**:
  - Example manifold with 40 timelines.
  - No splitters (1 timeline).
  - Single splitter (2 timelines).
  - Two splitters in series and edge splitters (branching and convergence behavior).
  - Real `input.txt` regression asserting 231229866702355 timelines.

For more detail on the tests, see `Day7/test_solution.py`.

## Files

- `problem.txt` – Full text of the Day 7 puzzle (both parts) and example manifold.
- `input.txt` – Puzzle input (the full tachyon manifold grid).
- `solution.py` – Python implementation with:
  - `parse_manifold(input_file)` – parses the grid and finds `S`.
  - `simulate_beams(grid, start_row, start_col)` – classical beam simulation for Part 1.
  - `simulate_quantum_particle(grid, start_row, start_col)` – quantum many-worlds simulation for Part 2.
  - `solve_part1(input_file)` – returns the number of splits.
  - `solve_part2(input_file)` – returns the number of timelines.
- `test_solution.py` – Unit tests described above.
- `README.md` – This documentation.
