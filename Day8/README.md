# Day 8: Playground – Junction Box Circuits

This directory contains my solutions for **Advent of Code – Day 8: Playground**.

The problem is described in `problem.txt` and involves a set of electrical junction boxes suspended in 3D space. Each junction box has an `(X, Y, Z)` coordinate. The Elves want to connect pairs of junction boxes with strings of lights so that electricity can flow between them, forming **circuits** (connected components).

Part 1 asks you to connect the 1000 **closest pairs** of junction boxes (by straight-line distance), then compute the product of the sizes of the three largest circuits. Part 2 asks you to keep connecting the closest remaining pairs until all junction boxes belong to a single circuit, then compute the product of the X-coordinates of the **last two boxes** that needed to be connected.

## Input format

- The input file is `input.txt`.
- Each line contains a single junction box position as three comma-separated integers:

  ```text
  X,Y,F
  ```

  For example (from `problem.txt`):

  ```text
  162,817,812
  57,618,57
  906,360,560
  592,479,940
  ...
  ```

- There are no blank lines or headers; every non-empty line is a junction box.

In the example, the first box is at `(162, 817, 812)`, the second at `(57, 618, 57)`, and so on.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, building up to 1000 shortest connections and printing the product of the sizes of the three largest resulting circuits.
- Run **Part 2**, adding connections until all boxes are in a single circuit and printing the product of the X-coordinates of the last two boxes connected.

If you want to use a different input file or a different number of pairs for Part 1, you can pass a different `input_file` or `num_pairs` argument when calling `solve_part1` from Python.

## Core helpers

The implementation in `solution.py` uses standard graph and union–find (disjoint-set) techniques.

### `parse_junction_boxes(input_file)`

- Reads `input_file` line by line.
- Ignores empty lines.
- Splits each line on commas and converts the three fields to integers.
- Returns a list of `(x, y, z)` tuples.

### `distance(box1, box2)`

- Given two `(x, y, z)` tuples, computes the Euclidean distance between them:

  \[ d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2} \]

- Used to sort all possible pairs (edges) by length.

### `UnionFind` class

A classic **disjoint-set / union–find** data structure that tracks which boxes belong to which circuit.

- `__init__(n)`:
  - Initializes `n` separate sets (one per junction box), with:
    - `parent[i] = i`
    - `rank[i] = 0`
    - `size[i] = 1`
- `find(x)`:
  - Returns the representative (root) of the set containing `x`.
  - Uses **path compression** to flatten the tree.
- `union(x, y)`:
  - Joins the sets containing `x` and `y` using **union by rank**.
  - Updates `size[root]` of the new root to reflect the combined component size.
  - Returns `True` if it actually merged two different sets, `False` if they were already connected.
- `get_component_sizes()`:
  - Computes the size of each distinct component by calling `find(i)` for all `i` and reading the stored `size[root]`.
  - Returns a list of component sizes (e.g., `[5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]`).

## Part 1: Product of three largest circuits

Implementation: `solve_part1(input_file, num_pairs=1000)`.

High-level approach:

1. Parse all junction boxes with `parse_junction_boxes`.
2. Generate **all pairs** `(i, j)` of box indices (`0 ≤ i < j < n`) and compute their distances using `distance`.
3. Store these as edges `(dist, i, j)` and sort the list by `dist` ascending.
4. Initialize a `UnionFind` over `n` boxes.
5. For the first `num_pairs` edges (or all edges if there are fewer than `num_pairs`):
   - Call `uf.union(i, j)` to connect the boxes. If they are already in the same component, `union` returns `False` and the graph structure remains unchanged, but that pair is still counted as one of the attempted connections.
6. Call `uf.get_component_sizes()` to get all component sizes after these unions.
7. Sort the component sizes in descending order and multiply the top three:
   - If there are fewer than 3 components, multiply all of them.

In the example from `problem.txt`, after 10 connections, the component sizes are `5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1`, so the result is `5 * 4 * 2 = 40`. For the real `input.txt` with `num_pairs=1000`, the Part 1 answer is **42840**.

## Part 2: Product of X-coordinates of final connection

Implementation: `solve_part2(input_file)`.

High-level approach:

1. Parse all junction boxes with `parse_junction_boxes`.
2. Generate and sort all edges `(dist, i, j)` by distance as in Part 1.
3. Initialize a `UnionFind` over `n` boxes and set `num_components = n`.
4. Iterate over sorted edges:
   - For each edge `(dist, i, j)`, call `uf.union(i, j)`.
   - If `union` returns `True`, `i` and `j` were in different components, so:
     - Decrement `num_components`.
     - Record `last_connection = (i, j)`.
   - Stop when `num_components == 1`, meaning all boxes are in a single circuit.
5. Using `last_connection`, look up the corresponding junction boxes and extract their X-coordinates `x1` and `x2`.
6. Return `x1 * x2`.

In the example from `problem.txt`, the final connection that unifies all boxes is between `216,146,977` and `117,168,530`, so Part 2 returns `216 * 117 = 25272`. For the real `input.txt`, the Part 2 answer is **170629052**.

## Test coverage overview

The tests in `test_solution.py` exercise the key parts of the implementation:

- **Parsing & distances**:
  - `test_parse_junction_boxes` confirms correct parsing of basic input.
  - `test_parse_empty_file` checks empty-input handling.
  - `test_distance` and `test_distance_3d` validate 2D and 3D distance calculations.
- **Union–Find**:
  - `test_union_find_basic` checks `find` and `union` (including idempotent union).
  - `test_union_find_component_sizes` ensures correct component sizes for separate and merged sets.
  - `test_union_find_single_component` and `test_union_find_no_unions` cover extreme cases.
- **Part 1**:
  - `test_solve_part1_example` uses the example from `problem.txt` (10 connections → result 40).
  - `test_solve_part1_small` checks behavior on a very small 3-node example.
  - `test_actual_input_part1` asserts the real answer `42840` for `input.txt`.
- **Part 2**:
  - `test_solve_part2_example` uses the example from `problem.txt` and checks the final connection product `25272`.
  - `test_solve_part2_small` uses a small 3-node example and ensures the function returns an integer (and completes correctly).
  - `test_actual_input_part2` asserts the real answer `170629052` for `input.txt`.

Together, these tests cover:

- All core helpers (`parse_junction_boxes`, `distance`, `UnionFind` methods).
- The main control flow and stopping conditions in both `solve_part1` and `solve_part2`.
- Edge cases like empty input, no unions, already-connected pairs, small graphs, and the large real dataset.

## Files

- `problem.txt` – Full text of the Day 8 puzzle (both parts) and the example.
- `input.txt` – Puzzle input (all junction box coordinates).
- `solution.py` – Python implementation with the helpers and `solve_part1` / `solve_part2`.
- `test_solution.py` – Unit tests described above.
- `README.md` – This documentation.
