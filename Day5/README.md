# Day 5: Cafeteria – Fresh Ingredients

This directory contains my solutions for **Advent of Code – Day 5: Cafeteria**.

The problem is described in `problem.txt` and involves determining which ingredient IDs are fresh according to a set of inclusive ranges. Part 1 asks how many of the **available ingredient IDs** are fresh; Part 2 asks how many **total IDs** are considered fresh by the ranges, regardless of which IDs are available.

## Input format

- The input file is `input.txt`.
- It has **two sections** separated by a blank line:
  1. **Fresh ingredient ranges** (one per line), in the form `start-end`.
  2. **Available ingredient IDs** (one per line), each a single integer.

Example (from `problem.txt`):

```text
3-5
10-14
16-20
12-18

1
5
8
11
17
32
```

- Ranges are **inclusive** (`3-5` means `3`, `4`, and `5` are fresh).
- Ranges may **overlap**; an ID is fresh if it falls in **any** range.

In the example:

- Fresh IDs among the available ones are `5`, `11`, and `17` → 3 fresh IDs.
- For Part 2, the ranges consider `3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20` fresh → 14 total IDs.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, printing how many available ingredient IDs are fresh.
- Run **Part 2**, printing how many total ingredient IDs are considered fresh by the ranges.

If you want to use a different input file, you can modify the `input_file` argument in the `__main__` block of `solution.py`.

## Core helpers

The implementation in `solution.py` is structured as a set of small, focused helpers.

### `parse_input(input_file)`

- Reads the entire input file and splits it on a blank line into two parts:
  - First part: fresh ranges (`start-end` per line).
  - Second part: available ingredient IDs (one per line).
- Returns a tuple `(ranges, ingredient_ids)` where:
  - `ranges` is a list of `(start, end)` tuples of integers.
  - `ingredient_ids` is a list of integer IDs.

### `is_fresh(ingredient_id, ranges)`

- Returns `True` if `ingredient_id` lies within **any** of the inclusive ranges.
- Simple linear scan over `ranges`, checking `start <= ingredient_id <= end`.

### `count_fresh_ingredients(ranges, ingredient_ids)`

- Counts how many IDs in `ingredient_ids` satisfy `is_fresh`.
- Used as the core of Part 1.

### `merge_ranges(ranges)`

- Takes a list of `(start, end)` ranges and merges them into a minimal set of **non-overlapping** inclusive ranges.
- Handles:
  - Overlapping ranges (e.g., `1-10` and `5-15` → `1-15`).
  - Adjacent ranges (e.g., `1-5` and `6-10` → `1-10` via `current_start <= last_end + 1`).
  - Unsorted input (it sorts by `start` first).
- Returns a new list of merged `(start, end)` tuples.

### `count_total_fresh_ids(ranges)`

- Uses `merge_ranges` to obtain a non-overlapping set of ranges.
- For each merged range `(start, end)`, adds `end - start + 1` to a running total.
- Returns the total number of distinct IDs considered fresh by the ranges.
- This is the core for Part 2.

## Part 1: Count fresh available IDs

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Call `parse_input(input_file)` to get `(ranges, ingredient_ids)`.
2. Call `count_fresh_ingredients(ranges, ingredient_ids)`.
3. Return the count.

For the example input, this yields `3` fresh IDs (5, 11, 17). For the actual `input.txt`, the Part 1 answer is **679**.

## Part 2: Count all IDs considered fresh by the ranges

Implementation: `solve_part2(input_file)`.

High-level approach:

1. Call `parse_input(input_file)` and take only `ranges`.
2. Call `count_total_fresh_ids(ranges)` to:
   - Merge overlapping/adjacent ranges.
   - Sum the sizes of the merged ranges.
3. Return this total.

For the example input, the merged ranges yield `3-5` and `10-20`, which together cover 14 IDs. For the actual `input.txt`, the Part 2 answer is **358155203664116**.

## Files

- `problem.txt` – Full text of the Day 5 puzzle (both parts) and example.
- `input.txt` – Puzzle input (fresh ranges, blank line, available IDs).
- `solution.py` – Python implementation with:
  - `parse_input(input_file)` – parses ranges and IDs.
  - `is_fresh(ingredient_id, ranges)` – checks if an ID is in any range.
  - `count_fresh_ingredients(ranges, ingredient_ids)` – counts how many available IDs are fresh.
  - `merge_ranges(ranges)` – merges overlapping/adjacent ranges.
  - `count_total_fresh_ids(ranges)` – counts all IDs covered by merged ranges.
  - `solve_part1(input_file)` – returns the Part 1 count.
  - `solve_part2(input_file)` – returns the Part 2 total.
- `test_solution.py` – Unit tests covering:
  - `is_fresh` on in-range, out-of-range, overlapping, boundary, and empty-range cases.
  - `count_fresh_ingredients` for all/none/some fresh IDs and large/adjacent/overlapping ranges.
  - `parse_input` and `solve_part1` using the example and real input (regression).
  - `merge_ranges` for no overlap, complete/partial overlap, adjacency, unsorted input, and single-value ranges.
  - `count_total_fresh_ids` for simple, overlapping, adjacent, empty, single-range, single-value, and large-value scenarios.
  - `solve_part2` for the example and real input (regression).
- `README.md` – This documentation.
