# Day 10: Factory – Indicator Lights & Joltages

This directory contains my solutions for **Advent of Code – Day 10: Factory**.

The problem is described in `problem.txt` and involves configuring a set of factory machines. Each machine has:

- A row of **indicator lights** that must match a target on/off pattern (Part 1).
- A set of **buttons**, each of which toggles some lights and, in a different mode, increments some **joltage counters** (Part 2).
- A list of **joltage requirements** that the counters must match exactly (Part 2).

Your job is to minimize the total number of button presses needed to satisfy all machines in both modes.

## Input format

- The input file is `input.txt`.
- Each non-empty line describes a **single machine** in three parts:
  - An **indicator light diagram** in square brackets `[...]`.
  - One or more **button wiring schematics** in parentheses `(…)`.
  - A list of **joltage requirements** in curly braces `{...}`.

Example (from `problem.txt`):

```text
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

- The indicator diagram uses:
  - `.` for an **off** light.
  - `#` for an **on** light.
- Each button wiring schematic `(i,j,k,...)` lists the **0-based indices** of the lights (Part 1) or counters (Part 2) that button affects.
  - In **indicator mode** (Part 1), pressing a button flips the state of each listed light.
  - In **joltage mode** (Part 2), pressing a button increments each listed counter by 1.
- Joltage values in `{}` are ignored in Part 1 but are the targets in Part 2.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, printing the minimum total number of button presses needed to configure all indicator lights.
- Run **Part 2**, printing the minimum total button presses needed to reach all joltage targets.

Note: the provided implementation for Part 2 is exact but can be slow on the full puzzle input; the corresponding regression test is skipped by default.

## Core helpers

### Parsing

- `parse_line(line)`:
  - Uses regular expressions to extract:
    - The indicator diagram between `[` and `]`.
    - All button wiring schematics between `(` and `)`.
    - The joltage requirements between `{` and `}`.
  - Converts the diagram into a list of booleans `target_state` (True for `#`, False for `.`).
  - Converts each button into a `set` of indices indicating which lights/counters it affects.
  - Converts joltage requirements into a list of integers.
  - Returns `(target_state, buttons, num_lights, joltage_targets)`.
- `parse_input(input_file)`:
  - Reads each non-empty line from the input file and parses it with `parse_line`.
  - Returns a list of machines.

### State and button encoding (Part 1)

- `apply_buttons(num_lights, buttons, pressed)`:
  - Applies a given set of button presses to an initial all-off indicator state.
  - `pressed` is a Boolean list over buttons; for each `True` entry, toggles the corresponding lights.
  - Returns the resulting light state as a list of booleans.
- `state_to_int(state)`:
  - Encodes a list of booleans (lights) into an integer bitmask for efficient state tracking.
- `button_to_int(button_set, num_lights)`:
  - Encodes a set of light indices into a bitmask representing which bits (lights) it toggles.

### Search / DP for minimal presses (Part 1)

Because toggling is modulo 2, pressing a button twice cancels out. Each button only needs to be considered as pressed 0 or 1 times. The problem reduces to finding a subset of buttons whose XOR of toggled lights equals the target pattern, minimizing the number of buttons selected.

Several solvers are provided (some for experimentation):

- `find_min_presses_brute_force(target_state, buttons, num_lights)`:
  - Tries **all subsets** of buttons using `itertools.combinations`, ordered by increasing subset size.
  - Applies the chosen buttons and checks if the final state matches the target.
  - Guaranteed minimal solution but exponential in the number of buttons; used only for small cases.
- `find_min_presses_bitmask(target_state, buttons, num_lights)`:
  - Encodes light states and buttons as bitmasks.
  - Performs a BFS over `(light_state, button_index)` pairs, choosing whether to press or skip each button.
  - Tracks the fewest presses seen per state using a dictionary `best`.
- `find_min_presses_dp(target_state, buttons, num_lights)` (primary method):
  - Uses dynamic programming over buttons:
    - `dp` is a dictionary mapping `state` → minimum presses.
    - For each button, build a new dictionary by considering two transitions from every previous state:
      - **Skip button**: keep the same state with the same press count.
      - **Press button**: XOR the button’s bitmask into the state and increment the press count.
  - After processing all buttons, `dp[target]` holds the minimum number of presses required.
  - This is the method used by `solve_part1`.

