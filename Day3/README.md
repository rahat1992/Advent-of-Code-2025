# Day 3: Lobby – Battery Banks

This directory contains my solutions for **Advent of Code – Day 3: Lobby**.

The problem is described in `problem.txt` and involves powering an escalator using emergency batteries arranged into banks. Each battery has a single-digit joltage rating (`1`–`9`), and each **line of digits** in the input represents one **bank** of batteries.

Within each bank, you must turn on a fixed number of batteries such that, when read in order from left to right, the selected digits form the **largest possible number** (the bank’s joltage). Part 1 and Part 2 differ only in how many batteries you must turn on per bank.

## Input format

- The input file is `input.txt`.
- Each **line** corresponds to a single bank of batteries.
- Each bank is represented as a string of digits `1`–`9` with no separators, for example:

```text
987654321111111
811111111111119
234234234234278
818181911112111
```

Blank lines are ignored.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, where each bank uses exactly **2** batteries.
- Run **Part 2**, where each bank uses exactly **12** batteries.
- For each part, print:
  - The **total output joltage** (sum of maximum joltages across all banks).
  - The **number of banks** processed.

If you want to use a different input file, you can modify the `input_file` argument in the `__main__` block of `solution.py`.

## Core helper: selecting the best digits

Implementation: `find_max_joltage_n_batteries(bank, n)` in `solution.py`.

Given a bank represented as a string of digits (e.g. `"987654321111111"`) and a required count `n`, this function selects exactly `n` digits, **in order**, to form the largest possible number.

High-level greedy strategy:

1. Let `bank` be the string of digits and `n` the number of digits to select.
2. Maintain:
   - `result` – list of chosen digits (as characters).
   - `start_idx` – the earliest index we are allowed to choose from (initially `0`).
3. While `len(result) < n`:
   - Compute how many digits are still needed: `remaining_needed = n - len(result)`.
   - Compute the furthest index we can search from `start_idx` without running out of digits:
     - `max_end = len(bank) - remaining_needed + 1`.
   - Scan the range `[start_idx, max_end)` to find the **maximum digit** and remember the **leftmost** occurrence of that maximum.
   - Append that best digit to `result`.
   - Set `start_idx` to one past the chosen index so future choices stay in order.
4. After selecting `n` digits, join `result` into a string and convert to an integer.

This ensures that, at each step, you pick the best possible next digit while still leaving enough digits to complete the selection.

## Part 1: Two batteries per bank

In **Part 1**, you must turn on exactly **two** batteries in each bank. The joltage for a bank is the 2-digit number formed by those two selected digits.

Implementation:

- `find_max_joltage(bank)` – thin wrapper that calls `find_max_joltage_n_batteries(bank, 2)`.
- `solve_part1(input_file)` – applies this to every line in the input.

High-level approach in `solve_part1`:

1. Read all non-empty lines from `input_file` into `banks`.
2. For each `bank` in `banks`:
   - Compute `max_joltage = find_max_joltage(bank)`.
   - Accumulate `total_joltage += max_joltage`.
   - Append `max_joltage` to `max_joltages`.
3. Return `(total_joltage, max_joltages)`.

For the example in `problem.txt`, the maximum joltages per bank are `98`, `89`, `78`, and `92`, summing to `357`. For the actual puzzle input, the total output joltage is `17554`.

## Part 2: Twelve batteries per bank

In **Part 2**, you must turn on exactly **twelve** batteries in each bank. The joltage is now a 12-digit number formed by the selected digits.

Implementation:

- `solve_part2(input_file)` – reuses `find_max_joltage_n_batteries(bank, 12)` for each bank.

High-level approach in `solve_part2`:

1. Read all non-empty lines from `input_file` into `banks`.
2. For each `bank` in `banks`:
   - Compute `max_joltage = find_max_joltage_n_batteries(bank, 12)`.
   - Accumulate `total_joltage += max_joltage`.
   - Append `max_joltage` to `max_joltages`.
3. Return `(total_joltage, max_joltages)`.

For the example in `problem.txt`, the maximum 12-digit joltages per bank are `987654321111`, `811111111119`, `434234234278`, and `888911112111`, summing to `3121910778619`. For the actual puzzle input, the total output joltage is `175053592950232`.

## Files

- `problem.txt` – Full text of the Day 3 puzzle (both parts).
- `input.txt` – Puzzle input (each line is a bank of digit joltages).
- `solution.py` – Python implementation with:
  - `find_max_joltage_n_batteries(bank, n)` – core greedy selector for `n` digits.
  - `find_max_joltage(bank)` – convenience wrapper for `n = 2`.
  - `solve_part1(input_file)` – Part 1 solver (2 digits per bank).
  - `solve_part2(input_file)` – Part 2 solver (12 digits per bank).
- `test_solution.py` – Unit tests covering:
  - Example banks and total joltages from the problem statement.
  - Various edge cases for the selection logic (ascending, descending, repeated digits, mixed digits).
  - Optional regression checks against the real `input.txt` if present.
- `README.md` – This documentation.
