# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

This repository contains solutions to Advent of Code-style puzzles, organized one day per directory (e.g., `Day1/`, `Day2/`). Each day is implemented as a small, self-contained Python project with:

- `solution.py` – main solution entry points
- `test_solution.py` – unit tests using the standard library `unittest`
- `input.txt` – puzzle input for that day
- `problem.txt` – puzzle statement for that day (when present)
- Day-specific docs such as `README.md` where applicable (e.g., `Day1/README.md`)

There is no global build system or dependency file; everything uses the Python standard library.

## Commands

All commands below assume a recent CPython 3 is available on `PATH`. There are no external dependencies.

### Run a day's solution

Solutions are meant to be run from within each day directory so that relative paths to `input.txt` work correctly.

- **Any implemented day (e.g., `Day1/`–`Day5/`)**
  - From the repository root:
    - `cd DayN`
    - Run the solution (reads `DayN/input.txt`):
      - `python3 solution.py`

**Pattern for new days:** create a `DayN/` directory with a `solution.py` that reads `input.txt` from the current working directory, then run it by `cd DayN && python3 solution.py`.

### Run tests for a single day

Each day has a dedicated `test_solution.py` using `unittest`. Tests are designed to be run from inside the day's directory.

- **Run all tests for a day**
  - Any day: `cd DayN && python3 -m unittest`

- **Run a specific test module**
  - Any day: `cd DayN && python3 -m unittest test_solution`

- **Run a single test case or method**
  - Example (Day 1, specific test method):
    - `cd Day1 && python3 -m unittest test_solution.TestSafeSolution.test_part1_example`
  - Example (Day 2, full test case class):
    - `cd Day2 && python3 -m unittest test_solution.TestGiftShop`

When running tests from the repository root via discovery (e.g., `python3 -m unittest discover -s Day1 -p "test_*.py"`), note that tests which reference `input.txt` use a relative path; those checks will only run if `input.txt` is present in the **current working directory**.

## Architecture and conventions

### Per-day structure

Each Advent of Code day is isolated in its own directory, following a consistent pattern:

- `DayN/solution.py` exposes one or more top-level solver functions (e.g., `solve_part1`, `solve_part2`) and an `if __name__ == "__main__"` block that wires them to `input.txt`.
- `DayN/test_solution.py` imports these functions directly (`from solution import ...`) and:
  - Builds small synthetic inputs in temporary files to validate behaviour.
  - Optionally validates results against the real `input.txt` if it exists.
- Inputs and problem statements live alongside the code so each day can be worked on independently.

### Day-specific notes

- **Day 1 (`Day1/`) – Secret Entrance**
  - Implements two solver functions in `solution.py`:
    - `solve_part1(input_file)` – counts how many times the dial ends at position `0` after each rotation.
    - `solve_part2(input_file)` – counts every time the dial passes through or lands on `0` during rotations, accounting for full cycles and partial wraps.
  - `Day1/README.md` documents the puzzle, dial mechanics, and the reasoning behind both parts; refer there for detailed problem context.
  - `test_solution.py` contains a comprehensive test suite, including:
    - Example-based tests mirroring the problem description.
    - Edge cases for wrapping behaviour.
    - Optional checks against the actual `input.txt` if present.

- **Day 2 (`Day2/`) – Gift Shop / Invalid Product IDs**
  - `solution.py` defines:
    - `is_invalid_id_part1(num)` – Part 1 rule: a numeric ID made of a digit/digit-sequence repeated **exactly twice** (e.g., `55`, `6464`, `123123`), with safeguards against leading-zero artefacts.
    - `is_invalid_id_part2(num)` – Part 2 rule: a numeric ID made of a digit/digit-sequence repeated **at least twice** (e.g., `12341234`, `123123123`, `1111111`).
    - `solve_part1(input_file)` – parses a comma-separated list of inclusive ranges like `11-22,95-115,...`, scans all IDs under the Part 1 rule, and returns `(total_sum_of_invalid_ids, list_of_invalid_ids)`.
    - `solve_part2(input_file)` – reuses the same ranges but applies the Part 2 rule.
  - `Day2/README.md` describes both parts and how the ID rules differ.
  - `test_solution.py`:
    - Thoroughly exercises both invalid-ID predicates across many patterns and lengths.
    - Verifies behaviour on the example ranges and the full example input string.
    - Optionally validates the actual puzzle answers for both parts when `input.txt` exists.