## Part 1: Minimum total button presses (indicator lights)

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Parse all machines via `parse_input`.
2. For each machine `(target_state, buttons, num_lights, _joltage_targets)`:
   - Run `find_min_presses_dp` to get the minimum number of presses for that machine.
   - Sum these minimums across all machines.
3. Return the total.

For the example in `problem.txt`:

- Machine 1 can be solved in **2** presses.
- Machine 2 can be solved in **3** presses.
- Machine 3 can be solved in **2** presses.

Total: `2 + 3 + 2 = 7`.

## Part 2: Minimum total button presses (joltage counters)

In Part 2, the indicator diagrams are ignored. Each machine has a vector of joltage requirements, and pressing a button increments a subset of these counters by 1. You can press buttons any non-negative integer number of times. The goal is to reach the exact joltage targets with the fewest total presses.

Mathematically, for each machine this is an **integer linear system**:

- Let `x_j` be the number of times you press button `j`.
- Let `A[i][j]` be 1 if button `j` affects counter `i`, else 0.
- Let `b[i]` be the target joltage for counter `i`.
- You must find `x ≥ 0` such that `A x = b` and `sum(x_j)` is minimized.

The implementation uses several layers of solvers:

- `solve_linear_system_min_sum(A, b)`:
  - Performs Gaussian elimination over rational numbers (`fractions.Fraction`) to obtain the general solution of `A x = b`.
  - If there are no free variables, checks that the unique solution is a vector of non-negative integers and returns its sum.
  - If there are free variables, searches over a bounded space of integer assignments to minimize the total number of button presses.
  - Falls back to a heuristic search when the space of free variables is too large.
- `find_min_joltage_heuristic_search(A, b)`:
  - Greedy search in the space of counters: at each step, choose the button that makes the most progress toward the target without overshooting.
- `find_min_joltage_presses_exact(buttons, joltage_targets)` / `find_min_joltage_presses_greedy(...)`:
  - Build the matrix `A` from the button definitions and call the linear solver.
- `find_min_joltage_presses_dp(buttons, joltage_targets)`:
  - An alternative BFS/DP over counter states (exact but only feasible for very small targets).

The main Part 2 solver is:

- `solve_part2(input_file)`:
  - Parses all machines.
  - For each `(target_state, buttons, num_lights, joltage_targets)` (ignoring `target_state` and `num_lights`):
    - Computes the minimum number of button presses needed to reach `joltage_targets` using the linear-algebra-based solver.
  - Sums these minima across all machines.

The example from `problem.txt` yields a total of **33** presses across the three machines.

## Tests

`Day10/test_solution.py` provides coverage for both parts:

- `test_parse_line_machine*` – parsing of each of the three example machines, including light patterns, buttons, and joltage targets.
- `test_apply_buttons` – correctness of toggle logic and repeated-press behavior for lights.
- `test_state_to_int` / `test_button_to_int` – correctness of bitmask encoding for the Part 1 DP.
- `test_find_min_presses_machine*` – checks that the DP-based solver finds the expected minimal press count for each example machine.
- `test_solve_part1_example` – validates total of 7 presses for the three-machine example input.
- `test_solve_part1_*` – small sanity checks for trivial machines (single button, zero presses needed).
- `test_solve_part2_example` – verifies that Part 2 yields 33 presses for the example.
- `test_actual_input_part2` – regression test for the real `input.txt`, skipped by default because it can take several minutes.

## Files

- `problem.txt` – Full text of the Day 10 puzzle (both parts) and examples.
- `input.txt` – Puzzle input (one machine per line).
- `solution.py` – Python implementation of parsing and both Part 1 (bitmask DP) and Part 2 (integer linear system) solvers.
- `test_solution.py` – Unit tests for the parser, helpers, and both parts (with the heavy Part 2 regression test skipped by default).
- `README.md` – This documentation.
