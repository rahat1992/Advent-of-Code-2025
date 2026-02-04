# CLAUDE.md

## Overview

This repository contains Advent of Code-style programming puzzles, organized one per directory (`Day1/` through `Day12/`). Each day is self-contained. All solutions are **Python 3** (tested with 3.14) using **only the standard library** — no external dependencies, no `requirements.txt`, no virtual environment.

## Repository structure

```
Advent-of-Code-2025/
├── DayN/
│   ├── solution.py          # Main solution code
│   ├── test_solution.py     # Unit tests (unittest)
│   ├── input.txt            # Puzzle input
│   ├── problem.txt          # Full puzzle statement
│   └── README.md            # Day-specific docs (approach, examples)
├── README.md                # Top-level overview with per-day algorithm summaries
├── WARP.md                  # Guidance for Warp AI
└── CLAUDE.md                # This file
```

## Commands

All commands must be run from inside the day's directory (relative paths to `input.txt` are used).

### Run a solution
```bash
cd DayN && python3 solution.py
```

### Run all tests for a day
```bash
cd DayN && python3 -m unittest
```

### Run a specific test
```bash
cd DayN && python3 -m unittest test_solution.TestClassName.test_method_name
```

### Run tests with verbose output
```bash
cd DayN && python3 -m unittest -v
```

## Code conventions

### Solution files (`solution.py`)

- Expose top-level solver functions: `solve_part1(input_file)` and `solve_part2(input_file)`.
- Break logic into small, composable helper functions (e.g., `parse_input`, `parse_line`, domain-specific helpers) that are independently testable.
- Each solver reads from a file path argument — do not hardcode `input.txt` except in the `if __name__ == "__main__"` block.
- The `__main__` block prints results for both parts:
  ```python
  if __name__ == "__main__":
      print("Part 1:")
      result1 = solve_part1("input.txt")
      print(f"Result: {result1}")

      print("\nPart 2:")
      result2 = solve_part2("input.txt")
      print(f"Result: {result2}")
  ```
- Use only the Python standard library (`functools`, `collections`, `re`, `itertools`, `fractions`, etc.). Never introduce external packages.
- Functions use docstrings (triple-quoted) to describe purpose. Inline comments explain non-obvious logic.

### Test files (`test_solution.py`)

- Use `unittest.TestCase` — not pytest (though pytest can also discover these tests).
- Import solver functions and helpers directly: `from solution import solve_part1, solve_part2, ...`
- Test class naming matches the puzzle theme (e.g., `TestSafeSolution`, `TestGiftShop`, `TestDay11`).
- Tests include:
  1. **Example-based tests** from the problem statement (primary validation).
  2. **Edge-case tests** for boundary conditions and special inputs.
  3. **Helper-level unit tests** for internal functions (e.g., parsers, predicates).
  4. **Regression tests** against the real `input.txt` — guarded with `if os.path.exists("input.txt")` so they skip gracefully if the file is absent.
- Temporary test input files are created in `setUp()` and cleaned up in `tearDown()` using `os.remove()`.
- Final line: `unittest.main(verbosity=2)`.

### Input parsing patterns

- Read with `open(input_file, 'r')` and iterate lines.
- Strip whitespace: `line.strip()`.
- Skip blank lines: `if not line: continue` or filter with list comprehension.
- Parse formats vary by day: split on delimiters, regex extraction, fixed-width column parsing, etc.

## Adding a new day

1. Create `DayN/` directory at the repo root.
2. Add these files following existing conventions:
   - `problem.txt` — full puzzle statement
   - `input.txt` — puzzle input
   - `solution.py` — with `solve_part1(input_file)`, `solve_part2(input_file)`, helper functions, and `__main__` block
   - `test_solution.py` — `unittest`-based tests covering examples, edge cases, helpers, and optional regression against `input.txt`
   - `README.md` — short description of the puzzle, approach, how to run, and file listing
3. Update the top-level `README.md` with a new "Day N" section summarizing the puzzle, algorithms, and relationship between parts.

## Git conventions

- Commit messages are short, imperative-style summaries (e.g., "Add Day10 README and document indicator light DP solution").
- The default branch is `master`.
- Remote: `origin` → `https://github.com/rahat1992/Advent-of-Code-2025.git`

## Key technical patterns across days

- **Modular arithmetic** (Day 1): `(pos ± distance) % N`
- **String pattern matching** (Day 2): half-string comparisons, factor-based repetition detection
- **Greedy subsequence selection** (Day 3): pick best digit while ensuring enough remain
- **2D grid simulation** (Days 4, 7): neighbor counting, iterative erosion/peeling, multi-beam tracking
- **Interval merging** (Day 5): sort-then-merge for overlapping ranges
- **Fixed-width text parsing** (Day 6): column-based problem segmentation, RTL reading
- **Union-Find / Kruskal's** (Day 8): component tracking with edge sorting by Euclidean distance
- **Computational geometry** (Day 9): polygon interior checks, range compression, rectangle validation
- **Bitmask DP / Linear algebra** (Day 10): XOR toggle optimization, Gaussian elimination over rationals
- **DAG path counting with memoization** (Day 11): `@lru_cache` DFS, state-augmented DFS with `frozenset` for waypoint constraints
- **2D piece packing / polyomino tiling** (Day 12): dihedral group orientations, bitmask backtracking with cell-scanning, box-tiling fast path for large grids
