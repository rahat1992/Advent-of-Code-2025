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

- **Day 1**
  - From the repository root:
    - Change into the directory:
      - `cd Day1`
    - Run the solution (reads `Day1/input.txt`):
      - `python solution.py`
- **Day 2**
  - From the repository root:
    - `cd Day2`
    - Run the solution (reads `Day2/input.txt`):
      - `python solution.py`

**Pattern for new days:** create a `DayN/` directory with a `solution.py` that reads `input.txt` from the current working directory, then run it by `cd DayN && python solution.py`.

### Run tests for a single day

Each day has a dedicated `test_solution.py` using `unittest`. Tests are designed to be run from inside the day's directory.

- **Run all tests for a day**
  - Day 1: `cd Day1 && python -m unittest`
  - Day 2: `cd Day2 && python -m unittest`

- **Run a specific test module**
  - Day 1: `cd Day1 && python -m unittest test_solution`
  - Day 2: `cd Day2 && python -m unittest test_solution`

- **Run a single test case or method**
  - Example (Day 1, specific test method):
    - `cd Day1 && python -m unittest test_solution.TestSafeSolution.test_part1_example`
  - Example (Day 2, full test case class):
    - `cd Day2 && python -m unittest test_solution.TestGiftShop`

When running tests from the repository root via discovery (e.g., `python -m unittest discover -s Day1 -p "test_*.py"`), note that tests which reference `input.txt` use a relative path; those checks will only run if `input.txt` is present in the **current working directory**.

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
    - `solve_part1(input_file)` – counts how many times a dial ends at position `0` after each rotation.
    - `solve_part2(input_file)` – counts every time the dial passes through or lands on `0` during rotations, accounting for full cycles and partial wraps.
  - `Day1/README.md` documents the puzzle, dial mechanics, and the reasoning behind both parts; refer there for detailed problem context.
  - `test_solution.py` contains a comprehensive test suite, including:
    - Example-based tests mirroring the problem description.
    - Edge cases for wrapping behaviour.
    - Optional checks against the actual `input.txt` if present.

- **Day 2 (`Day2/`) – Invalid Product IDs**
  - `solution.py` defines:
    - `is_invalid_id(num)` – returns `True` if a numeric ID consists of a digit/digit-sequence repeated exactly twice (e.g., `55`, `6464`, `123123`), with safeguards against leading-zero artefacts.
    - `solve_part1(input_file)` – parses a comma-separated list of inclusive ranges like `11-22,95-115,...`, scans all IDs in each range, and returns `(total_sum_of_invalid_ids, list_of_invalid_ids)`.
  - `test_solution.py`:
    - Thoroughly exercises `is_invalid_id` for different lengths and patterns.
    - Verifies behaviour on example ranges and the full example input string.
    - Optionally validates the actual puzzle answer when `input.txt` exists.

### Extending the repository

When adding a new puzzle day, follow the existing pattern for consistency and easy discoverability by future agents:

1. Create a new directory `DayN/` at the repository root.
2. Add `solution.py` exposing clear, top-level solver functions (e.g., `solve_part1`, `solve_part2`) that accept an `input_file` path.
3. Add `test_solution.py` using `unittest`, mirroring the style of `Day1/test_solution.py` and `Day2/test_solution.py`:
   - Include example-driven tests based on the problem statement.
   - Optionally add tests that run against the real `input.txt` when present.
4. Place the puzzle input as `DayN/input.txt` and, if helpful, `DayN/problem.txt` and a short `DayN/README.md` documenting the approach.
