# Day 9: Movie Theater – Red & Green Rectangles

This directory contains my solutions for **Advent of Code – Day 9: Movie Theater**.

The problem is described in `problem.txt` and involves a large grid of floor tiles in a movie theater. Some tiles are **red**; in Part 2, some tiles are also **green**. The Elves want to find the biggest axis-aligned rectangle you can place on the floor such that:

- The two opposite corners of the rectangle are red tiles.
- In Part 1, everything inside the rectangle can be any color.
- In Part 2, every tile inside the rectangle must be **red or green**.

The goal is to find the maximum possible **area** (in tiles) of such a rectangle.

## Input format

- The input file is `input.txt`.
- Each line contains a single red tile position as two comma-separated integers:

  ```text
  X,Y
  ```

  For example (from `problem.txt`):

  ```text
  7,1
  11,1
  11,7
  9,7
  9,5
  2,5
  2,3
  7,3
  ```

- Coordinates are given in the same coordinate system used in the problem diagrams (X = column, Y = row).
- The list describes **red** tiles. In Part 2, these red tiles are connected by straight horizontal/vertical segments of green tiles.

## Running the solutions

From this directory:

```bash
python3 solution.py
```

This will:

- Run **Part 1**, printing the largest rectangle area using any tiles (red corners only).
- Run **Part 2**, printing the largest rectangle area where all tiles are either red or green.

If you want to use a different input file, you can modify the `input_file` argument in the `__main__` block of `solution.py`.

## Core helpers

The implementation in `solution.py` separates geometry helpers (polygon, segments, range computations) from the rectangle search logic.

### `parse_red_tiles(input_file)`

- Reads `input_file` line by line.
- Ignores empty lines.
- Splits each line on `","` and converts the two fields to integers.
- Returns a list of `(x, y)` tuples, one for each red tile.

### `calculate_rectangle_area(tile1, tile2)`

- Given two `(x, y)` coordinates, returns the **continuous** geometric area of the rectangle that uses those points as opposite corners:

  ```python
  width = abs(x2 - x1)
  height = abs(y2 - y1)
  return width * height
  ```

- This helper is mostly used in tests; the actual puzzle uses **discrete tile counts**, which are handled directly in the solvers.

### Point-in-polygon and green tiles (Part 2 support)

- `is_point_inside_polygon(x, y, vertices)`:
  - Implements the classic **ray casting** algorithm to determine if a point lies strictly inside the polygon defined by the red tiles (treated in order as vertices of a rectilinear loop).
- `get_green_tiles(red_tiles)`:
  - For small examples, builds the full set of green tiles by:
    - Filling all horizontal/vertical edges connecting consecutive red tiles (including the wrap from last to first).
    - Then filling all interior points `(x, y)` within the bounding box that satisfy `is_point_inside_polygon(x, y, red_tiles)`.
  - Returns a set of `(x, y)` tiles that are either on the boundary or inside the red loop.
  - This is useful for validating the Part 2 logic on the example.

### Segment extraction

These functions summarize the polygon boundary as horizontal and vertical segments for more efficient range computations:

- `build_horizontal_segments(red_tiles)`:
  - Scans edges between consecutive red tiles and collects those with constant `y`.
  - Returns a list of `(y, x_start, x_end)` tuples.
- `build_vertical_segments(red_tiles)`:
  - Similarly, collects edges with constant `x`.
  - Returns a list of `(x, y_start, y_end)` tuples.

### Row-wise valid ranges

To efficiently determine which tiles are red-or-green at a given `y`, the solution uses these functions:

- `compute_valid_ranges_at_y(y, vertical_segments, horizontal_segments, red_tiles)`:
  - For a fixed row `y`, builds a list of **valid x-ranges** `(x_start, x_end)` such that every `(x, y)` in those ranges is either:
    - On a boundary segment, or
    - Strictly inside the polygon.
  - Uses:
    - Horizontal segments at that `y`.
    - Vertical segments spanning that `y`.
    - Interior checks via `is_point_inside_polygon` between critical x-values.
  - Merges overlapping/adjacent ranges into minimal intervals.
- `compute_y_bands(red_tiles, vertical_segments, horizontal_segments)`:
  - Identifies **critical y-coordinates** where the polygon changes shape (the y-values of red tiles).
  - For each critical y (and interior rows between them), precomputes `compute_valid_ranges_at_y`.
  - Returns:
    - `row_ranges`: a dict mapping each relevant `y` to its list of valid `(x_start, x_end)` ranges.
    - `critical_ys`: the sorted list of critical y-coordinates.
- `is_rectangle_valid_fast(min_x, max_x, min_y, max_y, row_ranges, critical_ys)`:
  - Checks whether a rectangle is fully covered by the red/green region by sampling only **critical y-rows** plus one representative interior row per band.
  - For each sampled `y`, ensures `[min_x, max_x]` lies entirely within one of the valid ranges in `row_ranges[y]`.

## Part 1: Largest rectangle (red corners only)

