# Day 10: Factory – Indicator Light Initialization

This directory contains my solutions for **Advent of Code – Day 10: Factory**.

The problem is described in `problem.txt` and involves initializing a set of factory machines. Each machine has a row of indicator lights and a collection of buttons. Pushing a button toggles specific lights on or off. The goal is to determine the minimum number of button presses needed to reach a desired pattern of lights.

## Input format

- The input file is `input.txt`.
- Each non-empty line describes a **single machine** in three parts:
  - An **indicator light diagram** in square brackets `[...]`.
  - One or more **button wiring schematics** in parentheses `(…)`.
  - A list of **joltage requirements** in curly braces `{...}` (which can be ignored).

Example (from `problem.txt`):

```text
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

- The indicator diagram uses:
  - `.` for an **off** light.
  - `#` for an **on** light.
- Each button wiring schematic `(i,j,k,...)` lists the **0-based indices** of the lights that button toggles.
  - Pressing a button flips the state of each listed light.
  - Pressing the same button twice cancels out (so effectively each button is either pressed 0 or 1 times).
- Joltage values in `{}` are present but not used for the logic of Part 1.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, printing the minimum total number of button presses needed to configure all machines.
- Run **Part 2**, which is currently a stub (returns `0` until the actual Part 2 puzzle is implemented).

## Core helpers

### Parsing

- `parse_line(line)`:
  - Uses regular expressions to extract:
    - The indicator diagram between `[` and `]`.
    - All button wiring schematics between `(` and `)`.
  - Converts the diagram into a list of booleans `target_state` (True for `#`, False for `.`).
  - Converts each button into a `set` of indices indicating which lights it toggles.
  - Returns `(target_state, buttons, num_lights)`.
- `parse_input(input_file)`:
  - Reads each non-empty line from the input file and parses it with `parse_line`.
  - Returns a list of machines.

### State and button encoding

- `apply_buttons(num_lights, buttons, pressed)`:
  - Applies a given set of button presses to an initial all-off state.
  - `pressed` is a Boolean list over buttons; for each `True` entry, toggles the corresponding lights.
  - Returns the resulting light state as a list of booleans.
- `state_to_int(state)`:
  - Encodes a list of booleans (lights) into an integer bitmask for efficient state tracking.
- `button_to_int(button_set, num_lights)`:
  - Encodes a set of light indices into a bitmask representing which bits (lights) it toggles.

### Search / DP for minimal presses (Part 1)

Because pressing a button twice cancels out, each button only needs to be considered as pressed 0 or 1 times. The problem reduces to finding a subset of buttons whose XOR of toggled lights equals the target pattern, minimizing the number of buttons selected.

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
  - Also uses bitmasks but interprets the process as dynamic programming over buttons:
    - `dp` is a dictionary mapping `state` → minimum presses.
    - For each button, `dp` is updated to a new dictionary `new_dp` via two transitions per prior state:
      - **Skip button**: keep the same state with the same press count.
      - **Press button**: XOR the button’s bitmask into the state and increment the press count.
  - After processing all buttons, `dp[target]` holds the minimum number of presses required.
  - This is the method used by `solve_part1`.

## Part 1: Minimum total button presses

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Parse all machines via `parse_input`.
2. For each machine `(target_state, buttons, num_lights)`:
   - Run `find_min_presses_dp` to get the minimum number of presses for that machine.
   - Sum these minimums across all machines.
3. Return the total.

For the example in `problem.txt`:

- Machine 1 can be solved in **2** presses.
- Machine 2 can be solved in **3** presses.
- Machine 3 can be solved in **2** presses.

Total: `2 + 3 + 2 = 7`.

The tests in `test_solution.py` also run Part 1 on the real `input.txt` and assert that the result is a positive integer.

## Part 2

At the moment, `solve_part2` is a placeholder and always returns `0`. The actual Part 2 puzzle has not yet been implemented.

## Tests

`Day10/test_solution.py` provides good coverage for the current implementation:

- `test_parse_line_machine*` – parsing of each of the three example machines.
- `test_apply_buttons` – correctness of toggle logic and repeated-press behavior.
- `test_state_to_int` / `test_button_to_int` – correctness of bitmask encoding.
- `test_find_min_presses_machine*` – checks that the DP-based solver finds the expected minimal press count for each example machine.
- `test_solve_part1_example` – validates total of 7 presses for the three-example input.
- Additional small scenarios (single button, no presses needed, real `input.txt`) to ensure robustness.

## Files

- `problem.txt` – Full text of the Day 10 puzzle (Part 1) and examples.
- `input.txt` – Puzzle input (one machine per line).
- `solution.py` – Python implementation of parsing and Part 1 solver (DP/bitmask), with a stub for Part 2.
- `test_solution.py` – Unit tests for the parser, helpers, DP solver, and Part 1.
- `README.md` – This documentation.
