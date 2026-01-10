# Day 6: Trash Compactor – Cephalopod Math

This directory contains my solutions for **Advent of Code – Day 6: Trash Compactor**.

The problem is described in `problem.txt` and involves evaluating a cephalopod math worksheet. Problems are laid out in vertical stacks of digits, with the operator (`+` or `*`) on the bottom row, and different problems separated by a full column of spaces. In Part 2, the same worksheet is reinterpreted column-wise from right to left.

## Input format

- The input file is `input.txt`.
- It consists of several rows of characters forming a wide worksheet.
- All rows are the same width.
- The **last row** contains only the operators for each problem; each operator is either:
  - `*` – multiply all numbers in that problem.
  - `+` – add all numbers in that problem.
- Above the last row are one or more rows of digits and spaces.
- **Within a single problem**:
  - Each number is written on its own row in a vertical stack.
  - Numbers may be left- or right-aligned inside the problem’s column span; leading spaces are ignored.
- **Between problems**:
  - There is at least one full column consisting only of spaces (no digits, no operator).

Example (from `problem.txt`):

```text
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  
```

In Part 1, this corresponds to four problems:

- `123 * 45 * 6 = 33210`
- `328 + 64 + 98 = 490`
- `51 * 387 * 215 = 4243455`
- `64 + 23 + 314 = 401`

The **grand total** is the sum of all problem results.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, computing the grand total by interpreting problems as written left-to-right.
- Run **Part 2**, recomputing the grand total by interpreting problems right-to-left, with numbers read column-wise.

If you want to use a different input file, you can modify the `input_file` argument in the `__main__` block of `solution.py`.

## Core helpers

The implementation in `solution.py` is organized around parsing helpers and a shared problem solver.

### `parse_worksheet(input_file)` – Part 1 parser

- Reads all lines from `input_file`.
- Strips trailing blank lines.
- Treats the **last line** as the operations line and all preceding lines as number rows.
- Pads all lines to the same width.
- Scans left-to-right to find contiguous column spans representing individual problems:
  - A **problem span** is a run of columns that is not a full-space column in both the number rows and the operations row.
  - Full-space columns separate problems.
- For each problem span:
  - Reads each number row slice in that span, strips spaces, and converts non-empty slices to integers.
  - Extracts the corresponding operator (`+` or `*`) from the operations line (within the same span).
- Returns a list of `(numbers, operation)` tuples, where `numbers` is a list of integers and `operation` is `"+"` or `"*"`.

### `solve_problem(numbers, operation)` – shared evaluator

- Given a list of integers `numbers` and an operation `"+"` or `"*"`:
  - If `numbers` is empty, returns `0`.
  - Otherwise, reduces the list from left to right:
    - For `"*"`, multiplies all numbers.
    - For `"+"`, adds all numbers.
- Used by both Part 1 and Part 2.

### `parse_worksheet_rtl(input_file)` – Part 2 parser

Part 2 reinterprets the same worksheet **right-to-left**, with each **column** inside a problem treated as a separate number read top-to-bottom.

This function:

1. Reads and trims the input in the same way as `parse_worksheet` (last line = operators).
2. Pads all lines to the same width.
3. Identifies problem spans exactly as in Part 1.
4. For each problem span, processes **columns within that span from right to left**:
   - For each column `c` in the span (from `end_col-1` down to `start_col`):
     - Reads all non-space characters in that column from top to bottom across the number rows.
     - If any digits are present, concatenates them into a string and converts to an integer. This is one number in the problem.
   - Collects the resulting numbers into a list in right-to-left column order.
5. Extracts the operator by slicing the operations line over the span and stripping spaces.
6. Returns a list of `(numbers, operation)` tuples representing the right-to-left problems.

For the example:

- Rightmost problem: `4 + 431 + 623 = 1058`
- Second from right: `175 * 581 * 32 = 3253600`
- Third from right: `8 + 248 + 369 = 625`
- Leftmost: `356 * 24 * 1 = 8544`

The right-to-left grand total is `1058 + 3253600 + 625 + 8544 = 3263827`.

## Part 1: Grand total (left-to-right problems)

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Call `parse_worksheet(input_file)` to obtain all `(numbers, operation)` problems.
2. For each problem, call `solve_problem(numbers, operation)` to compute its result.
3. Sum all problem results into `grand_total`.
4. Return `grand_total`.

For the real `input.txt`, the Part 1 grand total is **5784380717354**.

## Part 2: Grand total (right-to-left column reading)

Implementation: `solve_part2(input_file)`.

High-level approach:

1. Call `parse_worksheet_rtl(input_file)` to obtain the reinterpretation of the worksheet as right-to-left column-based problems.
2. For each problem, call `solve_problem(numbers, operation)`.
3. Sum all results into `grand_total`.
4. Return `grand_total`.

For the real `input.txt`, the Part 2 grand total is **7996218225744**.

## Files

- `problem.txt` – Full text of the Day 6 puzzle (both parts), including the example worksheet and both grand totals.
- `input.txt` – Puzzle input (the full-width cephalopod math worksheet).
- `solution.py` – Python implementation with:
  - `parse_worksheet(input_file)` – parses Part 1 problems.
  - `solve_problem(numbers, operation)` – adds or multiplies a list of numbers.
  - `parse_worksheet_rtl(input_file)` – parses Part 2 problems using right-to-left, column-wise reading.
  - `solve_part1(input_file)` – returns the Part 1 grand total.
  - `solve_part2(input_file)` – returns the Part 2 grand total.
- `test_solution.py` – Unit tests covering:
  - `solve_problem` for various combinations (single, many, zeros, large values, `+` and `*`).
  - `parse_worksheet` on the example, alignment variants, spacing, and differing row counts.
  - `solve_part1` on the example, synthetic cases, and the real input (regression).
  - `parse_worksheet_rtl` on the Part 2 example and several tricky layouts (single-digit columns, multi-digit columns, different column heights).
  - `solve_part2` on the example, simple synthetic problems, and the real input (regression).
- `README.md` – This documentation.
