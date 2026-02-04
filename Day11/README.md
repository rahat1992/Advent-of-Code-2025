# Day 11: Reactor – Path Counting in a Device Graph

This directory contains my solutions for **Advent of Code – Day 11: Reactor**.

The problem is described in `problem.txt` and involves tracing data paths through a network of electrical devices connecting a server rack to a toroidal reactor. Each device has named outputs leading to other devices, forming a directed acyclic graph.

## Input format

- The input file is `input.txt`.
- Each line describes a single device and its outputs:

```text
device_name: output1 output2 ...
```

Example (from `problem.txt`, Part 1):

```text
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
```

- Device names are short alphabetic strings.
- Data flows only from a device through its outputs (edges are directed).
- The graph is acyclic, so paths always terminate.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, printing the number of distinct paths from `you` to `out`.
- Run **Part 2**, printing the number of paths from `svr` to `out` that visit both `dac` and `fft`.

## Core helpers

### Parsing

- `parse_input(input_file)`:
  - Reads each non-empty line and splits on `': '` to extract the device name and its space-separated list of output devices.
  - Returns a dictionary mapping each device name to its list of outputs.

### Path counting

- `count_paths(graph, start, end)`:
  - Counts all distinct paths from `start` to `end` using recursive DFS.
  - Memoized with `@lru_cache`: each node's path count is computed once and reused.
  - Base cases: returns `1` at the `end` node, `0` if the node has no outgoing edges.

- `count_paths_through_required(graph, start, end, required_nodes)`:
  - Counts paths from `start` to `end` that visit **all** nodes in `required_nodes`.
  - Tracks which required nodes have been seen using a `frozenset` as part of the memoization state `(node, visited_required)`.
  - A path is only counted if `visited_required == required_set` when it reaches `end`.

## Part 1: Count all paths from `you` to `out`

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Parse the device graph.
2. Call `count_paths(graph, 'you', 'out')` to count all distinct directed paths.

For the example in `problem.txt`, the 5 paths are:

- `you -> bbb -> ddd -> ggg -> out`
- `you -> bbb -> eee -> out`
- `you -> ccc -> ddd -> ggg -> out`
- `you -> ccc -> eee -> out`
- `you -> ccc -> fff -> out`

**Algorithm:** DFS with memoization on a DAG. Time complexity is O(V + E) since each node is visited once and each edge is traversed once during the recursive expansion.

## Part 2: Count paths from `svr` to `out` through `dac` and `fft`

Implementation: `solve_part2(input_file)`.

High-level approach:

1. Parse the device graph.
2. Call `count_paths_through_required(graph, 'svr', 'out', ['dac', 'fft'])`.
3. Only paths that pass through **both** `dac` (digital-to-analog converter) and `fft` (fast Fourier transform) are counted.

For the Part 2 example, out of 8 total paths from `svr` to `out`, only **2** visit both `dac` and `fft`:

- `svr -> aaa -> fft -> ccc -> eee -> dac -> fff -> ggg -> out`
- `svr -> aaa -> fft -> ccc -> eee -> dac -> fff -> hhh -> out`

**Algorithm:** DFS with memoization keyed on `(node, visited_required)`. The `visited_required` frozenset has at most `2^k` states where `k` is the number of required nodes (here `k = 2`, so 4 states per node). Overall complexity is O((V + E) * 2^k).

## Tests

`Day11/test_solution.py` provides coverage for both parts:

- `test_parse_input` – verifies the graph dictionary matches expected adjacency lists.
- `test_count_paths_simple` – single linear path `a -> b -> c -> end` yields 1 path.
- `test_count_paths_branching` – branching graph `a -> {b, c} -> end` yields 2 paths.
- `test_solve_part1_example` – validates 5 paths for the Part 1 example.
- `test_count_paths_through_required` – confirms 8 total paths from `svr` to `out` in the Part 2 example graph.
- `test_solve_part2_example` – validates 2 paths through both `dac` and `fft`.
- `test_actual_input_part1` / `test_actual_input_part2` – regression tests against the real `input.txt`.

## Files

- `problem.txt` – Full text of the Day 11 puzzle (both parts) and examples.
- `input.txt` – Puzzle input (one device per line).
- `solution.py` – Python implementation of parsing and both Part 1 (DFS with memoization) and Part 2 (DFS with required-node tracking) solvers.
- `test_solution.py` – Unit tests for the parser, path counting helpers, and both parts.
- `README.md` – This documentation.
