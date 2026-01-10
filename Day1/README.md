# Day 1: Secret Entrance

This directory contains my solutions for **Advent of Code - Day 1: Secret Entrance**.

The problem is described in `problem.txt` and involves a safe with a dial labeled `0` through `99`. The dial starts at `50`, and a sequence of rotations (each starting with `L` or `R` followed by a distance) is applied.

- Rotating **left** (`L`) moves the dial toward lower numbers, wrapping from `0` back to `99`.
- Rotating **right** (`R`) moves the dial toward higher numbers, wrapping from `99` back to `0`.

The puzzle has two parts, both solved in `solution.py`.

## Input format

- The input file is `input.txt`.
- Each line contains a single rotation instruction, for example:
  - `L68`
  - `R5`
  - `L30`
- Blank lines are ignored.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:
- Print the answer for **Part 1** (original password method).
- Print the answer for **Part 2** (method `0x434C49434B`).

If you want to use a different input file, you can modify the `input_file` argument in the `__main__` block of `solution.py`.

## Part 1: Ending on zero

**Goal:** Count how many times the dial is left **pointing at `0` after a rotation**.

Implementation: `solve_part1(input_file)` in `solution.py`.

High-level approach:

1. Read all rotation instructions from the input file.
2. Start the dial at position `50`.
3. For each rotation:
   - Extract the direction (`L` or `R`).
   - Parse the distance (number of clicks).
   - Update the position using modular arithmetic on a 0–99 range:
     - `L`: `(position - distance) % 100`
     - `R`: `(position + distance) % 100`
   - If the new `position` is `0`, increment a counter.
4. Return the counter as the Part 1 answer.

This matches the Part 1 story: you only care about times when the dial is **left** at `0` after finishing a described rotation.

## Part 2: Counting every click through zero

**Goal:** Using password method `0x434C49434B`, count **every time any click causes the dial to point at `0`**, whether it happens **during** a rotation or **at the end**.

Implementation: `solve_part2(input_file)` in `solution.py`.

Key idea: For each rotation, instead of only checking the final position, we count how many times the dial passes through `0` while it moves, plus any time it ends exactly on `0`.

The dial is still on a 0–99 circle, so: 
- A movement of `100` clicks corresponds to one full revolution, meaning the dial points at `0` exactly once per full cycle.
- Larger distances can include multiple full cycles.

High-level approach:

1. Read all rotation instructions from the input file.
2. Start the dial at position `50` and set a `count_zeros` counter to `0`.
3. For each rotation:
   - Extract direction and distance.
   - Compute the number of **full 100-click cycles** in this rotation:
     - `full_cycles = distance // 100`
     - Each full cycle guarantees exactly one time the dial points at `0`, so add `full_cycles` to `count_zeros`.
   - Handle the **remaining clicks** (`remaining = distance % 100`) to see if we cross `0` in the partial movement:
     - For `L` (moving left/decreasing): if `remaining > position`, we must wrap past `0` during this partial movement, so increment `count_zeros` once.
     - For `R` (moving right/increasing): if `position + remaining >= 100`, we wrap past `99` back to `0`, so increment `count_zeros` once.
   - Update `position` to the final dial value after the rotation using modulo 100.
4. After processing all rotations, return `count_zeros`.

Why this works:
- Every group of 100 clicks (in either direction) is exactly one full loop around the dial, so it hits `0` once.
- The logic for the remainder handles whether the partial movement crosses the `0` boundary once more.
- If a rotation ends exactly on `0`, that crossing is naturally included by the same counting logic, consistent with the problem description and examples.

## Files

- `problem.txt` – Full text of the Day 1 puzzle (both parts).
- `input.txt` – Puzzle input (sequence of rotations).
- `solution.py` – Python implementation solving Part 1 and Part 2.
- `README.md` – This documentation.
