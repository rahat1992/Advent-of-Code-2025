# Advent of Code – Playground of Puzzles

This repository contains a series of Advent of Code–style programming puzzles, implemented one per directory (`Day1/`, `Day2/`, ..., `DayN/`). Each day is self-contained: it has its own `problem.txt`, `input.txt`, `solution.py`, `test_solution.py`, and (for most days) a `README.md` with day-specific details.

All solutions are written in Python and use only the standard library.

## Running solutions and tests

From the repo root, each day is run the same way:

- Run a day's solution:
  - `cd DayN`
  - `python3 solution.py`
- Run a day's tests (using `unittest`):
  - `cd DayN`
  - `python3 -m unittest`

See each `DayN/README.md` for puzzle-specific notes, inputs, and examples.

---

## Day-by-day overview

Below is a high-level summary of each day's puzzle, the core algorithms or data structures involved, and how Part 1 and Part 2 relate.

### Day 1 – Secret Entrance (Dial rotations)

- **Theme:** Simulating a safe dial labeled `0..99` starting at position 50, rotated left (`L`) and right (`R`).
- **Part 1:**
  - For each rotation, update the dial position using modular arithmetic on a ring of size 100.
  - Count how many times the dial ends exactly on `0` after a rotation.
  - **Algorithm:** Simple simulation with modulo arithmetic (`(pos ± distance) % 100`); linear in number of rotations.
- **Part 2:**
  - Instead of only final positions, count *every* time the dial passes through `0` during a rotation.
  - Decompose each rotation into full 100-click cycles (each cycle guarantees exactly one pass through `0`) plus a partial segment that may or may not cross `0`.
  - **Algorithm:** Arithmetic reasoning with integer division and modulo; track full cycles (`distance // 100`) and a partial wrap condition depending on direction and current position.
- **Relationship:** Part 2 strictly generalizes Part 1’s logic: Part 1 cares only about final landings on `0`, while Part 2 counts all intermediate visits. Many tests cross-check behavior at boundaries (`49→99→0`, large distances, etc.).

### Day 2 – Gift Shop (Invalid Product IDs)

- **Theme:** Identifying “invalid” numeric IDs based on repeated digit patterns across ranges of integers.
- **Part 1:**
  - An ID is invalid if it is made of a digit sequence repeated **exactly twice** (e.g., `55`, `6464`, `123123`).
  - For each inclusive range `a-b`, scan all integers and apply a predicate `is_invalid_id_part1` based on string splitting into two equal halves.
  - **Algorithm:** String pattern check with length parity, half comparison, and a small leading-zero guard; linear over the size of ranges.
- **Part 2:**
  - An ID is invalid if it is made of some digit sequence repeated **at least twice** (e.g., `12341234`, `123123123`, `1111111`).
  - For each number, try all factorable pattern lengths and check whether the entire string is `pattern * k` with `k ≥ 2`.
  - **Algorithm:** Factor enumeration over string length, inner equality checks; strictly more general pattern matching that subsumes Part 1 IDs.
- **Relationship:** Part 2’s predicate is a superset of Part 1; all Part 1-invalid IDs remain invalid in Part 2. Part 2 extends the combinatorial search over pattern lengths and repetition counts.

### Day 3 – Lobby (Battery Banks)

- **Theme:** Each input line is a “bank” of digit batteries; you must select digits to form the largest possible number.
- **Part 1:**
  - For each bank (string of digits), choose exactly **two** digits, in order, that produce the lexicographically largest 2-digit number.
  - **Algorithm:** Greedy subsequence selection:
    - At each step, scan ahead only as far as needed so that enough digits remain.
    - Pick the best digit, move the start index, and repeat.
- **Part 2:**
  - Same as Part 1 but with **12** digits per bank instead of 2.
  - **Algorithm:** Same greedy subsequence selection generalized to arbitrary `n`; complexity remains linear per bank.
- **Relationship:** Part 2 reuses and stresses the same greedy routine for much larger selections, so correctness of the general `n`-digit selector is crucial.