Implementation: `solve_part1(input_file)`.

High-level approach:

1. Use `parse_red_tiles(input_file)` to get all red tile coordinates.
2. For each unordered pair of red tiles `(x1, y1)` and `(x2, y2)`:
   - Compute:

     ```python
     width = abs(x2 - x1) + 1
     height = abs(y2 - y1) + 1
     area = width * height
     ```

     This counts the number of tiles in the axis-aligned rectangle that spans from the minimum to the maximum x and y, **inclusive**.
   - Track the maximum `area` seen.
3. Return the maximum discrete area.

For the example in `problem.txt`, the largest area is **50**, achieved between `(2,5)` and `(11,1)`:

- `width = 11 - 2 + 1 = 10`
- `height = 5 - 1 + 1 = 5`
- `area = 10 * 5 = 50`.

For the actual `input.txt`, the Part 1 answer is **4773451098**.

## Part 2: Largest rectangle using only red and green tiles

Implementation: `solve_part2(input_file)`.

High-level approach:

1. Parse red tile coordinates.
2. Interpret the red tiles as vertices of a **rectilinear loop** (each consecutive pair shares x or y).
3. Use `build_vertical_segments` and `build_horizontal_segments` to represent the boundary.
4. Use `compute_y_bands` to precompute, for each relevant `y`, the `x`-intervals where tiles are red or green.
5. For each unordered pair of red tiles `(x1, y1)` and `(x2, y2)` considered as opposite corners:
   - Compute the discrete bounding rectangle:

     ```python
     min_x, max_x = min(x1, x2), max(x1, x2)
     min_y, max_y = min(y1, y2), max(y1, y2)
     width = max_x - min_x + 1
     height = max_y - min_y + 1
     area = width * height
     ```

   - Skip this rectangle if `area` is not strictly greater than the current `max_area`.
   - Check whether **every tile** inside the rectangle is red or green by calling:

     ```python
     is_rectangle_valid_fast(min_x, max_x, min_y, max_y, row_ranges, critical_ys)
     ```

   - If valid, update `max_area`.
6. Return `max_area`.

For the example in `problem.txt`, this approach finds the largest valid rectangle has area **24**, e.g. between `(9,5)` and `(2,3)`.

## Test coverage overview

Tests in `test_solution.py` exercise both parts and the helper functions:

- **Parsing & simple geometry**:
  - `test_parse_red_tiles` confirms correct parsing of `(x, y)` pairs.
  - `test_parse_empty_file` ensures empty input yields zero tiles.
  - Multiple `test_calculate_rectangle_area_*` tests validate `calculate_rectangle_area` across normal, reversed, zero-width, zero-height, and example-based cases.
- **Part 1 solver**:
  - `test_solve_part1_example` uses the exact example from `problem.txt` and asserts the maximum area `50`.
  - Additional tests for scenarios like:
    - Two tiles only.
    - All tiles with same x (vertical line).
    - All tiles with same y (horizontal line).
    - Four corners of a square.
    - Mixed rectangles with clearly known max area.
  - `test_actual_input_part1` runs Part 1 on `input.txt` and asserts it returns a positive integer.
- **Polygon & green tiles (Part 2 helpers)**:
  - `TestPart2.setUp` builds the example polygon for reuse.
  - `test_is_point_inside_polygon_interior` and `test_is_point_inside_polygon_exterior` confirm the ray-casting logic.
  - `test_get_green_tiles_count` asserts the exact number of green tiles (46) in the example.
  - `test_build_horizontal_segments` / `test_build_vertical_segments` validate the extracted segment counts and specific segments.
  - `test_compute_valid_ranges_at_y` checks that valid x-ranges at several y-levels match expectations (boundary and interior rows).
- **Part 2 solver**:
  - `test_solve_part2_example` asserts that the example puzzle yields max area `24`.
  - `test_solve_part2_simple_square` validates a simple rectangular polygon where the entire area is valid (max area `25` for a 5x5 square).
  - `test_actual_input_part2` runs Part 2 on `input.txt` and asserts it returns a positive integer.

Together, these tests cover:

- All key helpers (`parse_red_tiles`, `calculate_rectangle_area`, `is_point_inside_polygon`, segment builders, range computation).
- The main control flow for **both** Part 1 and Part 2.
- Edge cases like empty input, degenerate rectangles, and simple polygons.

## Files

- `problem.txt` – Full text of the Day 9 puzzle (both parts) and the example diagrams.
- `input.txt` – Puzzle input (list of red tile coordinates).
- `solution.py` – Python implementation with:
  - `parse_red_tiles`, `calculate_rectangle_area`, `solve_part1`, `solve_part2`.
  - Polygon helpers: `is_point_inside_polygon`, `get_green_tiles`, `build_horizontal_segments`, `build_vertical_segments`, `compute_valid_ranges_at_y`, `compute_y_bands`, `is_rectangle_valid_fast`.
- `test_solution.py` – Unit tests described above.
- `README.md` – This documentation.
