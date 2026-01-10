# Day 2: Gift Shop – Invalid Product IDs

This directory contains my solutions for **Advent of Code – Day 2: Gift Shop**.

The problem is described in `problem.txt` and involves a gift shop database containing ranges of product IDs. Some of these IDs are **invalid** according to pattern-based rules that change between Part 1 and Part 2.

Your goal is to scan all IDs in the given ranges, identify which ones are invalid under each part’s rules, and compute the sum of those invalid IDs.

## Input format

- The input file is `input.txt`.
- It contains a **single logical line** with a comma-separated list of **inclusive ranges**:
  - Each range is written as `start-end`, e.g. `11-22` or `95-115`.
  - Ranges are separated by commas (`,`), and the line may be wrapped across multiple physical lines for readability.

For example (wrapped here for legibility):

```text
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
```

Whitespace and newlines are tolerated as long as the `start-end` and comma structure is preserved.

## Running the solutions

From this directory:

```bash
python solution.py
```

This will:

- Run **Part 1** using the "exactly twice" invalid-ID rule.
- Run **Part 2** using the "at least twice" invalid-ID rule.
- For each part, print:
  - The **total sum** of invalid IDs.
  - The **number of invalid IDs** found.

If you want to use a different input file, you can modify the `input_file` argument in the `__main__` block of `solution.py`.

## Part 1: Pattern repeated exactly twice

In **Part 1**, an ID is invalid if it is made only of **some sequence of digits repeated exactly twice**. Examples of invalid IDs:

- `55` → `5` repeated twice.
- `6464` → `64` repeated twice.
- `123123` → `123` repeated twice.

IDs like `101`, `1234`, or `123456` are **not** invalid under Part 1.

Implementation: `is_invalid_id_part1(num)` in `solution.py`.

High-level logic for `is_invalid_id_part1`:

1. Convert the number to its decimal string: `num_str`.
2. If the length of `num_str` is **odd**, it cannot be two equal halves → return `False`.
3. Split the string into two halves: `first_half` and `second_half`.
4. Reject if `first_half` starts with `'0'` to avoid leading-zero artefacts (e.g. treating `0101` as `"01" + "01"`).
5. Return `True` if and only if `first_half == second_half`.

### Part 1 solver

Implementation: `solve_part1(input_file)`.

High-level approach:

1. **Parse ranges** from the input:
   - Read the entire file into a string and `.split(',')` on commas.
   - For each non-empty `range_str`, split on `'-'` to obtain `start` and `end`.
   - Convert `start` and `end` to integers and store as `(start, end)` tuples.
2. **Scan IDs** in each range:
   - Initialize `total = 0` and `invalid_ids = []`.
   - For each `(start, end)` and each `num` from `start` to `end` **inclusive**:
     - If `is_invalid_id_part1(num)` is `True`, append `num` to `invalid_ids` and add it to `total`.
3. **Return results** as `(total, invalid_ids)`.

The tests in `test_solution.py` verify the example ranges from `problem.txt` and confirm that the sum of invalid IDs for the example input is `1227775554`. For the full puzzle input, the Part 1 answer is `12850231731` with `807` invalid IDs.

## Part 2: Pattern repeated at least twice

In **Part 2**, the rule is generalized: an ID is invalid if it is made only of **some sequence of digits repeated at least twice** (two or more times). Examples of invalid IDs:

- `12341234` → `1234` repeated 2 times.
- `123123123` → `123` repeated 3 times.
- `1212121212` → `12` repeated 5 times.
- `1111111` → `1` repeated 7 times.

Part 2 **includes all** Part 1 invalid IDs (since "exactly twice" is a special case of "at least twice") and adds new ones such as:

- `111` → `1` repeated 3 times.
- `999` → `9` repeated 3 times.
- `565656` → `56` repeated 3 times.

Implementation: `is_invalid_id_part2(num)` in `solution.py`.

High-level logic for `is_invalid_id_part2`:

1. Convert the number to `num_str` and get `length`.
2. For every possible pattern length `pattern_len` from `1` to `length // 2`:
   - Skip if `length % pattern_len != 0` (the pattern must tile the entire string).
   - Let `pattern = num_str[:pattern_len]`.
   - Skip if `pattern` starts with `'0'` (to avoid leading-zero patterns).
   - Compute `repetitions = length // pattern_len`.
   - If `repetitions >= 2` and `pattern * repetitions == num_str`, then the number is invalid → return `True`.
3. If no such pattern is found, return `False`.

This detects both the simple "two halves" cases from Part 1 and more general repeated-pattern cases.

### Part 2 solver

Implementation: `solve_part2(input_file)`.

The structure mirrors `solve_part1`:

1. **Parse ranges** in the same way as Part 1.
2. **Scan IDs** in each range using `is_invalid_id_part2`.
3. **Return results** as `(total, invalid_ids)`.

The tests in `test_solution.py` verify that:

- The Part 2 example sum for the sample ranges is `4174379265`.
- For the full puzzle input, the Part 2 answer is `24774350322` with `889` invalid IDs.

## Files

- `problem.txt` – Full text of the Day 2 puzzle (both parts).
- `input.txt` – Puzzle input (comma-separated ranges of IDs).
- `solution.py` – Python implementation with:
  - `is_invalid_id_part1(num)` and `solve_part1(input_file)` for Part 1 rules.
  - `is_invalid_id_part2(num)` and `solve_part2(input_file)` for Part 2 rules.
- `test_solution.py` – Unit tests covering:
  - Core invalid-ID logic for both parts and multiple pattern lengths.
  - Behaviour over the example ranges and the full example input.
  - Optional validation against the actual `input.txt` if present.
- `README.md` – This documentation.