### Day 4 – Printing Department (Paper Rolls)

- **Theme:** A 2D grid of paper rolls (`@`) and empty space (`.`). Rolls are “accessible” if they are not too crowded by neighbors.
- **Part 1:**
  - A roll is accessible if it has **fewer than 4** neighboring rolls among the 8 surrounding cells.
  - Count how many rolls are accessible in the initial grid.
  - **Algorithm:** 2D grid scan with an 8-neighbor adjacency count; purely local computation.
- **Part 2:**
  - Iteratively remove all currently accessible rolls (in batches) and re-evaluate accessibility until no more rolls are removable.
  - Sum the total number of removed rolls across all passes.
  - **Algorithm:** Repeated elimination / simulation on the grid; essentially a multi-pass “peeling” process (similar to layer-by-layer erosion or BFS from low-degree nodes).
- **Relationship:** Part 1 provides the core accessibility rule; Part 2 applies it iteratively as a dynamic process until reaching a fixed point.

### Day 5 – Cafeteria (Fresh Ingredients)

- **Theme:** Interpreting inclusive ID ranges as “fresh” ingredient IDs and checking availability.
- **Part 1:**
  - Input has two sections: fresh ranges, then available IDs.
  - An ID is fresh if it falls in *any* fresh range.
  - Count how many of the available IDs are fresh.
  - **Algorithm:** Range-membership checks via a linear scan over ranges for each ID; straightforward but potentially large.
- **Part 2:**
  - Ignore available IDs; count how many **distinct IDs** are fresh across all ranges.
  - Merge overlapping and adjacent ranges into disjoint intervals and sum their lengths.
  - **Algorithm:** Interval merging (sort by start, then merge where `current_start <= last_end + 1`) and length aggregation.
- **Relationship:** Part 2 abstracts Part 1’s membership logic into range merging and counting, avoiding double-counting overlaps. Part 1 is effectively a sampling problem; Part 2 is an exact combinatorial count.

### Day 6 – Trash Compactor (Cephalopod Math)

- **Theme:** Evaluating vertically-arranged math problems on a worksheet; operations (`+` or `*`) sit at the bottom row.
- **Part 1:**
  - Each problem is a vertical stack of decimal numbers, with the operator at the bottom.
  - Problems are separated by full columns of spaces; numbers within a problem may be left- or right-aligned.
  - Parse each problem, then evaluate `sum` or `product` over its numbers.
  - **Algorithm:**
    - 2D text parsing: treat the input as a fixed-width matrix, segment problems by columns.
    - For each problem region, trim each row slice to derive integers and apply simple reduction.
- **Part 2:**
  - Same physical worksheet, but now **read right-to-left**: each column in a problem corresponds to a separate number, read top-to-bottom.
  - Parse per-column numbers within each problem from rightmost column to leftmost; evaluation per problem is still `+` or `*`.
  - **Algorithm:**
    - Reinterpret the same matrix: scan problem spans as before, but iterate columns from right to left and vertically collect digits into numbers.
- **Relationship:** Part 2 shares the same underlying representation and operations but changes the *interpretation* of the columns. Parsing is the main difference; evaluation is shared via a common `solve_problem` helper.

### Day 7 – Laboratories (Tachyon Manifold)

- **Theme:** A vertical beam of tachyons moving through a grid containing splitters (`^`) and empty space (`.`) from a starting cell `S`.
- **Part 1:**
  - Classical beams move downward; upon hitting a splitter, the incoming beam stops and two new beams emerge immediately left and right.
  - Count how many **split events** occur (each splitter cell only counted once, even if multiple beams hit it later).
  - **Algorithm:**
    - Multi-beam simulation: track active beam positions, step rows downward.
    - Use a set of already-split positions to avoid double-counting.
- **Part 2:**
  - Quantum many-worlds interpretation: a single particle branches at each splitter into left and right paths; you must count how many **timelines** the particle can end up in.
  - **Algorithm:** Dynamic programming over the grid:
    - Maintain a map from `(row, col)` to number of paths arriving there.
    - At each step, distribute path counts to child cells (straight, left, right) depending on content.
    - Sum all paths that exit beyond the bottom row.