- **Day 3 (`Day3/`) – Lobby / Battery Banks**
  - `solution.py` defines:
    - `find_max_joltage_n_batteries(bank, n)` – greedy selector that chooses exactly `n` digits from a bank (string of digits) in order to form the largest possible number.
    - `find_max_joltage(bank)` – convenience wrapper for `n = 2` (Part 1 behaviour).
    - `solve_part1(input_file)` – for each line/bank, selects 2 digits and sums the resulting per-bank joltages.
    - `solve_part2(input_file)` – for each bank, selects 12 digits and sums the resulting joltages.
  - `Day3/README.md` documents the battery-bank model, the greedy selection strategy, and both parts.
  - `test_solution.py`:
    - Covers the example banks and totals from the problem statement.
    - Exercises the selector with ascending, descending, repeated, and mixed digits, and multiple `n` values (including near full-length selections).
    - Optionally validates the actual puzzle answers for both parts when `input.txt` exists.

- **Day 4 (`Day4/`) – Printing Department / Paper Rolls**
  - `solution.py` defines:
    - `count_adjacent_rolls(grid, row, col)` – counts neighboring rolls (`@`) in the 8 surrounding cells.
    - `count_accessible_rolls(grid)` – counts how many rolls have fewer than 4 adjacent rolls (forklift-accessible in the current grid).
    - `remove_accessible_rolls(grid)` – removes all currently accessible rolls in a single pass and returns the updated grid and removed count.
    - `count_total_removable_rolls(grid)` – repeatedly removes accessible rolls until none remain and returns the total removed.
    - `solve_part1(input_file)` – reads the grid and returns the number of accessible rolls in the initial configuration.
    - `solve_part2(input_file)` – returns the total number of rolls that can be removed by repeated passes.
  - `Day4/README.md` describes the grid model, accessibility rule, and iterative removal process for both parts.
  - `test_solution.py`:
    - Exercises adjacency counting on corners, edges, center cells, and isolated rolls.
    - Verifies accessibility counts on dense clusters, lines, crosses, and sparse patterns, including boundary cases for exactly 3 vs 4 neighbors.
    - Confirms the iterative removal logic on the example and synthetic grids, and validates the actual puzzle answers when `input.txt` exists.

- **Day 5 (`Day5/`) – Cafeteria / Fresh Ingredients**
  - `solution.py` defines:
    - `parse_input(input_file)` – parses a two-section file into a list of inclusive freshness ranges and a list of ingredient IDs.
    - `is_fresh(ingredient_id, ranges)` – predicate indicating whether an ID falls within any freshness range.
    - `count_fresh_ingredients(ranges, ingredient_ids)` – counts how many available ingredient IDs are fresh (Part 1 core).
    - `merge_ranges(ranges)` – merges overlapping/adjacent ranges into a minimal non-overlapping set.
    - `count_total_fresh_ids(ranges)` – counts all fresh IDs implied by the merged ranges (Part 2 core).
    - `solve_part1(input_file)` – parses the file and returns the number of available ingredient IDs that are fresh.
    - `solve_part2(input_file)` – returns the total number of distinct fresh IDs after merging overlapping ranges.
  - `test_solution.py` (`TestCafeteria`) provides:
    - Example-driven tests that mirror the puzzle statement, including the sample input and expected counts for both parts.
    - Extensive property-style coverage for `is_fresh`, `merge_ranges`, and `count_total_fresh_ids` (boundaries, overlaps, adjacency, empty/large ranges).
    - Optional assertions against the real `input.txt` that lock in the final puzzle answers for future refactors.

- **Day 6 (`Day6/`) – Unimplemented stub**
  - Contains `input.txt` and `problem.txt` only; no `solution.py` or `test_solution.py` yet.
  - When implementing Day 6, follow the "Extending the repository" guidelines below to mirror the existing per-day structure.

### Extending the repository

When adding a new puzzle day, follow the existing pattern for consistency and easy discoverability by future agents:

1. Create a new directory `DayN/` at the repository root.
2. Add `solution.py` exposing clear, top-level solver functions (e.g., `solve_part1`, `solve_part2`) that accept an `input_file` path.
3. Add `test_solution.py` using `unittest`, mirroring the style of `Day1/test_solution.py` and `Day2/test_solution.py`:
   - Include example-driven tests based on the problem statement.
   - Optionally add tests that run against the real `input.txt` when present.
4. Place the puzzle input as `DayN/input.txt` and, if helpful, `DayN/problem.txt` and a short `DayN/README.md` documenting the approach.