- **Relationship:** Part 1 and Part 2 share the same geometry and splitter semantics, but Part 1 tracks unique **split locations**, while Part 2 tracks the **multiplicity of paths** via DP. Conceptually, Part 2 is “Part 1 + counting all quantum branches.”

### Day 8 – Playground (Junction Box Circuits)

- **Theme:** A set of junction boxes in 3D space; you connect pairs in order of increasing Euclidean distance, building circuits (connected components).
- **Part 1:**
  - Consider all pairwise connections, sorted by straight-line distance.
  - Attempt to connect the 1000 closest pairs using union–find; some connections may be redundant if boxes are already in the same circuit.
  - After these attempts, compute the product of sizes of the **three largest circuits**.
  - **Algorithm:**
    - All-pairs distance computation (complete graph edges) + sorting.
    - Disjoint-set union (Union-Find) to maintain components and their sizes.
- **Part 2:**
  - Continue connecting boxes by increasing distance until there is **one** circuit containing all boxes.
  - Record the last successful union; return the product of the **X-coordinates** of the two boxes in that last connection.
  - **Algorithm:** Same edge list and union–find structure as Part 1; stop condition changes to `num_components == 1` and we read coordinates from the final edge.
- **Relationship:** Algorithmically, it’s essentially one Kruskal-like pass over edges. Part 1 stops early after a fixed number of attempts and inspects component sizes; Part 2 runs until full connectivity and inspects the final edge.

### Day 9 – Movie Theater (Red & Green Rectangles)

- **Theme:** Red tiles form a simple rectilinear polygonal loop on a grid; in Part 2, red tiles are connected by green tiles along edges and all interior tiles are green. Rectangles must use red tiles as opposite corners.
- **Part 1:**
  - Given only the set of red tiles, find the largest axis-aligned rectangle whose opposite corners are red tiles.
  - The interior may be any color; only corners are constrained.
  - **Algorithm:**
    - Brute-force all unordered pairs of red tiles as opposite corners.
    - Compute discrete area as `(abs(dx) + 1) * (abs(dy) + 1)` and keep the maximum.
- **Part 2:**
  - Now, every tile inside the chosen rectangle must be **red or green**.
  - Red tiles form the vertices of a rectilinear loop; green tiles lie on edges and throughout the interior of this loop.
  - **Algorithm:**
    - Polygon processing and range compression:
      - Extract horizontal and vertical segments from consecutive red tiles.
      - For each relevant row `y`, compute valid x-ranges where tiles are inside or on the boundary (using segment info plus point-in-polygon checks).
      - Precompute these ranges for all “bands” of rows between red y-coordinates.
    - For each pair of red tiles defining a candidate rectangle:
      - Quickly test validity with `is_rectangle_valid_fast`, sampling at critical rows and band representatives to ensure the entire rectangle lies within the red/green region.
      - Track the maximum area that passes this test.
- **Relationship:** Part 1 is purely combinatorial over corners; Part 2 adds a **geometric feasibility** constraint that relies on understanding the red polygon’s shape and its interior. The same corner enumeration is used; Part 2 layers in geometry and range-checking to filter out invalid rectangles.

---

## Extending the repository

New days follow the same pattern:

1. Create a directory `DayN/`.
2. Add:
   - `problem.txt` – the full puzzle statement.
   - `input.txt` – your puzzle input.
   - `solution.py` – functions `solve_part1(input_file)` and `solve_part2(input_file)` (if applicable), plus helpers.
   - `test_solution.py` – `unittest`-based tests covering core helpers, examples from the problem, and regression checks against `input.txt`.
   - `README.md` – a short description of the puzzle, approach, and how to run it.
3. Prefer small, composable helpers whose behavior is unit-tested independently of I/O.

See the existing days (especially Days 1–9) for concrete patterns to reuse.